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

@app.get("/players/{puuid}", response_model=PlayerSchema)
def get_player(puuid: str, db: session = Depends(get_db)):
    player = db.query(PLAYER).filter(PLAYER.puuid == puuid).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player is not found")
    
    return player

@app.get("/match/{matchid}", response_model=MatchSchema)
def get_match(matchid: str, db: session = Depends(get_db)):
    match = db.query(MATCH).filter(MATCH.matchid == matchid).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match is not found")
    
    return match

