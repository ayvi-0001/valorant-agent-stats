import pandas as pd
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

from LeaderboardScraper import *

Episode5Act2 = LeaderboardScraper(episode=5, act=2, ranks=25, agents=19)
Episode5Act1 = LeaderboardScraper(episode=5, act=1, ranks=25, agents=19)
Episode4Act3 = LeaderboardScraper(episode=4, act=3, ranks=22, agents=19)
Episode4Act2 = LeaderboardScraper(episode=4, act=2, ranks=22, agents=18)
Episode4Act1 = LeaderboardScraper(episode=4, act=1, ranks=22, agents=18)
Episode3Act3 = LeaderboardScraper(episode=3, act=3, ranks=22, agents=17)
Episode3Act2 = LeaderboardScraper(episode=3, act=2, ranks=22, agents=16)
Episode3Act1 = LeaderboardScraper(episode=3, act=1, ranks=22, agents=16)
Episode2Act3 = LeaderboardScraper(episode=2, act=3, ranks=20, agents=15)
Episode2Act2 = LeaderboardScraper(episode=2, act=2, ranks=20, agents=15)
Episode2Act1 = LeaderboardScraper(episode=2, act=1, ranks=20, agents=14)

if __name__ == "__main__":
    Episode5Act2.scrape_stats()
    Episode5Act2.export_stats()
    Episode5Act1.scrape_stats()
    Episode5Act1.export_stats()
    Episode4Act3.scrape_stats()
    Episode4Act3.export_stats()
    Episode4Act2.scrape_stats()
    Episode4Act2.export_stats()
    Episode4Act1.scrape_stats()
    Episode4Act1.export_stats()
    Episode3Act3.scrape_stats()
    Episode3Act3.export_stats()
    Episode3Act2.scrape_stats()
    Episode3Act2.export_stats()
    Episode3Act1.scrape_stats()
    Episode3Act1.export_stats()
    Episode2Act3.scrape_stats()
    Episode2Act3.export_stats()
    Episode2Act2.scrape_stats()
    Episode2Act2.export_stats()
    Episode2Act1.scrape_stats()
    Episode2Act1.export_stats()

df_e5act2 = pd.read_csv('ep-act-csvs/e5act2.csv')
df_e5act1 = pd.read_csv('ep-act-csvs/e5act1.csv')
df_e4act3 = pd.read_csv('ep-act-csvs/e4act3.csv')
df_e4act2 = pd.read_csv('ep-act-csvs/e4act2.csv')
df_e4act1 = pd.read_csv('ep-act-csvs/e4act1.csv')
df_e3act3 = pd.read_csv('ep-act-csvs/e3act3.csv')
df_e3act2 = pd.read_csv('ep-act-csvs/e3act2.csv')
df_e3act1 = pd.read_csv('ep-act-csvs/e3act1.csv')
df_e2act3 = pd.read_csv('ep-act-csvs/e2act3.csv')
df_e2act2 = pd.read_csv('ep-act-csvs/e2act2.csv')
df_e2act1 = pd.read_csv('ep-act-csvs/e2act1.csv')

query_union_all_agent_stats = pysqldf(
            """ 
                select * from df_e5act2 union all
                select * from df_e5act1 union all
                select * from df_e4act3 union all
                select * from df_e4act2 union all
                select * from df_e4act1 union all
                select * from df_e3act3 union all
                select * from df_e3act2 union all
                select * from df_e3act1 union all
                select * from df_e2act3 union all
                select * from df_e2act2 union all
                select * from df_e2act1
            """
        )

query_union_all_agent_stats.to_csv('ep-act-csvs/union_all_agent_stats.csv', index=False)

all_agent_stats = pd.read_csv('ep-act-csvs/union_all_agent_stats.csv')
