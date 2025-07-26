


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
            return(
            <tr key={champpoolIndex}> 
                <td>                                    
                    <img className="Icon" 
                        crossOrigin="anonymous"
                        referrerPolicy="no-referrer"
                        src={`https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${playerChamppool.champ.toLowerCase()}/skins/base/images/${playerChamppool.champ.toLowerCase()}_splash_tile_0.jpg`}
                        alt={playerChamppool.champ} />
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
                    <img className="Icon" 
                        crossOrigin="anonymous"
                        referrerPolicy="no-referrer"
                        src={`https://raw.communitydragon.org/latest/game/data/spells/icons2d/summoner_${playerChamppool.summonerspell1.toLowerCase()}.png`}
                        alt={playerChamppool.summonerspell1} />
                    <img className="Icon" 
                        crossOrigin="anonymous"
                        referrerPolicy="no-referrer"
                        src={`https://raw.communitydragon.org/latest/game/data/spells/icons2d/summoner_${playerChamppool.summonerspell2.toLowerCase()}.png`}
                        alt={playerChamppool.summonerspell2} />
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