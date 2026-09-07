import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

MEMBERS_PER_RALLY = 15

class KSBT:
    def __init__(self):
        self.df = pd.read_csv("KSBT.csv", sep=";", encoding="utf-8")
        self.dates = list(self.df["Date"])

        self.bt1_dmg = self.df["BT1 Damage (in millions)"]
        self.bt2_dmg = self.df["BT2 Damage (in millions)"]
        self.bt1_rallies = self.df["BT1 Rallies"]
        self.bt2_rallies = self.df["BT2 Rallies"]

        self.bt1 = list(zip(self.bt1_dmg, self.bt1_rallies))
        self.bt2 = list(zip(self.bt2_dmg, self.bt2_rallies))

        self.fig, self.axes = plt.subplots(2, 2, figsize=(10, 8))

    def damage_over_time(self):
        diff = [b1 - b2 for b1, b2 in zip(self.bt1_dmg, self.bt2_dmg)]
        tot = [b1 + b2 for b1, b2 in zip(self.bt1_dmg, self.bt2_dmg)]

        ax = self.axes[0, 0]
        ax.plot(self.dates, self.bt1_dmg, label="BT1", linewidth=2, marker="o", markersize=4)
        ax.plot(self.dates, self.bt2_dmg, label="BT2", linewidth=2, marker="o", markersize=4)
        ax.plot(self.dates, diff, label="Difference (BT1 - BT2)", linewidth=1, marker="o", markersize=2, linestyle="--")
        ax.plot(self.dates, tot, label="Total", linewidth=1, marker="o", markersize=2, linestyle="--")
        ax.set_title("Damage over time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Damage (millions)")
        ax.legend()

    def rallies_over_time(self):
        ax = self.axes[0, 1]
        ax.plot(self.dates, self.bt1_rallies, label="BT1", linewidth=2, marker="o", markersize=4)
        ax.plot(self.dates, self.bt2_rallies, label="BT2", linewidth=2, marker="o", markersize=4)
        ax.set_title("Rallies over time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Rallies")
        ax.legend()

    def damage_per_rally(self):
        bt1_ratio = [dmg / rallies for dmg, rallies in self.bt1]
        bt2_ratio = [dmg / rallies for dmg, rallies in self.bt2]

        diff = [b1 - b2 for b1, b2 in zip(bt1_ratio, bt2_ratio)]

        ax = self.axes[1, 0]
        ax.plot(self.dates, bt1_ratio, label="BT1", linewidth=2, marker="o", markersize=4)
        ax.plot(self.dates, bt2_ratio, label="BT2", linewidth=2, marker="o", markersize=4)
        ax.plot(self.dates, diff, label="Difference (BT1 - BT2)", linewidth=1, marker="o", markersize=2, linestyle="--")
        ax.set_title("Damage per rally")
        ax.set_xlabel("Date")
        ax.set_ylabel("Damage/rally (millions)")
        ax.legend()

    def damage_per_member(self):
        bt1_ratio_mem = [dmg / rallies / MEMBERS_PER_RALLY for dmg, rallies in self.bt1]
        bt2_ratio_mem = [dmg / rallies / MEMBERS_PER_RALLY for dmg, rallies in self.bt2]

        diff = [b1 - b2 for b1, b2 in zip(bt1_ratio_mem, bt2_ratio_mem)]

        ax = self.axes[1, 1]
        ax.plot(self.dates, bt1_ratio_mem, label="BT1", linewidth=2, marker="o", markersize=4)
        ax.plot(self.dates, bt2_ratio_mem, label="BT2", linewidth=2, marker="o", markersize=4)
        ax.plot(self.dates, diff, label="Difference (BT1 - BT2)", linewidth=1, marker="o", markersize=2, linestyle="--")
        ax.set_title("Damage per rally member")
        ax.set_xlabel("Date")
        ax.set_ylabel("Damage/rally/member (millions)")
        ax.legend()

    def plot(self):
        self.damage_over_time()
        self.rallies_over_time()
        self.damage_per_rally()
        self.damage_per_member()

        for ax in self.axes.flat:
            ax.tick_params(axis='x', rotation=45)
            ax.yaxis.set_major_locator(MaxNLocator(nbins=15))

        plt.tight_layout()
        plt.savefig("overview.png")
        plt.show()


if __name__ == "__main__":
    ksbt = KSBT()
    ksbt.plot()