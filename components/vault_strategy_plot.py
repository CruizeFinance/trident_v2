import numpy as np
import pandas as pd
import plotly.express as px

from components import FirebaseDataManager
from utilities.enum import Vaults


class VaultStrategyPlot(object):
    def __init__(self, vault, asset_symbol):
        self.vault = vault
        self.asset_symbol = asset_symbol

    def strategy_plot_data(self):
        if self.vault == Vaults.PROTECTEDTWINPEAKS.value:
            return self.twin_peaks_plot()

    def twin_peaks_plot(
        self,
    ):

        leftmost = -0.3
        rightmost = 0.3
        step = 0.0005
        grid = np.arange(leftmost, rightmost, step)

        firebase_db_manager_obj = FirebaseDataManager()

        asset_info = firebase_db_manager_obj.fetch_data(
            collection_name=self.vault, document_name=self.asset_symbol
        )
        base_apy = float(asset_info["apy"]["base_apy"].split("%")[0]) / 100
        participation_rate = float(asset_info["participation_rate"])
        lower_barrier = float(asset_info["price_range"]["lower_bound"]) / 100
        upper_barrier = float(asset_info["price_range"]["upper_bound"]) / 100
        print(lower_barrier, upper_barrier)
        twin_win_data = [
            self._twin_peaks_plot(
                1 + round(i, 3),
                upper_barrier,
                lower_barrier,
                base_apy=base_apy,
                part_rate=participation_rate,
            )
            for i in grid
        ]
        twin_win_data = [(data * 100) for data in twin_win_data]
        twin_win_df = pd.DataFrame(
            {"results": twin_win_data, "pcg_moved": (grid + 1) * 100}
        )
        return twin_win_df

    def _twin_peaks_plot(
        self, pcg_change, upper_barrier, lower_barrier, base_apy, part_rate
    ):

        bad_condition_up = pcg_change > upper_barrier
        bad_condition_down = pcg_change < lower_barrier
        if bad_condition_up | bad_condition_down:
            return base_apy * 0.9
        else:
            return (max(1 - pcg_change, pcg_change - 1) * part_rate + base_apy) * 0.9


if __name__ == "__main__":
    v = VaultStrategyPlot("protected_twin_peaks", "ETH")
    print(v.strategy_plot_data())
    df = v.strategy_plot_data()
    fig = px.line(df, x="pcg_moved", y="results", title="Twin Win", height=400)
    fig.update_yaxes(scaleratio=100)
    fig.update_traces(mode="markers+lines")
    fig.show()
