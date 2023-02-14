import numpy as np
import pandas as pd
import plotly.express as px

from utilities.enum import Vaults


class VaultStrategyPlot(object):
    def __init__(self, vault):
        self.vault = vault

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

        upper_barrier = 1.08
        lower_barrier = 0.92
        twin_win_data = [
            self._twin_peaks_plot(
                1 + round(i, 3), upper_barrier, lower_barrier, base_apy=0.005
            )
            for i in grid
        ]
        twin_win_df = pd.DataFrame({"results": twin_win_data, "pcg_moved": grid + 1})
        return twin_win_df

    def _twin_peaks_plot(self, pcg_change, upper_barrier, lower_barrier, base_apy):

        bad_condition_up = pcg_change > upper_barrier
        bad_condition_down = pcg_change < lower_barrier
        if bad_condition_up | bad_condition_down:
            return base_apy * 0.9
        else:
            return (max(1 - pcg_change, pcg_change - 1) * 1.59 + base_apy) * 0.9


if __name__ == "__main__":
    leftmost = -0.3
    rightmost = 0.3
    step = 0.0005
    grid = np.arange(leftmost, rightmost, step)

    upper_barrier = 1.1
    lower_barrier = 0.9
    twin_win_ = [
        VaultStrategyPlot("protected_twin_peaks")._twin_peaks_plot(
            1 + round(i, 3), upper_barrier, lower_barrier, 0.005
        )
        for i in grid
    ]
    df = pd.DataFrame({"results": twin_win_, "pcg_moved": grid + 1})

    fig = px.line(df, x="pcg_moved", y="results", title="Twin Win")
    fig.update_yaxes(scaleratio=100)
    fig.update_traces(mode="markers+lines")
    # py.plot()
    fig.show()
