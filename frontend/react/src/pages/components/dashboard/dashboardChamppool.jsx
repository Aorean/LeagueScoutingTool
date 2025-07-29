import { useNavigate } from "react-router-dom"
import { useState } from "react"
import playerdataService from "../../../playerdata"
import GetImage from "../getImage"

import "./css/dashboardChamppool.css"

const DashboardChamppool = ({content}) => {
    const [inputValue, setInputValue] = useState("")
    const navigate = useNavigate()
    const playerData = content.player

    
  const roleIcon = (role) => {
    let roleUrl = ""
    if (role === "TOP") {
        roleUrl = "https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-parties/global/default/icon-position-top-blue.png"
    }
    else if (role === "JUNGLE") {
        roleUrl = "https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-parties/global/default/icon-position-jungle-blue.png"
    }
    else if (role === "MIDDLE") {
        roleUrl = "https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-parties/global/default/icon-position-middle-blue.png"
    }
    else if (role === "BOTTOM") {
        roleUrl = "https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-parties/global/default/icon-position-bottom-blue.png"
    }
    else if (role === "UTILITY") {
        roleUrl = "https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-parties/global/default/icon-position-utility-blue.png"
    }

    return (roleUrl)
  }


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
        <section className="DashboardChamppool-Container">
            <h2>Champpool</h2>
            <div className="DashboardChamppool"> 
                {playerData.map((accountData, index) => (
                    <table className="DashboardChamppool-Table" key={index}>
                        <caption>{accountData.account.gamertag}#{accountData.account.tagline}</caption>
                        <thead>
                            <tr>
                            <th>Champ</th>
                            <th>K/D/A</th>
                            <th>Games played</th>
                            <th>Winrate</th>
                            <th>Role</th>
                            </tr>
                        </thead>
                        <tbody>
                            {accountData.champpool.map((champpool, index) => {
                                const UrlChamp = champpool.champ.replace(" ", "").toLowerCase()
                                return(
                                <tr key={index}>
                                    <td>
                                        <GetImage 
                                            source={[
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChamp}/skins/base/images/${UrlChamp}_splash_tile_0.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChamp}/skins/base/images/${UrlChamp}_splash_tile_0.${UrlChamp}_rework.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChamp}/skins/base/images/${UrlChamp}_splash_tile_0.${UrlChamp}vgu.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChamp}/skins/base/images/${UrlChamp}_splash_tile_0.domina.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChamp}/skins/base/images/${UrlChamp}_splash_tile_0.${UrlChamp}.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChamp}/skins/skin0/images/${UrlChamp}_splash_tile_0.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChamp}/skins/skin0/images/${UrlChamp}_splash_tile_0.${UrlChamp}_rework.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChamp}/skins/skin0/images/${UrlChamp}_splash_tile_0.${UrlChamp}vgu.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChamp}/skins/skin0/images/${UrlChamp}_splash_tile_0.domina.jpg`,
                                                `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${UrlChamp}/skins/skin0/images/${UrlChamp}_splash_tile_0.${UrlChamp}.jpg`,
                                            ]}  
                                            alt={champpool.champ}
                                            className="Icon"
                                        />
                                    </td>
                                    <td>{champpool.kda}</td>
                                    <td>{champpool.games_played}</td>
                                    <td>{champpool.winrate}</td>
                                    <td>
                                        <img className="RoleIcon" 
                                        crossOrigin="anonymous"
                                        referrerPolicy="no-referrer"
                                        src={roleIcon(champpool.fav_role)}
                                        alt={champpool.fav_role} />
                                    </td>
                            </tr>
                            )})}
                        </tbody>
                    </table>
                ))}
                
            </div>
            <button onClick={() => handleMore({path: "champpool"})}>More...</button>
        </section>
    );
}

export default DashboardChamppool;