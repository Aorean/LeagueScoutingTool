class aram_Match:
    def __init__(self, puuid, matchid, single_match):
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
        self.gamemode = info["gameMode"]
        self.season = season
        self.patch = patch

class aram_Playerstats:
    def __init__(self, participant, match_json):

        info = match_json["info"]
        metadata = match_json["metadata"]

        full_patch = info["gameVersion"]
        list_patch = full_patch.split(".")
        season = list_patch[0]
        patch = list_patch[0]+list_patch[1]

        self.PUUID_MATCHID = participant["puuid"] + metadata["matchId"]
        self.puuid = participant["puuid"]
        self.matchid = metadata["matchId"]
        self.gamertag = participant["riotIdGameName"]
        self.tagline = participant["riotIdTagline"]
        self.team = participant["teamId"]
        self.champ = participant["championName"]
        self.kills = participant["kills"]
        self.deaths = participant["deaths"]
        self.assists = participant["assists"]
        self.cs = participant["totalMinionsKilled"]
        self.level = participant["champLevel"]
        self.exp = participant["champExperience"]
        self.gold = participant["goldEarned"]
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
            try:
                self.item4 = dict_items[i_id4]
            except KeyError as e:
                self.item4 = "Item not Found"


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
            print(f"{str(k)} = {str(v)}")