import GetImage from "../getImage"


const ChamppoolTableData = ({player}) => {

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


    return(
        <>
        {player.map((playerChamppool, champpoolIndex)=> {
            const UrlChamp = playerChamppool.champ.replace(" ", "").toLowerCase()
            let summoner1 = ""
            let summoner2 = ""
            if (playerChamppool.summonerspell1 === "Ghost") {
                summoner1 = "Haste"
            }
            else {
                summoner1 = playerChamppool.summonerspell1
            }
            if (playerChamppool.summonerspell2 === "Ghost") {
                summoner2 = "Haste"
            }
            else {
                summoner2 = playerChamppool.summonerspell2
            }


            return(
            <tr key={champpoolIndex}> 
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
                        alt={playerChamppool.champ}
                        className="Icon"
                    />
                </td>
                <td>{playerChamppool.games_played}</td>
                <td>{playerChamppool.winrate}</td>
                <td>{playerChamppool.kda}</td>
                <td>{playerChamppool.kills}</td> 
                <td>{playerChamppool.deaths}</td>
                <td>{playerChamppool.assists}</td>
                <td>{playerChamppool.cs}</td>
                <td>{playerChamppool.visionscore}</td>
                <td>{playerChamppool.cs_diff}</td>
                <td>{playerChamppool.level_diff}</td>
                <td>{playerChamppool.gold_diff}</td>
                <td>
                    <GetImage 
                        source={[
                            `https://raw.communitydragon.org/latest/game/data/spells/icons2d/summoner_${summoner1.toLowerCase()}.png`,
                            `https://raw.communitydragon.org/latest/game/data/spells/icons2d/summoner${summoner1.toLowerCase()}.png`

                        ]}
                        alt={summoner1}
                        className="Icon"
                    />
                    <GetImage 
                        source={[
                            `https://raw.communitydragon.org/latest/game/data/spells/icons2d/summoner_${summoner2.toLowerCase()}.png`,
                            `https://raw.communitydragon.org/latest/game/data/spells/icons2d/summoner${summoner2.toLowerCase()}.png`

                        ]}
                        alt={summoner2}
                        className="Icon"
                    />

                </td>
                <td>                                        
                    <img className="RoleIcon" 
                        crossOrigin="anonymous"
                        referrerPolicy="no-referrer"
                        src={roleIcon(playerChamppool.fav_role)}
                        alt={playerChamppool.fav_role} />
                </td>
                <td>{playerChamppool.season}</td>
            </tr>  
            )})       


        }
        </>
    )}


export default ChamppoolTableData