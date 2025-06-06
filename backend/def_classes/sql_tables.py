from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ARRAY
from backend.db_base import Base



#Table for Player (=PLAYER)
class PLAYER(Base):
    __table_args__ = {"schema": "playerdata"}
    __tablename__ = "player"

    puuid = Column(String, primary_key=True, index=True)
    gamertag = Column(String, nullable=False)
    tagline = Column(String, nullable=False)

    @classmethod
    def from_player(cls, player):
        return cls(
            __table_args__= {"schema": "playerdata"},
            __tablename__= "player",

            puuid=player.puuid,
            gamertag=player.gamertag,
            tagline=player.tagline
        )


#Table for Match (=MATCH)
class MATCH(Base):
    __table_args__ = {"schema": "playerdata"}
    __tablename__ = "match"

    PUUID_MATCHID = Column(String, primary_key=True, index=True)
    puuid = Column(String, nullable=False)
    matchid = Column(String, nullable=False)
    participants = Column(String, nullable=False)
    gamestart = Column(String, nullable=False)
    gameend = Column(String, nullable=False)
    gameduration = Column(String, nullable=False)
    tournamentcode = Column(String, nullable=True)
    gamemode = Column(Integer, nullable=False)
    season = Column(String, nullable=False)
    patch = Column(String, nullable=False)
    mapid = Column(Integer, nullable=False)
    earlysurrender_blue = Column(Boolean, nullable=False)
    earlysurrender_red = Column(Boolean, nullable=False)
    earlysurrender = Column(Boolean, nullable=False)


    @classmethod
    def from_match(cls, match):

        tc = "NULL"
        if match.tournamentcode != "":
            tc = match.tournamentcode

        return cls(
            __table_args__={"schema": "playerdata"},
            __tablename__="match",


            PUUID_MATCHID=match.PUUID_MATCHID,
            puuid=match.puuid,
            matchid=match.matchid,
            participants=match.participants,
            gamestart=match.gamestart,
            gameend=match.gameend,
            gameduration=match.gameduration,
            tournamentcode=tc,
            gamemode=match.gamemode,
            season=match.season,
            patch=match.patch,
            mapid=match.mapid,
            earlysurrender_blue=match.earlysurrender_blue,
            earlysurrender_red=match.earlysurrender_red,
            earlysurrender=match.earlysurrender
        )

#Table for Playerstats (=PLAYERSTATS)
class PLAYERSTATS(Base):
    __table_args__ = {"schema": "playerdata"}
    __tablename__ = "playerstats"


    PUUID_MATCHID = Column(String, primary_key=True, index=True)
    puuid = Column(String, nullable=False)
    matchid = Column(String, nullable=False)
    gamertag = Column(String, nullable=False)
    tagline = Column(String, nullable=False)
    team = Column(Integer, nullable=False)
    champ = Column(String, nullable=False)
    role = Column(String, nullable=True)
    kills = Column(Integer, nullable=False)
    deaths = Column(Integer, nullable=False)
    assists = Column(Integer, nullable=False)
    cs = Column(Integer, nullable=True)
    level = Column(Integer, nullable=False)
    exp = Column(Integer, nullable=False)
    gold = Column(Integer, nullable=False)
    visionscore = Column(Integer, nullable=True)
    summonerspell1 = Column(String, nullable=False)
    summonerspell2 = Column(String, nullable=False)
    item1 = Column(String, nullable=False)
    item2 = Column(String, nullable=False)
    item3 = Column(String, nullable=False)
    item4 = Column(String, nullable=False)
    item5 = Column(String, nullable=False)
    item6 = Column(String, nullable=False)
    keyrune = Column(String, nullable=True)
    win = Column(Boolean, nullable=False)
    season = Column(String, nullable=False)
    patch = Column(String, nullable=False)
    mapid = Column(Integer, nullable=False)
    gamemode = Column(Integer, nullable=False)

    @classmethod
    def from_playerstats(cls, playerstats):
        defeat = "FALSE"
        victory = "TRUE"

        if playerstats.win:
            playerstats.win = victory
        elif not playerstats.win:
            playerstats.win = defeat


        return cls(
        __table_args__={"schema": "playerdata"},
        __tablename__="playerstats",


        PUUID_MATCHID=playerstats.PUUID_MATCHID,
        puuid=playerstats.puuid,
        matchid=playerstats.matchid,
        gamertag=playerstats.gamertag,
        tagline=playerstats.tagline,
        team=playerstats.team,
        champ=playerstats.champ,
        role=playerstats.role,
        kills=playerstats.kills,
        deaths=playerstats.deaths,
        assists=playerstats.assists,
        cs=playerstats.cs,
        level=playerstats.level,
        exp=playerstats.exp,
        gold=playerstats.gold,
        visionscore=playerstats.visionscore,
        summonerspell1=playerstats.summonerspell1,
        summonerspell2=playerstats.summonerspell2,
        item1=playerstats.item1,
        item2=playerstats.item2,
        item3=playerstats.item3,
        item4=playerstats.item4,
        item5=playerstats.item5,
        item6=playerstats.item6,
        keyrune=playerstats.keyrune,
        win=playerstats.win,
        season=playerstats.season,
        patch=playerstats.patch,
        mapid=playerstats.mapid,
        gamemode=playerstats.gamemode
        )

