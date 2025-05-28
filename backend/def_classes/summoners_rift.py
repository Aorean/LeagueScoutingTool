class Player:
    def __init__(self, puuid, gamertag, tagline):
        self.puuid = puuid
        self.gamertag = gamertag
        self.tagline = tagline


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


class Matchhistory:
    def __init__(self, puuid, matchhistory):
        self.PUUID = puuid
        self.matchhistory = matchhistory

#### SUMMONERS RIFT ####
class Match:
    def __init__ (self, puuid, matchid, single_match):

        metadata = single_match["metadata"]
        participants = metadata["participants"]
        info = single_match["info"]

        full_patch = info["gameVersion"]
        list_patch = full_patch.split(".")
        season = list_patch[0]
        patch = str(list_patch[0])+"."+str(list_patch[1])
        
        self.PUUID_MATCHID = puuid + matchid
        self.puuid = puuid
        self.matchid = matchid
        self.participants = participants
        self.gamestart = str(info["gameStartTimestamp"])
        self.gameend = str(info["gameEndTimestamp"])
        self.gameduration = str(info["gameDuration"])
        self.tournamentcode = info["tournamentCode"]
        self.gamemode = info["gameMode"]
        self.season = season
        self.patch = patch


class Playerstats:

    def __init__(self, participant, matchid, puuid, match_json):
        info = match_json["info"]

        full_patch = info["gameVersion"]
        list_patch = full_patch.split(".")
        season = list_patch[0]
        patch = list_patch[0] + "." + list_patch[1]
        

        self.PUUID_MATCHID = participant["puuid"] + matchid
        self.puuid = participant["puuid"]
        self.matchid = matchid

        self.gamertag = participant["riotIdGameName"]
        self.tagline = participant["riotIdTagline"]
        self.team = participant["teamId"]
        self.champ = participant["championName"]
        self.role = participant["teamPosition"]
        self.kills = participant["kills"]
        self.deaths = participant["deaths"]
        self.assists = participant["assists"]
        #set kda function
        self.cs = participant["totalMinionsKilled"]
        self.level = participant["champLevel"]
        self.exp = participant["champExperience"]
        self.gold = participant["goldEarned"]
        self.visionscore = participant["visionScore"]
        self.summonerspell1 = participant["summoner1Id"]
        self.summonerspell2 = participant["summoner2Id"]
        self.item1 = participant["item0"]
        self.item2 = participant["item1"]
        self.item3 = participant["item2"]
        self.item4 = participant["item3"]
        self.item5 = participant["item4"]
        self.item6 = participant["item5"]
        self.keyrune = participant["perks"]["styles"][0]["selections"][0]["perk"]
        self.win = participant["win"]

        self.season = season
        self.patch = patch


    def translate_ids(self, dict_items, dict_summonerspells, dict_primary_rune):

        i_id1 = self.item1
        i_id2 = self.item2
        i_id3 = self.item3
        i_id4 = self.item4
        i_id5 = self.item5
        i_id6 = self.item6

        if self.item1 == 0:
            self.item1 = 0
        else:
            self.item1 = dict_items[i_id1]

        if self.item2 == 0:
            self.item2 = 0
        else:
            self.item2 = dict_items[i_id2]

        if self.item3 == 0:
            self.item3 = 0
        else:
            self.item3 = dict_items[i_id3]

        if self.item4 == 0:
            self.item4 = 0
        else:
            self.item4 = dict_items[i_id4]

        if self.item5 == 0:
            self.item5 = 0
        else:
            self.item5 = dict_items[i_id5]

        if self.item6 == 0:
            self.item6 = 0
        else:
            self.item6 = dict_items[i_id6]

        s_id1 = self.summonerspell1
        s_id2 = self.summonerspell2

        self.summonerspell1 = dict_summonerspells[s_id1]
        self.summonerspell2 = dict_summonerspells[s_id2]

        pr_id1 = self.keyrune

        self.keyrune = dict_primary_rune[pr_id1]

    def print_all(self):
        for k,v in self.__dict__.items():
            print(f"{str(k)} = {str(v)})")

class Objectives:
    def __init__(self, team, matchid):

        self.MATCHID_TEAMID = matchid + str(team["teamId"])
        self.matchid = matchid
        self.teamid = team["teamId"]

        objectives = team.get("objectives", 0)

        self.baronfirst = objectives.get("baron", {}).get("first", False)
        self.baronkills = objectives.get("baron", {}).get("kills", False)
        self.atakhanfirst = objectives.get("atakhan", {}).get("first", False)
        self.atakhankills = objectives.get("atakhan", {}).get("kills", False)
        self.grubsfirst = objectives.get("horde", {}).get("first", False)
        self.grubskills = objectives.get("horde", {}).get("kills", False)
        self.dragonfirst = objectives.get("dragon", {}).get("first", False)
        self.dragonkills = objectives.get("dragon", {}).get("kills", False)
        self.riftheraldfirst = objectives.get("riftHerald", {}).get("first", False)
        self.riftheraldkills = objectives.get("riftHerald", {}).get("kills", False)
        self.towerfirst = objectives.get("tower", {}).get("first", False)
        self.towerkills = objectives.get("tower", {}).get("kills", False)
        self.inhibfirst = objectives.get("inhibitor", {}).get("first", False)
        self.inhibkills = objectives.get("inhibitor", {}).get("kills", False)


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


#### HOWLING ABYSS ####






#### ARENA ####



#### BANDLE CITY ####