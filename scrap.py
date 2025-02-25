from new import player_scouting


class test:
    def __init__(self, puuid):
        self.puuid = player_scouting["puuid"]
        self.Gamertag = player_scouting["gamertag"]

for puuid in puuids:
    matchistory = test(puuid)


# Lesson Thomas

class Fraction:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def multiply(self, other):
        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator

        return Fraction(numerator, denominator)

    def __mul__(self, other):
        return self.multiply(other)

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

first = Fraction(1, 2)
second = Fraction(1, 3)
third = first.multiply(second) # Fraction(1, 6)
third = first * second
print(third) # 1/6




class Champ:
    def __init__(self, name, games, kills, deaths, assists):
        self.name = name
        self.games = games
        self.kills = kills
        self.deaths = deaths
        self.assists = assists

    def get_kda(self):
        return self.kills + self.assists / self.deaths

class Player:
    def __init__(self, puuid, gamertag, champs: List[Champ]):
        self.puuid = puuid
        self.gamertag = gamertag
        self.champs = champs

    def get_matches(self):
        # api: get matches for player with puuid
        return fetch_result

    def get_all_champ_kdas(self):
        for champ in self.champs:
            kda = champ.get_kda()


l = []
for (puuid, tag) in [("abc", "Aorean#1311"), ("def", "witcher#1311")]:
    player = Player(puuid, tag)
    l.append(player)

# len(l) == 2

aorean = Player("abc", "Aorean#1311")
# aorean = { "puuid": "abc", "gamertag: "Aorean#1311" }
witcher = Player("def", "witcher#1311")

print(f"{aorean.get_matches()[0]}")