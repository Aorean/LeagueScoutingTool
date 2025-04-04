class Player:
    def __init__(self, puuid, gamertag, tagline):
        self.puuid = puuid
        self.gamertag = gamertag
        self.tagline = tagline
        self.kda = 0

    def set_kda(self, number):
        self.kda = number

