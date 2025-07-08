import cDragonRequestIcon from "../../playerdata"


const DashboardTcMatches = (props) => {
    let blueTeam = props.participants.filter((participant, index) => {
        return participant.team === 100});
    let redTeam = props.participants.filter((participant, index) => {
        return participant.team === 200});

    const roleOrder = [
        "TOP",
        "JUNGLE",
        "MIDDLE",
        "BOTTOM",
        "UTILITY"
    ]

    let blueTeamSorted = roleOrder.map((role) => {
        return blueTeam.find((player, index) => {return player.role === role});
    });
    let redTeamSorted = roleOrder.map((role) => {
        return redTeam.find((player, index) => {return player.role === role});
    });

    console.log(redTeamSorted)
    return(
        <div className="tc-panel">
            <h3>
                {props.matchId}
            </h3>
            <p>
                {props.gameDuration}
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

                                    <td>

                                         {playerBlueSide.gamertag}#{playerBlueSide.tagline} - | {playerBlueSide.kills} / {playerBlueSide.deaths} / {playerBlueSide.assists} | {playerBlueSide.cs}
                                        <img className="Icon" 
                                        crossOrigin="anonymous"
                                        referrerPolicy="no-referrer"
                                        src={`https://raw.communitydragon.org/${playerBlueSide.patch}/plugins/rcp-be-lol-game-data/global/default/assets/characters/${playerBlueSide.champ.toLowerCase()}/skins/base/images/${playerBlueSide.champ.toLowerCase()}_splash_tile_0.jpg`}
                                        alt={playerBlueSide.champ}
                                        /> 
                                    </td>
                                    <td>
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
