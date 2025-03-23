class Objectives:
    def __init__(self, team, matchid):
        self.MATCHID_TEAMID = matchid + str(team["teamId"])
        self.matchid = matchid
        self.teamid = team["teamId"]
        self.baronfirst = team["objectives"]["baron"]["first"]
        self.baronkills = team["objectives"]["baron"]["kills"]
        self.atakhanfirst = team["objectives"]["atakhan"]["first"]
        self.atakhankills = team["objectives"]["atakhan"]["kills"]
        self.grubsfirst = team["objectives"]["horde"]["first"]
        self.grubskills = team["objectives"]["horde"]["kills"]
        self.dragonfirst = team["objectives"]["dragon"]["first"]
        self.dragonkills = team["objectives"]["dragon"]["kills"]
        self.riftheraldfirst = team["objectives"]["riftHerald"]["first"]
        self.riftheraldkills = team["objectives"]["riftHerald"]["kills"]
        self.towerfirst = team["objectives"]["tower"]["first"]
        self.towerkills = team["objectives"]["tower"]["kills"]
        self.inhibfirst = team["objectives"]["inhibitor"]["first"]
        self.inhibkills = team["objectives"]["inhibitor"]["kills"]