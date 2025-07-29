import GetImage from "../getImage"

const ChamppoolTableData = ({player}) => {
    
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

    return(
        player.map((playerMastery, masteryIndex) => {
            const UrlChamp = playerMastery.champ.replace(" ", "").toLowerCase()


            return(
                <tr key={masteryIndex}>
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
                        alt={playerMastery.champ}
                        className="Icon"
                        />
                    </td>
                    <td>{playerMastery.masterypoints} </td>              
                    <td>
                        {playerMastery.masterylevel}
                        <img className="MasteryIcon" 
                        crossOrigin="anonymous"
                        referrerPolicy="no-referrer"
                        src={masteryPng(playerMastery.masterylevel)}
                        alt={playerMastery.masterylevel}
                        /> 
                    </td>

                </tr>
            )
        })
    )
}

export default ChamppoolTableData