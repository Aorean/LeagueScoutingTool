import "./css/dashboardMastery.css"
import GetImage from "../getImage"
import playerdataService from "../../../playerdata"
import { useNavigate } from "react-router-dom"



const DashboardMastery = ({content}) => {
    const navigate = useNavigate()
    const playerData = content.player
 
    const masteryPng = (masteryLevel) => {
        let level = 0
        if (masteryLevel > 10) {
            level = 10
        }
        else {
            level = masteryLevel
        }
        
        const baseUrl = `https://raw.communitydragon.org/latest/game/assets/ux/mastery/legendarychampionmastery/masterycrest_level${level}.cm_updates.png`
        return(baseUrl)
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
        <section className="DashboardMastery-Container">
            <h2>Mastery</h2>
            <div className="DashboardMastery"> 
                    {playerData.map((accountData, index) => (
                        <table className="DashboardMastery-Table" key={index}>
                            <caption>{accountData.account.gamertag}#{accountData.account.tagline}</caption>
                            <thead>
                                <tr>
                                <th>Champ</th>
                                <th>Masterypoints</th>
                                <th>Masterylevel</th>
                                </tr>
                            </thead>
                            <tbody>
                                {accountData.mastery.map((champMastery, index) => {
                                    const UrlChamp = champMastery.champ.replace(" ", "").toLowerCase()
                                    
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
                                                alt={champMastery.champ}
                                                className="Icon"
                                            />
                                        </td>
                                        <td>{champMastery.masterypoints}</td>
                                        <td>
                                            {champMastery.masterylevel}
                                            <img className="MasteryIcon" 
                                            crossOrigin="anonymous"
                                            referrerPolicy="no-referrer"
                                            src={masteryPng(champMastery.masterylevel)}
                                            alt={champMastery.masterylevel}
                                            /> 
                                        </td>
                                </tr>
                                )})}
                            </tbody>
                        </table>
                        
                    ))}
                
            </div>
            <button onClick={() => handleMore({path: "mastery"})}>More...</button>
        </section>
    );
}

export default DashboardMastery;