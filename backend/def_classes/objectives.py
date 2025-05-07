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