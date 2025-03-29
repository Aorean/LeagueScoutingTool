
class stats_for_champpool:
    def __init__(self, matchdata, diff_stats, kda):
        self.puuid = matchdata[1]
        self.champ = matchdata[6]
        self.name = matchdata[3] , "#" , matchdata[4]
        self.kda = kda
        self.kills = matchdata[8]
        self.deaths = matchdata[9]
        self.assists = matchdata[10]
        self.exp = matchdata[13]
        self.level = matchdata[12]
        self.gold = matchdata[14]
        self.visionscore = matchdata[15]

        self.cs_diff = diff_stats["cs"]
        self.exp_diff = diff_stats["exp"]
        self.level_diff = diff_stats["level"]
        self.gold_diff = diff_stats["gold"]
        self.visionscore_diff = diff_stats["visionscore"]

        self.summonerspell1 = matchdata[16]
        self.summonerspell2 = matchdata[17]

        self.role = matchdata[7]

        self.win = matchdata[25]
        self.side = matchdata[5]

    def print_all(self):
        for k,v in self.__dict__.items():
            print(f"{str(k)} = {str(v)}")


class Champpool:
    def __init__(self, dict_champ):

        self.puuid = matchdata[1]
        self.champ = matchdata[6]
        self.games_played = 0

        self.kda = []
        self.kills = []
        self.deaths = []
        self.assists = []
        self.exp = []
        self.level = []
        self.gold = []
        self.visionscore = []

        self.exp_diff = []
        self.level_diff = []
        self.gold_diff = []
        self.visionscore_diff = []

        self.summonerspell1 = []
        self.summonerspell2 = []

        self.fav_role = []

        self.winrate = []
        self.win_blue = []
        self.win_red = []

    #smarter to do that outside of the class? and just insert the data inside

    def avarage_stats(self):
        self.kda = round(len(self.kda) / sum(self.kda), 2)
        self.kills = round(len(self.kills) / sum(self.kills), 2)
        self.deaths = round(len(self.deaths) / sum(self.deaths), 2)
        self.assists = round(len(self.assists) / sum(self.assists), 2)
        self.exp = round(len(self.exp) / sum(self.exp), 2)
        self.level = round(len(self.level) / sum(self.level), 2)
        self.gold = round(len(self.gold) / sum(self.gold), 2)
        self.visionscore = round(len(self.visionscore) / sum(self.visionscore), 2)

        self.exp_diff = round(len(self.exp_diff) / sum(self.exp_diff), 2)
        self.level_diff = round(len(self.level_diff) / sum(self.level_diff), 2)
        self.gold_diff = round(len(self.gold_diff) / sum(self.gold_diff), 2)
        self.visionscore_diff = round(len(self.visionscore_diff) / sum(self.visionscore_diff), 2)


    def count(self):
        self.games_played += 1

