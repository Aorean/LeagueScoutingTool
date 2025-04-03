class Champpool:
    def __init__(self, champ, puuid, matchdata=None):
        self.PUUID_CHAMP = puuid + champ

        self.puuid = puuid
        self.champ = champ

        self.name = None
        self.tagline = None

        self.games_played = 0

        self.kda = []
        self.kills = []
        self.deaths = []
        self.assists = []
        self.cs = []
        self.exp = []
        self.level = []
        self.gold = []
        self.visionscore = []

        self.cs_diff = []
        self.exp_diff = []
        self.level_diff = []
        self.gold_diff = []
        self.visionscore_diff = []

        self.summonerspell1 = []
        self.summonerspell2 = []

        self.fav_role = []

        self.team = []

        self.winrate = []
        self.win_blue = []
        self.win_red = []

    #smarter to do that outside of the class? and just insert the data inside

    def avarage_stats(self):
        #stats
        try:
            self.kda = round(sum(self.kda) / len(self.kda), 2)
        except ZeroDivisionError as e:
            self.kda = 0

        try:
            self.kills = round(sum(self.kills) / len(self.kills), 2)
        except ZeroDivisionError as e:
            self.kills = 0

        try:
            self.deaths = round(sum(self.deaths) / len(self.deaths), 2)
        except ZeroDivisionError as e:
            self.deaths = 0

        try:
            self.assists = round(sum(self.assists) / len(self.assists), 2)
        except ZeroDivisionError as e:
            self.assists = 0

        try:
            self.cs = round(sum(self.cs) / len(self.cs), 2)
        except ZeroDivisionError as e:
            self.cs = 0

        try:
            self.exp = round(sum(self.exp) / len(self.exp), 2)
        except ZeroDivisionError as e:
            self.exp = 0

        try:
            self.level = round(sum(self.level) / len(self.level), 2)
        except ZeroDivisionError as e:
            self.level = 0

        try:
            self.gold = round(sum(self.gold) / len(self.gold), 2)
        except ZeroDivisionError as e:
            self.gold = 0

        try:
            self.visionscore = round(sum(self.visionscore) / len(self.visionscore), 2)
        except ZeroDivisionError as e:
            self.visionscore = 0

        #diff stats
        try:
            self.cs_diff = round(sum(self.cs_diff) / len(self.cs_diff), 2)
        except ZeroDivisionError as e:
            self.cs_diff = 0

        try:
            self.exp_diff = round(sum(self.exp_diff) / len(self.exp_diff), 2)
        except ZeroDivisionError as e:
            self.exp_diff = 0

        try:
            self.level_diff = round(sum(self.level_diff) / len(self.level_diff), 2)
        except ZeroDivisionError as e:
            self.level_diff = 0

        try:
            self.gold_diff = round(sum(self.gold_diff) / len(self.gold_diff), 2)
        except ZeroDivisionError as e:
            self.gold_diff = 0

        try:
            self.visionscore_diff = round(sum(self.visionscore_diff) / len(self.visionscore_diff), 2)
        except ZeroDivisionError as e:
            self.visionscore_diff = 0

        #summonerspells
        summonerspell1_max = ""
        summonerspell1_value = 0
        for val in self.summonerspell1:
            value = self.summonerspell1.count(val)
            if value > summonerspell1_value:
                summonerspell1_value = value
                summonerspell1_max = val
        self.summonerspell1 = summonerspell1_max


        summonerspell2_max = ""
        summonerspell2_value = 0
        for val in self.summonerspell2:
            value = self.summonerspell2.count(val)
            if value > summonerspell2_value:
                summonerspell2_value = value
                summonerspell2_max = val
        self.summonerspell2 = summonerspell2_max

        #winrates
        blue_count = 0
        red_count = 0
        blue_win = 0
        red_win = 0
        for win, team in zip(self.winrate, self.team):
            if team == 100:
                blue_count += 1
                if win:
                    blue_win += 1

            elif team == 200:
                red_count += 1
                if win:
                    red_win += 1

        winrate_blue = 0
        try:
            winrate_blue = round(blue_win / blue_count, 4)
        except ZeroDivisionError as e:
            winrate_blue = 0

        winrate_red = 0
        try:
            winrate_red = round(red_win / red_count, 4)
        except ZeroDivisionError as e:
            winrate_red = 0

        try:
            self.winrate = round((blue_win + red_win) / (blue_count + red_count), 2)
        except ZeroDivisionError as e:
            self.winrate = 0



        self.win_blue = winrate_blue
        self.win_red = winrate_red

        role_max = ""
        role_value = 0
        for val in self.fav_role:
            value = self.fav_role.count(val)
            if value > role_value:
                role_value = value
                role_max = val
        self.fav_role = role_max

    def count(self):
        self.games_played += 1

    def print_all(self):
        for k,v in self.__dict__.items():
            print(f"{str(k)} = {str(v)}")
