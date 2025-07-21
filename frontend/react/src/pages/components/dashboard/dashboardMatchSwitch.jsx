import { useState } from "react";
import DashboardTcMatches from "./dachboardTcMatches";
//import "./dashboardMatchSwitch.css"

const MatchSwitch = ({ content }) => {
    const [index, setIndex] = useState(0);
    const matches = content.tc_Matches

    const nextMatch = () => {
        if (index < matches.length - 1) setIndex((oldIndex) => oldIndex + 1);
    };

    const prevMatch = () => {
        if (index > 0) setIndex((oldIndex) => oldIndex - 1);
    };

    const currentMatch = matches[index] 

    if (!matches || matches.length === 0){
        return(<p>Kein Match gefunden</p>)
    }

    return(
        <section className="MatchSwitchContainer">
            <div className="MatchSwitch">

                <DashboardTcMatches {...currentMatch} />

                <div className="MatchSwitchButtons">
                    <button onClick={prevMatch} disabled={index === 0}>←</button>

                    <button onClick={nextMatch} disabled={index === matches.length - 1}>→</button>
                </div>
            </div>
        </section>
    )
} 

export default MatchSwitch