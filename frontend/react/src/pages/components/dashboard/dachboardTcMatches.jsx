import cDragonRequestIcon from "../../../playerdata"
//import "./css/dashboardTcMatches.css"

const DashboardTcMatches = (props) => {
    const blueTeam = props.participants.filter((participant, index) => {
        return participant.team === 100});
    const redTeam = props.participants.filter((participant, index) => {
        return participant.team === 200});

    const min = Math.floor(props.gameDuration / 60)
    const sec = Math.floor(props.gameDuration % 60)

    const roleOrder = [
        "TOP",
        "JUNGLE",
        "MIDDLE",
        "BOTTOM",
        "UTILITY"
    ]
 
    const blueTeamSorted = roleOrder.map((role) => {
        return blueTeam.find((player, index) => {return player.role === role});
    });
    const redTeamSorted = roleOrder.map((role) => {
        return redTeam.find((player, index) => {return player.role === role});
    });


    return(
        <div className="tc-panel">
            <h3>
                {props.matchId}
            </h3>
            <p>
                {min}:{sec}
            </p>
            <table className="table">
                <thead>
                    <tr>
                        <th>Blueside</th>
                        <th>Redside</th>
                    </tr>
                </thead>
                    <tbody>
                        {blueTeamSorted.map((playerBlueSide, index) => {
                            const playerRedSide = redTeamSorted[index];
                            return (
                            <tr key={index} className="tableInfo">

                                    <td style={{
                                        backgroundColor: playerBlueSide.win === true ? 'rgba(0, 89, 255, 0.22)' : 'rgba(255, 68, 0, 0.2)',
                                    }}>

                                         {playerBlueSide.gamertag}#{playerBlueSide.tagline} - | {playerBlueSide.kills} / {playerBlueSide.deaths} / {playerBlueSide.assists} | {playerBlueSide.cs} 

                                        <img className="Icon" 
                                        crossOrigin="anonymous"
                                        referrerPolicy="no-referrer"
                                        src={`https://raw.communitydragon.org/${playerBlueSide.patch}/plugins/rcp-be-lol-game-data/global/default/assets/characters/${playerBlueSide.champ.toLowerCase()}/skins/base/images/${playerBlueSide.champ.toLowerCase()}_splash_tile_0.jpg`}
                                        alt={playerBlueSide.champ}
                                        /> 
                                    </td>
                                    <td style={{
                                        backgroundColor: playerRedSide.win === true ? 'rgba(0, 89, 255, 0.22)' : 'rgba(255, 68, 0, 0.2)'
                                    }}>
                                        <img className="Icon" 
                                        crossOrigin="anonymous"
                                        referrerPolicy="no-referrer"
                                        src={`https://raw.communitydragon.org/${playerRedSide.patch}/plugins/rcp-be-lol-game-data/global/default/assets/characters/${playerRedSide.champ.toLowerCase()}/skins/base/images/${playerRedSide.champ.toLowerCase()}_splash_tile_0.jpg`}
                                        alt={playerRedSide.champ}
                                        /> 
                                         {playerRedSide.gamertag}#{playerRedSide.tagline} - | {playerRedSide.kills} / {playerRedSide.deaths} / {playerRedSide.assists} | {playerRedSide.cs}
                                    </td>
                            </tr>
                            
                            );
                            })}
                    </tbody>
            </table>
        </div>
    )
}

export default DashboardTcMatches
