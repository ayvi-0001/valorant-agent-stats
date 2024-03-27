import typing as t
from pathlib import Path

import pandas as pd

__all__: t.Sequence[str] = ("plot_heatmap", "pivot_pick_rate")


RC_PARAMS = {
    "axes.facecolor": "black",
    "axes.labelcolor": "white",
    "axes.labelsize": "15",
    "axes.titlelocation": "center",
    "axes.titlesize": "14",
    "figure.facecolor": "black",
    "figure.figsize": "14, 8",
    "figure.titlesize": "17",
    "font.family": "monospace",
    "font.weight": "bold",
    "text.color": "white",
    "xtick.color": "white",
    "xtick.labelsize": "small",
    "ytick.color": "white",
    "ytick.labelsize": "small",
}

CSV_DIR: t.Final[Path] = Path("csvs")
HEATMAPS_DIR: t.Final[Path] = Path("heatmaps")


def pivot_pick_rate(df_stats: pd.DataFrame) -> pd.DataFrame:
    new_df = pd.DataFrame()
    unique_agents = df_stats[df_stats["placement"] == "radiant"]["agent"].unique()

    for name in unique_agents:
        pivotted: pd.DataFrame = (
            df_stats.loc[df_stats["agent"] == name]
            .groupby("placement", sort=False)
            .aggregate({"pick_rate": "mean"})
        )
        # Append each new column and rename to the appropriate agent.
        pivotted = pivotted.rename(columns={"pick_rate": name})
        new_df[name] = pivotted[name]

    return new_df.fillna(0)


def plot_heatmap(
    df: pd.DataFrame,
    heatmap_dir: Path,
    title: str,
    cmap: str = "rocket",
) -> None:
    import matplotlib.pyplot as plt
    import seaborn as sns  # type: ignore

    sns.reset_orig()
    sns_ = sns
    plt_ = plt

    global RC_PARAMS
    sns_.set_theme(rc=RC_PARAMS)

    cbar_kws = {"pad": 0.03, "label": "Average Pick Rate %", "shrink": 0.95}
    heatmap = sns_.heatmap(
        df, cmap=cmap, linewidth=2, linecolor="black", cbar_kws=cbar_kws
    )

    # cbar_kws has no key for padding ticklabels. Spaces following '%' are there as an artifical padding.
    ticklabels = ["0%", "2.5%", "5%", "7.5%", "10%    ", "12.5%", "15%", "17.5%", "20%", "25%"]  # fmt: skip
    heatmap.collections[0].colorbar.set_ticklabels(ticklabels, fontsize=10)

    plt_.suptitle(f"Agent Pick Rates per Rank | {title}\n")
    plt_.xlabel(
        "Agents\n(ordered by highest[left] win rate to lowest[right])",
        labelpad=20,
    )
    plt_.ylabel("Rank Placement", labelpad=20)
    plt_.tight_layout()
    plt_.subplots_adjust(left=0.16, bottom=0.205, right=0.99, top=0.9)

    target_dir = Path(heatmap_dir / cmap)
    target_dir.mkdir(exist_ok=True)

    plt_.savefig(target_dir / f"{title}.svg", dpi=300)
    plt.clf()


if __name__ == "__main__":
    pick_rates_dir = CSV_DIR / "pick_rates"
    pick_rates_dir.mkdir(exist_ok=True)

    for csv in filter(lambda p: p.stem != "all" and p.is_file(), CSV_DIR.iterdir()):
        df = pivot_pick_rate(pd.read_csv(csv, index_col=None))
        df.to_csv(pick_rates_dir / f"pick_rates_{csv.name}")

        plot_heatmap(
            pivot_pick_rate(pd.read_csv(csv, index_col=None)),
            heatmap_dir=HEATMAPS_DIR,
            title=csv.stem,
        )
