import "./css/dashboardPlayer.css"
import playerdataService from "../../../playerdata"
import { useState } from "react"
import { useNavigate } from "react-router-dom"

const DashboardPlayer = ({content}) => {
    const playerData = content.player
    const navigate = useNavigate()

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


    return (
        <section className="DashboardPlayer-Container">
            <h2>Player</h2>
            <div className="DashboardPlayer">
                <table>
                    <thead>
                        <tr>
                        <th>Name</th>
                        <th>Elo</th>
                        <th>Winrate</th>
                        </tr>
                    </thead>
                    <tbody>
                        
                        {playerData.map((accountData, index) => (
                            
                            <tr key={index}>
                                <td>{accountData.account.gamertag}#{accountData.account.tagline}</td>
                                <td>{accountData.account.division} {accountData.account.rank}
                                    <img className="RankIcon" 
                                    crossOrigin="anonymous"
                                    referrerPolicy="no-referrer"
                                    src={`https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-static-assets/global/default/ranked-emblem/emblem-${accountData.account.division.toLowerCase()}.png`}
                                    alt={accountData.account.division}
                                    /> 
                                </td>
                                <td>{accountData.account.winrate}</td>
                            </tr>
                            ))}

                    </tbody>
                </table>
            </div>
            <button onClick={() => handleMore({path: "player"})}>More...</button>
        </section>
    );
}

export default DashboardPlayer;