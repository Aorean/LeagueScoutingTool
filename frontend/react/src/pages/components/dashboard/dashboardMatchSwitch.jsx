import { useState } from "react";
import DashboardTcMatches from "./dachboardTcMatches";
import playerdataService from "../../../playerdata"

import { useNavigate } from "react-router-dom"
//import "./dashboardMatchSwitch.css"

const MatchSwitch = ({ content }) => {
    const [index, setIndex] = useState(0);
    const matches = content.tc_Matches
    const navigate = useNavigate()
    
    const nextMatch = () => {
        if (index < matches.length - 1) setIndex((oldIndex) => oldIndex + 1);
    };

    const prevMatch = () => {
        if (index > 0) setIndex((oldIndex) => oldIndex - 1);
    };

    const currentMatch = matches[index] 


    const handleMore = ({path}) => {
        // "push" to append to a list
        let puuids = []
        playerData.map((player, index) => {
            puuids.push(player.account.puuid)
        })
        //post to api, return detailed Champpool JSON
        playerdataService.postMore({path:path, puuids:puuids}).then((returnedData) => {
            const returnedBody = returnedData.Body;
        
            
            navigate(`/${path}`, {state: {returnedBody}})
        })
        console.log(puuids)
        }





    if (!matches || matches.length === 0){
        return(<p>Kein Match gefunden</p>)
    }





    return(
        <section className="MatchSwitchContainer">
            <h2>Tournamentcode Matches</h2>
            <div className="MatchSwitch">

                <DashboardTcMatches {...currentMatch} />

                <div className="MatchSwitchButtons">
                    <button onClick={prevMatch} disabled={index === 0}>←</button>

                    <button onClick={nextMatch} disabled={index === matches.length - 1}>→</button>
                </div>
            </div>
            <button onClick={() => handleMore({path: "tc-matches"})}>More...</button>
        </section>
    )
} 

export default MatchSwitch