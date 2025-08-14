import cDragonRequestIcon from "../../../playerdata"
import "./css/dashboardTcMatches.css"
import GetImage from "../getImage";

const DashboardTcMatches = (props) => {
    const blueTeam = props.participants.filter((participant, index) => {
        return participant.team === 100});
    const redTeam = props.participants.filter((participant, index) => {
        return participant.team === 200});
    console.log(props)
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
            <table className="DashboardTcMatches-Table">
                <thead>
                    <tr>
                        <th>Blueside</th>
                        <th>Redside</th>
                    </tr>
                </thead>
                    <tbody>
                        {blueTeamSorted.map((playerBlueSide, index) => {
                            const playerRedSide = redTeamSorted[index];
                            const UrlChampBlue = playerBlueSide.champ.replace(" ", "").toLowerCase()
                            const UrlChampRed = playerRedSide.champ.replace(" ", "").toLowerCase()

                            return (
                            <tr key={index} >

                                    <td style={{
                                        backgroundColor: playerBlueSide.win === true ? 'rgba(0, 89, 255, 0.22)' : 'rgba(255, 68, 0, 0.2)'
                                        
                                    }}
                                    className="DashboardBlueside">

                                         {playerBlueSide.gamertag}#{playerBlueSide.tagline} - | {playerBlueSide.kills} / {playerBlueSide.deaths} / {playerBlueSide.assists} | {playerBlueSide.cs} 
                                          
                                        <GetImage 
                                            source={[
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampBlue}/skins/base/images/${UrlChampBlue}_splash_tile_0.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampBlue}/skins/base/images/${UrlChampBlue}_splash_tile_0.${UrlChampBlue}_rework.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampBlue}/skins/base/images/${UrlChampBlue}_splash_tile_0.${UrlChampBlue}vgu.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampBlue}/skins/base/images/${UrlChampBlue}_splash_tile_0.domina.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampBlue}/skins/base/images/${UrlChampBlue}_splash_tile_0.${UrlChampBlue}.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampBlue}/skins/skin0/images/${UrlChampBlue}_splash_tile_0.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampBlue}/skins/skin0/images/${UrlChampBlue}_splash_tile_0.${UrlChampBlue}_rework.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampBlue}/skins/skin0/images/${UrlChampBlue}_splash_tile_0.${UrlChampBlue}vgu.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampBlue}/skins/skin0/images/${UrlChampBlue}_splash_tile_0.domina.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampBlue}/skins/skin0/images/${UrlChampBlue}_splash_tile_0.${UrlChampBlue}.jpg`,
                                            ]}  
                                            alt={playerBlueSide.champ}
                                            className="Icon"
                                        />

                                    </td>
                                    <td style={{
                                        backgroundColor: playerRedSide.win === true ? 'rgba(0, 89, 255, 0.22)' : 'rgba(255, 68, 0, 0.2)'

                                    }}
                                    className="DashboardRedside">
                                        <GetImage 
                                            source={[
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampRed}/skins/base/images/${UrlChampRed}_splash_tile_0.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampRed}/skins/base/images/${UrlChampRed}_splash_tile_0.${UrlChampRed}_rework.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampRed}/skins/base/images/${UrlChampRed}_splash_tile_0.${UrlChampRed}vgu.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampRed}/skins/base/images/${UrlChampRed}_splash_tile_0.domina.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampRed}/skins/base/images/${UrlChampRed}_splash_tile_0.${UrlChampRed}.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampRed}/skins/skin0/images/${UrlChampRed}_splash_tile_0.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampRed}/skins/skin0/images/${UrlChampRed}_splash_tile_0.${UrlChampRed}_rework.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampRed}/skins/skin0/images/${UrlChampRed}_splash_tile_0.${UrlChampRed}vgu.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampRed}/skins/skin0/images/${UrlChampRed}_splash_tile_0.domina.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChampRed}/skins/skin0/images/${UrlChampRed}_splash_tile_0.${UrlChampRed}.jpg`,
                                            ]}  
                                            alt={playerRedSide.champ}
                                            className="Icon"
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