class OBJECTIVES(Base):
    __table_args__ = {"schema": "playerdata"}
    __tablename__ = "objectives"

    MATCHID_TEAMID = Column(String, primary_key=True, index=True)
    matchid = Column(String, nullable=False)
    teamid = Column(Integer, nullable=False)
    baronfirst = Column(Boolean, nullable=False)
    baronkills = Column(Integer, nullable=False)
    atakhanfirst = Column(Boolean, nullable=False)
    atakhankills = Column(Integer, nullable=False)
    grubsfirst = Column(Boolean, nullable=False)
    grubskills = Column(Integer, nullable=False)
    dragonfirst = Column(Boolean, nullable=False)
    dragonkills = Column(Integer, nullable=False)
    riftheraldfirst = Column(Boolean, nullable=False)
    riftheraldkills = Column(Integer, nullable=False)
    towerfirst = Column(Boolean, nullable=False)
    towerkills = Column(Integer, nullable=False)
    inhibfirst = Column(Boolean, nullable=False)
    inhibkills = Column(Integer, nullable=False)

    @classmethod
    def from_objectives(cls, objectives):

        not_first = "FALSE"
        first = "TRUE"

        if objectives.baronfirst:
            objectives.baronfirst = first
        elif not objectives.baronfirst:
            objectives.baronfirst = not_first

        if objectives.atakhanfirst:
            objectives.atakhanfirst = first
        elif not objectives.atakhanfirst:
            objectives.atakhanfirst = not_first

        if objectives.grubsfirst:
            objectives.grubsfirst = first
        elif not objectives.grubsfirst:
            objectives.grubsfirst = not_first

        if objectives.dragonfirst:
            objectives.dragonfirst = first
        elif not objectives.dragonfirst:
            objectives.dragonfirst = not_first

        if objectives.riftheraldfirst:
            objectives.riftheraldfirst = first
        elif not objectives.riftheraldfirst:
            objectives.riftheraldfirst = not_first

        if objectives.towerfirst:
            objectives.towerfirst = first
        elif not objectives.towerfirst:
            objectives.towerfirst = not_first

        if objectives.inhibfirst:
            objectives.inhibfirst = first
        elif not objectives.inhibfirst:
            objectives.inhibfirst = not_first


        return cls(
            __table_args__={"schema": "playerdata"},
            __tablename__="objectives",

            MATCHID_TEAMID=objectives.MATCHID_TEAMID,
            matchid=objectives.matchid,
            teamid=objectives.teamid,
            baronfirst=objectives.baronfirst,
            baronkills=objectives.baronkills,
            atakhanfirst=objectives.atakhanfirst,
            atakhankills=objectives.atakhankills,
            grubsfirst=objectives.grubsfirst,
            grubskills=objectives.grubskills,
            dragonfirst=objectives.dragonfirst,
            dragonkills=objectives.dragonkills,
            riftheraldfirst=objectives.riftheraldfirst,
            riftheraldkills=objectives.riftheraldkills,
            towerfirst=objectives.towerfirst,
            towerkills=objectives.towerkills,
            inhibfirst=objectives.inhibfirst,
            inhibkills=objectives.inhibkills,
        )

