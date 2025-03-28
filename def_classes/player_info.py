class avrg_stats:
    def __init__(self, avrg_data):
        self.winrate =
        self.winrate_blue =
        self.winrate_red =
        self.kda =
        self.cs




class Player_Info:
    def __init__(self,
                 puuid,
                 elo,
                 wins,
                 losses,
                 ):
        self.puuid = puuid
        self.matchhistory = []
        self.elo = elo
        self.wins = wins
        self.losses = losses
        self.totalgames = wins + losses
        self.winrate = round((wins + losses) / wins, 2)

        self.avrg_cs = 0.0
        self.avrg_level = 0.0
        self.avrg_exp = 0.0
        self.avrg_gold = 0.0
        self.avrg_visionscore = 0.0

        self.avrg_cs_diff = 0.0
        self.avrg_gold_diff = 0.0
        self.avrg_exp_diff = 0.0
        self.avrg_level_diff = 0.0
        self.avrg_visionscore_diff = 0.0

    def set_matchhistory(self, matchhistory):
        self.matchhistory = matchhistory

    #maybe possible to get all the avrg stats into one function?
    def set_avrg_cs(self, cs_total, games_played):
        avrg_cs = cs_total / games_played
        self.avrg_cs = avrg_cs

    def set_avrg_level(self, level_total, games_played):
        avrg_level = level_total / games_played
        self.avrg_level = avrg_level

"""              avrg_exp,
                 avrg_gold,
                 avrg_visionscore,
                 avrg_cs_diff,
                 avrg_gold_diff,
                 avrg_exp_diff,
                 avrg_level_diff,
                 avrg_visionscore_diff
"""