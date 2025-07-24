import { useLocation, useParams, useNavigate } from "react-router-dom"; 
import { useState } from "react";

//import "./css/dashboard.css"

const detailsChamppool = () => {
    const [player, setPlayer] = useState([]);
    const { id } = useParams();
    const { state } = useLocation();
    const rawContent = state?.returnedBody ?? [];
    const content = JSON.parse(rawContent);
    console.log(content)

    const champpool = content.champpools
    
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


    return (
        <section>
            <div>
                {champpool.map((player, index) => {
                    return(
                    <table key={index}>
                        <caption>{index + 1}</caption>
                        <thead>
                            <tr>
                            <th>Champ</th>
                            <th>Games played</th>
                            <th>Winrate</th>
                            <th>K/D/A</th>
                            <th>Kills</th>
                            <th>Deaths</th>
                            <th>Assists</th>
                            <th>CS</th>
                            <th>Visionscore</th>
                            <th>CS/D</th>
                            <th>Level/D</th>
                            <th>Gold/D</th>
                            <th>Fav. Summonerspells</th>
                            <th>Role</th>
                            <th>Season</th>
                            </tr>
                        </thead>
                        <tbody>
                    
                    {player.map((playerChamppool, deepIndex) => (
                    
                        <tr key={deepIndex}>
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
                            <td>PLACE SUMMONERSPELL ICONS</td>
                            <td>                                        
                                <img className="RoleIcon" 
                                    crossOrigin="anonymous"
                                    referrerPolicy="no-referrer"
                                    src={roleIcon(playerChamppool.fav_role)}
                                    alt={playerChamppool.fav_role} />
                            </td>
                            <td>{playerChamppool.season}</td>
                        </tr>  

                    ))}
                        </tbody>
                    </table>
                );
            })}

            </div>
        </section>
    )
}
export default detailsChamppool;