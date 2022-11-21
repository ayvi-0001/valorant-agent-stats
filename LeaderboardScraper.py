import re
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

class LeaderboardScraper:
    """ Web scraper for Valorant leaderboard stats on Blitz.gg """
    """ Class instance will only scrape stats for the approriate episode, act, agents, and ranks set in initialization """
    """ 
        Example: 
        Episode5Act2 = LeaderboardScraper(episode=5, act=2, ranks=25, agents=19)
        # Episode5Act2.scrape_stats()
        # Episode5Act2.export_stats() 
    """

    def __init__(self, ranks= int(), episode= str(), act= str(), agents= int()):
        self._episode = episode
        self.ranks = ranks
        self.agents = agents
        self.act = act
        self.agent_stats = []

    def __repr__(self):
        return f'LeaderboardScraper_episode{self._episode}_act_{self.act}'
    
    def __str__(self):
        return f'Episode {self._episode} Act {self.act}'

    @property
    # Episode string to input in url parameters.
    def episode(self):
        return f'e{self._episode}act{self.act}'

    @property
    def tiered_ranks(self):
        # First rank url begins at '%rank=3'. 
        # Adjust self.ranks to start on the correct page. 
        adjusted = self.ranks + 3
        return range(3, adjusted)

    @property
    def url(self):
        # Returns url with instance's episode/act set as a paramter.
        base_url = 'https://blitz.gg/valorant/stats/agents?sortBy=matches&type=general&map=all&act='
        comp_params = '&queue=competitive&tier=27&sortDirection=DESC&mode=competitive&rank='
        return f'{base_url}{self.episode}{comp_params}'

    def scrape_stats(self):
        for rank in self.tiered_ranks:
            url = f'{self.url}' + str(rank)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # List of column_names.
            c_name = list(x.text.replace(' ', '_').replace('%', 'Rate') for x in soup("p"))[:9]
            
            # Setup 1st dataframe.
            gen_data = {c_name[0]: {}, c_name[1]: {}, c_name[2]: {}, c_name[5]: {}, c_name[7]: {}, c_name[8]: {}}
            df1 = pd.DataFrame(gen_data)

            # Scrape general agent stats.
            np_data = np.array(
                list(x.text for x in soup.find_all("span", attrs={'class': 'type-body2'}))
                ).reshape(self.agents, 6)
                # Numpy array reshaped to number of agents in act and columns in 1st dataframe.

            # Each array set as values for last row in dataframe.
            for i in range(self.agents):
                df1.loc[len(df1)] = np_data[i]

            # Split ['KDA'] in column_names, into ['K', 'D', 'A'].
            kda_name = re.findall('.', c_name[3])

            # Setup 2nd dataframe.
            kda_data = {kda_name[0]: {}, kda_name[1]: {}, kda_name[2]: {}}
            df2 = pd.DataFrame(kda_data)

            # Scrape KDA stats.
            kda = list(x.text for x in soup.find_all("div", attrs={'class': 'â¡12fc343'}))

            # Strip whitespace and split on '/' for Kills/Deaths/Assists. 
            for i in range(self.agents):
                df2.loc[len(df2)] = str(kda[i]).replace(' ','').replace('\n','').split('/')

            # Concat columns from dataframes.
            df = pd.concat([df1, df2], axis=1)

            # Scrape win rates and avg. scores.
            # Both come in from same tag as [{win_rate}, {avg._score}, {win_rate} ..]
            # List slice has a step to capture only 1 of the 2. Arrays stacked on rows to separate.
            tags_win_avg = np.row_stack(
                (np.array(list(x.text for x in soup("p"))[9:-3:2]), #Win %
                (np.array(list(x.text for x in soup("p"))[10:-3:2]) #Avg. Score
                    )
                )
            )
            # Add 2 new columns for win rate and avg. score.
            df[c_name[4]] = tags_win_avg[0]
            df[c_name[-3]] = tags_win_avg[1]

            # Scrape Act and Placement.
            df['Act'] = list(x.text for x in soup.find_all('span', attrs={'class': 'type-form--button text'}))[4]
            df['Placement'] = list(x.text for x in soup.find_all('span', attrs={'class': 'type-form--button text'}))[3]

            # Rearrange columns. Assigned to 'c' for brevity.
            c = df.columns.to_list()
            df = df[[c[11],c[12],c[1],c[0],c[2],c[6],c[7],c[8],c[4],c[3],c[9],c[10],c[5]]]

            # Recast types & strip characters.
            df[c_name[0]] = df[c_name[0]].astype('int')
            df[c_name[-3]] = df[c_name[-3]].astype('int')
            df[c_name[1]] = df[c_name[1]].astype('string')
            df["Placement"] = df["Placement"].astype('string')
            df[c_name[2]] = df[c_name[2]].astype('float')
            df[kda_name[0]] = df[kda_name[0]].astype('float')
            df[kda_name[1]] = df[kda_name[1]].astype('float')
            df[kda_name[2]] = df[kda_name[2]].astype('float')
            df[c_name[-2]] = df[c_name[-2]].apply(lambda x : x.replace('%', '')).astype('float')
            df[c_name[-1]] = df[c_name[-1]].apply(lambda x : x.replace(',', '')).astype('int')
            df['Act'] = df['Act'].apply(lambda x : x.replace(' ','').replace('\n','')).astype('string')
            df[c_name[4]] = round(df[c_name[4]].apply(lambda x : x.replace('%', '')).astype('float') / 100, 2)
            df[c_name[5]] = round(df[c_name[5]].apply(lambda x : x.replace('%', '')).astype('float') / 100, 4)

            # Each dataframe appended to class attribute for exporting. 
            self.agent_stats.append(df)
    
    def export_stats(self):
        # Concat all dataframes and export as csv.
        for i in range(0, len(self.agent_stats)):
            pd.concat(self.agent_stats).to_csv(f'{self.episode}.csv', index=False)