class CHAMPPOOL(Base):
    __table_args__ = {"schema": "playerdata"}
    __tablename__ = "champpool"


    PUUID_CHAMP_SEASON = Column(String, primary_key=True, index=True)

    puuid = Column(String, nullable=False)
    champ = Column(String, nullable=False)

    name = Column(String, nullable=False)
    tagline = Column(String, nullable=False)

    games_played = Column(Integer, nullable=False)

    kda = Column(Float, nullable=False)
    kills = Column(Float, nullable=False)
    deaths = Column(Float, nullable=False)
    assists = Column(Float, nullable=False)
    cs = Column(Float, nullable=False)
    exp = Column(Float, nullable=False)
    level = Column(Float, nullable=False)
    gold = Column(Float, nullable=False)
    visionscore = Column(Float, nullable=False)

    cs_diff = Column(Float, nullable=False)
    exp_diff = Column(Float, nullable=False)
    level_diff = Column(Float, nullable=False)
    gold_diff = Column(Float, nullable=False)
    visionscore_diff = Column(Float, nullable=False)

    summonerspell1 = Column(String, nullable=False)
    summonerspell2 = Column(String, nullable=False)

    fav_role = Column(String, nullable=False)

    winrate = Column(Float, nullable=False)
    win_blue = Column(Float, nullable=False)
    win_red = Column(Float, nullable=False)

    season = Column(Integer, nullable=False)

    @classmethod
    def from_champpool(cls, champpool):
        return cls(
            __table_args__= {"schema": "playerdata"},
            __tablename__= "champpool",

            PUUID_CHAMP_SEASON=champpool.PUUID_CHAMP_SEASON,
            puuid=champpool.puuid,
            champ=champpool.champ,
            name=champpool.name,
            tagline=champpool.tagline,
            games_played=champpool.games_played,
            kda=champpool.kda,
            kills=champpool.kills,
            deaths=champpool.deaths,
            assists=champpool.assists,
            cs=champpool.cs,
            exp=champpool.exp,
            level=champpool.level,
            gold=champpool.gold,
            visionscore=champpool.visionscore,
            cs_diff=champpool.cs_diff,
            exp_diff=champpool.exp_diff,
            level_diff=champpool.level_diff,
            gold_diff=champpool.gold_diff,
            visionscore_diff=champpool.visionscore_diff,
            summonerspell1=champpool.summonerspell1,
            summonerspell2=champpool.summonerspell2,
            fav_role=champpool.fav_role,

            winrate=champpool.winrate,
            win_blue=champpool.win_blue,
            win_red=champpool.win_red,
            season=champpool.season
        )

class PLAYERINFO(Base):
    __table_args__ = {"schema": "playerdata"}
    __tablename__ = "playerinfo"

    puuid = Column(String, primary_key=True, index=True)
    summonerlevel = Column(Integer, nullable=False)
    profile_icon = Column(Integer, nullable=False)
    division = Column(String, nullable=False)
    rank = Column(String, nullable=False)
    wins_total = Column(Integer, nullable=False)
    losses_total = Column(Integer, nullable=False)
    stuck = Column(Boolean, nullable=False)

    @classmethod
    def from_playerinfo(cls, playerinfo):
        return cls(            
            __table_args__= {"schema": "playerdata"},
            __tablename__= "playerinfo",

            puuid = playerinfo.puuid,
            summonerlevel = playerinfo.summonerlevel,
            profile_icon = playerinfo.profile_icon,
            division = playerinfo.division,
            rank = playerinfo.rank,
            wins_total = playerinfo.wins_total,
            losses_total = playerinfo.losses_total,
            stuck = playerinfo.stuck
        )

