class Champpool:
    def __init__(self, dict_matches, matchid, puuid, query_participants):
        #match = all players in the match
        match = dict_matches[matchid][1]

        if match.puuid == puuid:
            self.puuid = puuid
            self.champ = match.champ
            self.kda = dict_champ_stats["kda"]
            self.kills = dict_champ_stats["kills"]
            self.deaths = dict_champ_stats["deaths"]
            self.assists = dict_champ_stats["assists"]
            self.exp = dict_champ_stats["exp"]
            self.level = dict_champ_stats["level"]
            self.gold = dict_champ_stats["gold"]
            self.visionscore = dict_champ_stats["visionscore"]
            self.fav_role = dict_champ_stats["fav_role"]
            self.exp_diff = dict_champ_stats["exp_diff"]
            self.level_diff = dict_champ_stats["level_diff"]
            self.gold_diff = dict_champ_stats["gold_diff"]
            self.visionscore_diff = dict_champ_stats["visionscore_diff"]




