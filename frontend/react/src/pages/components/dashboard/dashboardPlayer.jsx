
//import "./css/dashboardPlayer.css"

const DashboardPlayer = ({content}) => {
    const playerData = content.player
 


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
            <button>More...</button>
        </section>
    );
}

export default DashboardPlayer;