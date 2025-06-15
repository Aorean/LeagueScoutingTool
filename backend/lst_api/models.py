from pydantic import BaseModel
from pydantic.config import ConfigDict

class PlayerSchema(BaseModel):
    puuid: str
    gamertag: str
    tagline: str

    model_config = ConfigDict(from_attributes=True)

    
class MatchSchema(BaseModel):
    PUUID_MATCHID : str
    puuid : str
    matchid : str
    participants : str
    gamestart : str
    gameend : str
    gameduration : str
    tournamentcode : str
    gamemode : int
    season : str
    patch : str
    mapid  : int
    earlysurrender_blue : bool
    earlysurrender_red : bool
    earlysurrender : bool

    model_config = ConfigDict(from_attributes=True)

class PlayerstatsSchema(BaseModel):
    PUUID_MATCHID : str
    puuid : str
    matchid : str
    gamertag : str
    tagline : str
    team : int
    champ : str
    role : str
    kills : int
    deaths : int
    assists : int
    cs : int
    level : int
    exp : int
    gold : int
    visionscore : int
    summonerspell1 : str
    summonerspell2 : str
    item1 : str
    item2 : str
    item3 : str
    item4 : str
    item5 : str
    item6 : str
    keyrune : str
    win : bool
    season : str
    patch : str 
    mapid : int
    gamemode : int

    class Config:
        orm_mode = True

class ObjectivesSchema(BaseModel):
    MATCHID_TEAMID : str
    matchid : str
    teamid : int
    baronfirst : bool
    baronkills : int
    atakhanfirst : bool
    atakhankills : int
    grubsfirst : bool
    grubskills : int
    dragonfirst : bool
    dragonkills : int
    riftheraldfirst : bool
    riftheraldkills : int
    towerfirst : bool
    towerkills : int
    inhibfirst : bool
    inhibkills : int

    class Config:
        orm_mode = True

class ChamppoolSchema(BaseModel):
    PUUID_CHAMP_SEASON : str

    puuid : str
    champ : str

    name : str
    tagline : str

    games_played : int

    kda : float
    kills : float
    deaths : float
    assists : float
    cs : float
    exp : float
    level : float
    gold : float
    visionscore : float

    cs_diff : float
    exp_diff : float
    level_diff : float
    gold_diff : float
    visionscore_diff : float

    summonerspell1 : str
    summonerspell2 : str

    fav_role : str

    winrate : float
    win_blue : float
    win_red : float

    season : int

    class Config:
        orm_mode = True

class PlayerinfoSchema(BaseModel):
    puuid : str
    summonerlevel : int
    profile_icon : int
    division : str
    rank : str
    wins_total : int
    losses_total : int
    stuck : bool

    class Config:
        orm_mode = True