class MATCHHISTORY(Base):
    __table_args__ = {"schema": "playerdata"}
    __tablename__ = "matchhistory"

    PUUID = Column(String, primary_key=True, index=True)
    matchhistory = Column(ARRAY(String), nullable=False)

    @classmethod
    def from_matchhistory(cls, matchhistory):
        return cls(            
            __table_args__= {"schema": "playerdata"},
            __tablename__= "matchhistory",

            PUUID = matchhistory.PUUID,
            matchhistory = matchhistory.matchhistory
        )



"""
##############
#### ARAM ####
##############
class ARAM_MATCH(Base):
    __table_args__ = {"schema": "playerdata"}
    __tablename__ = "aram_match"

    PUUID_MATCHID = Column(String, primary_key=True, index=True)
    puuid = Column(String, nullable=False)
    matchid = Column(String, nullable=False)
    participants = Column(String, nullable=False)
    gamestart = Column(String, nullable=False)
    gameend = Column(String, nullable=False)
    gameduration = Column(String, nullable=False)
    gamemode = Column(String, nullable=False)
    season = Column(String, nullable=False)
    patch = Column(String, nullable=False)


    @classmethod
    def from_match(cls, match):
        return cls(
            __table_args__={"schema": "playerdata"},
            __tablename__="aram_match",

            PUUID_MATCHID=match.PUUID_MATCHID,
            puuid=match.puuid,
            matchid=match.matchid,
            participants=match.participants,
            gamestart=match.gamestart,
            gameend=match.gameend,
            gameduration=match.gameduration,
            gamemode=match.gamemode,
            season=match.season,
            patch=match.patch
        )

class ARAM_PLAYERSTATS(Base):
    __table_args__ = {"schema": "playerdata"}
    __tablename__ = "aram_playerstats"


    PUUID_MATCHID = Column(String, primary_key=True, index=True)
    puuid = Column(String, nullable=False)
    matchid = Column(String, nullable=False)
    gamertag = Column(String, nullable=False)
    tagline = Column(String, nullable=False)
    team = Column(Integer, nullable=False)
    champ = Column(String, nullable=False)
    kills = Column(Integer, nullable=False)
    deaths = Column(Integer, nullable=False)
    assists = Column(Integer, nullable=False)
    cs = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    exp = Column(Integer, nullable=False)
    gold = Column(Integer, nullable=False)
    summonerspell1 = Column(String, nullable=False)
    summonerspell2 = Column(String, nullable=False)
    item1 = Column(String, nullable=False)
    item2 = Column(String, nullable=False)
    item3 = Column(String, nullable=False)
    item4 = Column(String, nullable=False)
    item5 = Column(String, nullable=False)
    item6 = Column(String, nullable=False)
    keyrune = Column(String, nullable=False)
    win = Column(Boolean, nullable=False)
    season = Column(String, nullable=False)
    patch = Column(String, nullable=False)
    @classmethod
    def from_playerstats(cls, playerstats):
        defeat = "FALSE"
        victory = "TRUE"

        if playerstats.win:
            playerstats.win = victory
        elif not playerstats.win:
            playerstats.win = defeat


        return cls(
        __table_args__={"schema": "playerdata"},
        __tablename__="aram_playerstats",


        PUUID_MATCHID=playerstats.PUUID_MATCHID,
        puuid=playerstats.puuid,
        matchid=playerstats.matchid,
        gamertag=playerstats.gamertag,
        tagline=playerstats.tagline,
        team=playerstats.team,
        champ=playerstats.champ,
        kills=playerstats.kills,
        deaths=playerstats.deaths,
        assists=playerstats.assists,
        cs=playerstats.cs,
        level=playerstats.level,
        exp=playerstats.exp,
        gold=playerstats.gold,
        summonerspell1=playerstats.summonerspell1,
        summonerspell2=playerstats.summonerspell2,
        item1=playerstats.item1,
        item2=playerstats.item2,
        item3=playerstats.item3,
        item4=playerstats.item4,
        item5=playerstats.item5,
        item6=playerstats.item6,
        keyrune=playerstats.keyrune,
        win=playerstats.win,
        season=playerstats.season,
        patch=playerstats.patch
        )
    
###############
#### Arena ####
###############
class ARENA_MATCH(Base):
    __table_args__ = {"schema": "playerdata"}
    __tablename__ = "arena_match"

    PUUID_MATCHID = Column(String, primary_key=True, index=True)
    puuid = Column(String, nullable=False)
    matchid = Column(String, nullable=False)
    participants = Column(String, nullable=False)
    gamestart = Column(String, nullable=False)
    gameend = Column(String, nullable=False)
    gameduration = Column(String, nullable=False)
    gamemode = Column(String, nullable=False)
    season = Column(String, nullable=False)
    patch = Column(String, nullable=False)


    @classmethod
    def from_match(cls, match):
        return cls(
            __table_args__={"schema": "playerdata"},
            __tablename__="arena_match",

            PUUID_MATCHID=match.PUUID_MATCHID,
            puuid=match.puuid,
            matchid=match.matchid,
            participants=match.participants,
            gamestart=match.gamestart,
            gameend=match.gameend,
            gameduration=match.gameduration,
            gamemode=match.gamemode,
            season=match.season,
            patch=match.patch
        )

class ARENA_PLAYERSTATS(Base):
    __table_args__ = {"schema": "playerdata"}
    __tablename__ = "arena_playerstats"


    PUUID_MATCHID = Column(String, primary_key=True, index=True)
    puuid = Column(String, nullable=False)
    matchid = Column(String, nullable=False)
    gamertag = Column(String, nullable=False)
    tagline = Column(String, nullable=False)
    team = Column(Integer, nullable=False)
    champ = Column(String, nullable=False)
    kills = Column(Integer, nullable=False)
    deaths = Column(Integer, nullable=False)
    assists = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    exp = Column(Integer, nullable=False)
    gold = Column(Integer, nullable=False)
    summonerspell1 = Column(String, nullable=False)
    summonerspell2 = Column(String, nullable=False)
    item1 = Column(String, nullable=False)
    item2 = Column(String, nullable=False)
    item3 = Column(String, nullable=False)
    item4 = Column(String, nullable=False)
    item5 = Column(String, nullable=False)
    item6 = Column(String, nullable=False)
    keyrune = Column(String, nullable=False)
    win = Column(Boolean, nullable=False)
    season = Column(String, nullable=False)
    patch = Column(String, nullable=False)
    @classmethod
    def from_playerstats(cls, playerstats):
        defeat = "FALSE"
        victory = "TRUE"

        if playerstats.win:
            playerstats.win = victory
        elif not playerstats.win:
            playerstats.win = defeat


        return cls(
        __table_args__={"schema": "playerdata"},
        __tablename__="arena_playerstats",


        PUUID_MATCHID=playerstats.PUUID_MATCHID,
        puuid=playerstats.puuid,
        matchid=playerstats.matchid,
        gamertag=playerstats.gamertag,
        tagline=playerstats.tagline,
        team=playerstats.team,
        champ=playerstats.champ,
        kills=playerstats.kills,
        deaths=playerstats.deaths,
        assists=playerstats.assists,
        level=playerstats.level,
        exp=playerstats.exp,
        gold=playerstats.gold,
        summonerspell1=playerstats.summonerspell1,
        summonerspell2=playerstats.summonerspell2,
        item1=playerstats.item1,
        item2=playerstats.item2,
        item3=playerstats.item3,
        item4=playerstats.item4,
        item5=playerstats.item5,
        item6=playerstats.item6,
        keyrune=playerstats.keyrune,
        win=playerstats.win,
        season=playerstats.season,
        patch=playerstats.patch
        )
"""