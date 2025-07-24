




const DashboardMastery = ({content}) => {
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
                                {accountData.mastery.map((champMastery, index) => (
                                    <tr key={index}>
                                        <td>
                                        <img className="Icon" 
                                        crossOrigin="anonymous"
                                        referrerPolicy="no-referrer"
                                        src={`https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/${champMastery.champ.toLowerCase()}/skins/base/images/${champMastery.champ.toLowerCase()}_splash_tile_0.jpg`}
                                        alt={champMastery.champ} />
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
                                ))}
                            </tbody>
                        </table>
                        
                    ))}
                
            </div>
            <button>More...</button>
        </section>
    );
}

export default DashboardMastery;