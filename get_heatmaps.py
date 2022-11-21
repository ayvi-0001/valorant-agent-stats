import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from union_agent_stats import *

def pivot_pick_rate(df_stats, df_empty):
    for name in (unique_names := df_stats[df_stats["Placement"] == "Radiant"]['Agent'].unique()):
        df_temp = df_stats.loc[df_stats['Agent'] == name].groupby('Placement', sort=False).aggregate({'Pick_Rate': 'mean'})
        # Append each new column and rename to the appropriate agent.
        df_temp = df_temp.rename(columns={"Pick_Rate": name})
        df_empty[name] = df_temp[name]

def plot_heatmap(df, title, episode: str()):
    heatmap = sns.heatmap(df, linewidth=2, linecolor="black", cbar_kws={'pad': 0.03, 'label': 'Average Pick Rate %', 'shrink': 0.95})
    # Add ticklabels.
    heatmap.collections[0].colorbar.set_ticklabels(ticklabels, fontsize=10)
    plt.suptitle(f"Agent Pick Rates per Rank | {title}")
    plt.title(" ")
    plt.xlabel("Agents", labelpad=20)
    plt.ylabel("Rank Placement", labelpad=20)
    plt.tight_layout()
    plt.subplots_adjust(left=0.16, bottom=0.205, right=0.99, top=0.9)
    plt.savefig(f"heatmaps/heatmap-{episode}_avg_agent_pick_rates.png", dpi=100)

# Seaborn parameters.
rc_txt = {'text.color': 'white', 'font.family': 'monospace', 'font.weight': 'bold'}
rc_axes = {'axes.facecolor': 'black', 'axes.titlesize': '14', 'axes.titlelocation': 'center'}
rc_fig = {'figure.facecolor': 'black', 'figure.titlesize': '17', 'figure.figsize': '14, 8'}
rc_label = {'axes.labelcolor': 'white', 'axes.labelsize': '15'}
rc_xtick = {'xtick.color': 'white', 'xtick.labelsize': 'small'}
rc_ytick = {'ytick.color': 'white', 'ytick.labelsize': 'small'}

# cbar_kws has no key for padding ticklabels. Spaces following '%' are there as an artifical padding.
ticklabels = ['0%', '2.5%', '5%', '7.5%', '10%    ', '12.5%', '15%', '17.5%', '20%', '25%'] 

sns.set_theme(rc={**rc_txt, **rc_fig, **rc_axes, **rc_axes, **rc_ytick, **rc_xtick, **rc_label})

""" Plots need to be exported individually """
""" 
    Reindexing:
    pick_rates_e5act2 = pick_rates_e5act2.reindex(df_e5act2['Placement'].unique()[::-1])
    Selects unique placements and reverse order of the array.

"""

if __name__ == "__main__":
    pivot_pick_rate(df_e5act2, (pick_rates_e5act2 := pd.DataFrame()))
    pick_rates_e5act2 = pick_rates_e5act2.reindex(df_e5act2['Placement'].unique()[::-1])
    # plot_heatmap(pick_rates_e5act2, title=Episode5Act2.__str__(), episode=Episode5Act2.episode)

    pivot_pick_rate(df_e5act1, (pick_rates_e5act1 := pd.DataFrame()))
    pick_rates_e5act1 = pick_rates_e5act1.reindex(df_e5act1['Placement'].unique()[::-1])
    # plot_heatmap(pick_rates_e5act1, title=Episode5Act1.__str__(), episode=Episode5Act1.episode)

    pivot_pick_rate(df_e4act3, (pick_rates_e4act3 := pd.DataFrame()))
    pick_rates_e4act3 = pick_rates_e4act3.reindex(df_e4act3['Placement'].unique()[::-1])
    # plot_heatmap(pick_rates_e4act3, title=Episode4Act3.__str__(), episode=Episode4Act3.episode)

    pivot_pick_rate(df_e4act2, (pick_rates_e4act2 := pd.DataFrame()))
    pick_rates_e4act2 = pick_rates_e4act2.reindex(df_e4act2['Placement'].unique()[::-1])
    # plot_heatmap(pick_rates_e4act2, title=Episode4Act2.__str__(), episode=Episode4Act2.episode)

    pivot_pick_rate(df_e4act1, (pick_rates_e4act1 := pd.DataFrame()))
    pick_rates_e4act1 = pick_rates_e4act1.reindex(df_e4act1['Placement'].unique()[::-1])
    # plot_heatmap(pick_rates_e4act1, title=Episode4Act1.__str__(), episode=Episode4Act1.episode)

    pivot_pick_rate(df_e3act3, (pick_rates_e3act3 := pd.DataFrame()))
    pick_rates_e3act3 = pick_rates_e3act3.reindex(df_e3act3['Placement'].unique()[::-1])
    # plot_heatmap(pick_rates_e3act3, title=Episode3Act3.__str__(), episode=Episode3Act3.episode)

    pivot_pick_rate(df_e3act2, (pick_rates_e3act2 := pd.DataFrame()))
    pick_rates_e3act2 = pick_rates_e3act2.reindex(df_e3act2['Placement'].unique()[::-1])
    # plot_heatmap(pick_rates_e3act2, title=Episode3Act2.__str__(), episode=Episode3Act2.episode)

    pivot_pick_rate(df_e3act1, (pick_rates_e3act1 := pd.DataFrame()))
    pick_rates_e3act1 = pick_rates_e3act1.reindex(df_e3act1['Placement'].unique()[::-1])
    # plot_heatmap(pick_rates_e3act1, title=Episode3Act1.__str__(), episode=Episode3Act1.episode)

    pivot_pick_rate(df_e2act3, (pick_rates_e2act3 := pd.DataFrame()))
    pick_rates_e2act3 = pick_rates_e2act3.reindex(df_e2act3['Placement'].unique()[::-1])
    # plot_heatmap(pick_rates_e2act3, title=Episode2Act3.__str__(), episode=Episode2Act3.episode)

    pivot_pick_rate(df_e2act2, (pick_rates_e2act2 := pd.DataFrame()))
    pick_rates_e2act2 = pick_rates_e2act2.reindex(df_e2act2['Placement'].unique()[::-1])
    # plot_heatmap(pick_rates_e2act2, title=Episode2Act2.__str__(), episode=Episode2Act2.episode)

    pivot_pick_rate(df_e2act1, (pick_rates_e2act1 := pd.DataFrame()))
    pick_rates_e2act1 = pick_rates_e2act1.reindex(df_e2act1['Placement'].unique()[::-1])
    plot_heatmap(pick_rates_e2act1, title=Episode2Act1.__str__(), episode=Episode2Act1.episode)
