import ChamppoolTableData from "./ChamppoolTableData";

const ChamppoolTableStructure = ({champpool}) => {

    return(
        <div>
            
            {champpool.map((player, index) => {
                const Name = player[0].name + "#" + player[0].tagline
                console.log(player)
                const sortedChamppool = player.sort((a,b) => b.games_played - a.games_played).sort((c,d) => d.season - c.season)
                    return(
                        <section className="detailsChamppool-Container">
                        <table key={index} className="detailsChamppool-Table">

                                <caption className="detailChamppool-Summonername">{Name}</caption>
                                <thead className="detailsChamppool-TableHead">
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
                                <ChamppoolTableData player={sortedChamppool}/>
                            </tbody>
                        </table>
                        </section>
                    );
            })}
            
        </div>
    )
}

export default ChamppoolTableStructure