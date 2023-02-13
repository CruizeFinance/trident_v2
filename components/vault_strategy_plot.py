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
            self._twin_peaks_plot(1 + round(i, 3), upper_barrier, lower_barrier)
            for i in grid
        ]
        twin_win_data = [round(data, 2) for data in twin_win_data]
        twin_win_df = pd.DataFrame({"results": twin_win_data, "pcg_moved": np.round(grid+1, 2)})
        return twin_win_df

    def _twin_peaks_plot(self, pcg_change, upper_barrier, lower_barrier):

        bad_condition_up = pcg_change > upper_barrier
        bad_condition_down = pcg_change < lower_barrier
        if bad_condition_up | bad_condition_down:
            return 0.02 * 0.9
        else:
            return (max(1 - pcg_change, pcg_change - 1) * 1.59 + 0.02) * 0.9


if __name__ == "__main__":
    v = VaultStrategyPlot('protected_twin_peaks')
    print(v.strategy_plot_data())