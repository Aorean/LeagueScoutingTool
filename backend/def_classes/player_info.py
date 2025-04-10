# potentially following with another class for sql table
# playerinfo == puuid, rank, winrate, avrg. stats

class Playerinfo:
    def __init__(self, json_playerinfos):
        summonerid_data = json_playerinfos[0]
        rank_data = json_playerinfos[1]

        self.puuid = summonerid_data["puuid"]
        self.summonerlevel = summonerid_data["summonerLevel"]
        self.profile_icon = summonerid_data["profileIconId"]
        self.division = rank_data[0]["tier"]
        self.rank = rank_data[0]["rank"]
        self.wins_total = rank_data[0]["wins"]
        self.losses_total = rank_data[0]["losses"]
        self.stuck = rank_data[0]["veteran"]
