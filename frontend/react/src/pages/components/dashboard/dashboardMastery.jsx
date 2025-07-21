




const DashboardMastery = ({content}) => {
    const playerData = content.mastery
 


    return (
        <div>
            <table>
                <thead>
                    <tr>
                    <th>Champ</th>
                    <th>Masterypoints</th>
                    <th>Masterylevel</th>
                    </tr>
                </thead>
                
                    
                {playerData.map((accountData, index) => (
                    <tbody>
                        <tr key={index}>
                            <td>{accountData.mastery.gamertag}#{accountData.mastery.tagline}</td>
                            <td>{accountData.mastery.division} {accountData.mastery.rank}
                                <img className="MasteryIcon" 
                                crossOrigin="anonymous"
                                referrerPolicy="no-referrer"
                                src={`https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-static-assets/global/default/ranked-emblem/emblem-${accountData.account.division.toLowerCase()}.png`}
                                alt={accountData.account.division}
                                /> 
                            </td>
                            <td>{accountData.mastery.winrate}</td>
                        </tr>
                    </tbody>
                        ))}

                
            </table>

        </div>
    );
}

export default DashboardMastery;