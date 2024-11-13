from __future__ import annotations

import logging
import typing as t
from decimal import Decimal
from enum import Enum
from pathlib import Path

import httpx
import numpy as np
import pandas as pd
from more_itertools import filter_map, first, flatten, windowed, zip_equal
from scrapy.selector import Selector  # type: ignore[import-untyped]

__all__: t.Sequence[str] = ("main",)


logging.basicConfig(
    level=logging.DEBUG,
    format=("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"),
    datefmt="%m-%d %H:%M:%S",
)


ENDPOINT: str = "".join(
    [
        "https://blitz.gg/",
        "valorant/stats/agents?",
        "&mode=competitive",
        "&rank=%s",
        "&act=%s",
    ]
)


def _get_stats(html: str) -> list[t.Any]:
    row_selector = first(
        Selector(text=html, type="html").xpath(
            '//*[@class="\u26A1b73efc61 row \u26A1f6341061"]'
        )
    )

    stats = windowed(
        seq=row_selector.xpath('//*[contains(@class, "type-body2")]/text()').getall(),
        n=7,
        step=7,
    )

    kda = row_selector.xpath('//*[@class="\u26A18a7d61c3"]//span/text()').getall()
    kda_type = lambda t: Decimal(t) if t not in (" ", ", ", "/") else None
    kda_windowed = list(windowed(seq=[*filter_map(kda_type, kda)], n=3, step=3))

    row = list(map(lambda l: list(flatten(l)), zip_equal(stats, kda_windowed)))
    return row


def _generate_df_from_stats(row: list[t.Any]) -> pd.DataFrame:
    df = pd.DataFrame()
    columns = [
        "rank",
        "agent",
        "kd",
        "kills",
        "deaths",
        "assists",
        "win_rate",
        "pick_rate",
        "avg_score",
        "matches",
    ]

    for idx, column in enumerate(columns):
        df.insert(idx, column, None)

    for idx, character in enumerate(row):
        # fmt: off
        rank, agent, kd, win_rate, pick_rate, avg_score, matches, kills, deaths, assists = character
        # Reordering kda to columns 3 ~ 5.
        character_stats = np.array(
            [rank, agent, kd, kills, deaths, assists, win_rate, pick_rate, avg_score, matches]
        )
        # fmt: on

        df.loc[idx] = character_stats

    df = df.set_index("rank")
    _map_types(df)

    return df


def _map_types(df: pd.DataFrame) -> None:
    map_rates = lambda col: round(float(col.replace("%", "")) / 100, 4)
    map_commas = lambda v: int(v.replace(",", ""))

    df["win_rate"] = df["win_rate"].apply(map_rates)
    df["pick_rate"] = df["pick_rate"].apply(map_rates)
    df["matches"] = df["matches"].apply(map_commas)

    int_cols = ["avg_score"]
    df[int_cols] = df[int_cols].astype("int64")

    float_cols = ["kd", "kills", "deaths", "assists"]
    df[float_cols] = df[float_cols].astype("float64")

    df = df.convert_dtypes()


def concat_all_csvs(csv_dir: Path, file_name: str) -> None:
    csvs = filter(lambda p: p.stem != "all" and p.is_file(), csv_dir.iterdir())
    all_dfs = list(map(lambda csv: pd.read_csv(csv), csvs))
    all_dfs_pd = pd.concat(all_dfs[::-1])
    all_dfs_pd = all_dfs_pd.set_index("rank")
    all_dfs_pd.to_csv(csv_dir / file_name)


def main(episodes: t.Sequence[Episode], csv_dir: Path = Path("csvs")) -> None:
    for ep in episodes:
        for act in list(map(lambda a: a.value, Act)):
            act_stats: list[pd.DataFrame] = []

            for rank in list(Rank):
                url = ENDPOINT % (rank.value, ep + act)

                response: httpx.Response = httpx.get(url)
                if response.status_code == 404:
                    continue

                df = _generate_df_from_stats(_get_stats(response.text))

                df["episode"] = ep
                df["act"] = act
                df["placement"] = rank.name

                act_stats.append(df)

            if not act_stats:
                continue

            pd.concat(act_stats).to_csv(csv_dir / f"{ep}{act}.csv")

    concat_all_csvs(csv_dir, "all.csv")


class Rank(int, Enum):
    radiant = 27
    immortal3 = 26
    immortal2 = 25
    immortal1 = 24
    ascendant3 = 23
    ascendant2 = 22
    ascendant1 = 21
    diamond3 = 20
    diamond2 = 19
    diamond1 = 18
    platinum3 = 17
    platinum2 = 16
    platinum1 = 15
    gold3 = 14
    gold2 = 13
    gold1 = 12
    silver3 = 11
    silver2 = 10
    silver1 = 9
    bronze3 = 8
    bronze2 = 7
    bronze1 = 6
    iron3 = 5
    iron2 = 4
    iron1 = 3


class ValueEnum(Enum):
    def __get__(self, instance: t.Any, owner: t.Any) -> str:
        return self.value


class Episode(str, ValueEnum):
    eight = "e8"
    seven = "e7"
    six = "e6"
    five = "e5"
    four = "e4"
    three = "e3"
    two = "e2"
    one = "e1"


class Act(str, ValueEnum):
    one = "act1"
    two = "act2"
    three = "act3"


if __name__ == "__main__":
    # Episodes 1~5 not available on blitz.gg anymore.
    # csv exports for ep 1~5 are from a previous version of this script.
    main(
        [
            Episode.eight,
            Episode.seven,
            Episode.six,
            # Episode.five,
            # Episode.four,
            # Episode.three,
            # Episode.two,
            # Episode.one,
        ]
    )
