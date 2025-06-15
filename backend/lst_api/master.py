from fastapi import FastAPI, Depends, HTTPException
from backend.lst_api.models import *
from sqlalchemy.orm import session, sessionmaker
from backend.config import db_engine
from backend.def_classes.sql_tables import *

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def read_root():
    return {"players" : "http://127.0.0.1:8000/players",
            "match" : "http://127.0.0.1:8000/match",
            "playerstats" : "http://127.0.0.1:8000/playerstats",
            "objectives" : "http://127.0.0.1:8000/objectives",
            "champpool" : "http://127.0.0.1:8000/champpool"
            }

@app.get("/players/", response_model=list[PlayerSchema])
def get_all_player(db: session = Depends(get_db)):
    players = db.query(PLAYER).all()
    if not players:
        raise HTTPException(status_code=404, detail="Players is not found")

    return players

@app.get("/players/{puuid}", response_model=PlayerSchema)
def get_player(puuid: str, db: session = Depends(get_db)):
    player = db.query(PLAYER).filter(PLAYER.puuid == puuid).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player is not found")
    
    return player



@app.get("/matches/", response_model=list[MatchSchema])
def get_all_matches(db: session = Depends(get_db)):
    matches = db.query(MATCH).all()
    if not matches:
        raise HTTPException(status_code=404, detail="Matches is not found")

    return matches

@app.get("/matches/{matchid}", response_model=MatchSchema)
def get_match(matchid: str, db: session = Depends(get_db)):
    match = db.query(MATCH).filter(MATCH.matchid == matchid).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match is not found")
    
    return match



@app.get("/playerstats/", response_model=list[PlayerstatsSchema])
def get_all_playerstats(db: session = Depends(get_db)):
    playerstats = db.query(PLAYERSTATS).all()
    if not playerstats:
        raise HTTPException(status_code=404, detail="Matches is not found")

    return playerstats

@app.get("/playerstats/{PUUID_MATCHID}", response_model=PlayerstatsSchema)
def get_playerstats(PUUID_MATCHID: str, db: session = Depends(get_db)):
    playerstats = db.query(PLAYERSTATS).filter(PLAYERSTATS.PUUID_MATCHID == PUUID_MATCHID).first()
    if not playerstats:
        raise HTTPException(status_code=404, detail="Playerstats is not found")
    
    return playerstats



@app.get("/objectives/", response_model=list[ObjectivesSchema])
def get_all_playerstats(db: session = Depends(get_db)):
    objectives = db.query(OBJECTIVES).all()
    if not objectives:
        raise HTTPException(status_code=404, detail="Matches is not found")

    return objectives

@app.get("/objectives/{PUUID_CHAMP}", response_model=ObjectivesSchema)
def get_playerstats(MATCHID_TEAMID: str, db: session = Depends(get_db)):
    objectives = db.query(OBJECTIVES).filter(OBJECTIVES.MATCHID_TEAMID == MATCHID_TEAMID).first()
    if not objectives:
        raise HTTPException(status_code=404, detail="Match is not found")
    
    return objectives



@app.get("/champpools/", response_model=list[ChamppoolSchema])
def get_all_playerstats(db: session = Depends(get_db)):
    champpools = db.query(CHAMPPOOL).all()
    if not champpools:
        raise HTTPException(status_code=404, detail="Matches is not found")

    return champpools


@app.get("/champpools/{PUUID_CHAMP_SEASON}", response_model=ChamppoolSchema)
def get_playerstats(PUUID_CHAMP_SEASON: str, db: session = Depends(get_db)):
    champpool = db.query(CHAMPPOOL).filter(CHAMPPOOL.PUUID_CHAMP_SEASON == PUUID_CHAMP_SEASON).first()
    if not champpool:
        raise HTTPException(status_code=404, detail="Match is not found")
    
    return champpool

@app.get("/champpools/by_puuid/{puuid}", response_model=list[ChamppoolSchema])
def get_playerstats(puuid: str, db: session = Depends(get_db)):
    champpools = db.query(CHAMPPOOL).filter(CHAMPPOOL.puuid == puuid).all()
    if not champpools:
        raise HTTPException(status_code=404, detail="Match is not found")
    
    return champpools



@app.get("/playerinfos/", response_model=list[PlayerinfoSchema])
def get_all_playerstats(db: session = Depends(get_db)):
    playerinfos = db.query(PLAYERINFO).all()
    if not playerinfos:
        raise HTTPException(status_code=404, detail="Matches is not found")

    return playerinfos


@app.get("/playerinfos/{puuid}", response_model=PlayerinfoSchema)
def get_playerstats(puuid: str, db: session = Depends(get_db)):
    playerinfo = db.query(PLAYERINFO).filter(PLAYERINFO.puuid == puuid).first()
    if not playerinfo:
        raise HTTPException(status_code=404, detail="Match is not found")
    
    return playerinfo