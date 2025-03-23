class Match:
    def __init__ (self, puuid, matchid, single_match):
        metadata = single_match["metadata"]
        participants = metadata["participants"]
        info = single_match["info"]
        self.PUUID_MATCHID = puuid + matchid
        self.puuid = puuid
        self.matchid = matchid
        self.participants = participants
        self.gamestart = str(info["gameStartTimestamp"])
        self.gameend = str(info["gameEndTimestamp"])
        self.gameduration = str(info["gameDuration"])
        self.tournamentcode = info["tournamentCode"]
        self.gamemode = info["gameMode"]


class Playerstats:
    def __init__(self, participant, matchid, puuid):
        self.PUUID_MATCHID = puuid + matchid
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

