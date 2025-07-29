import MasteryTableData from "./MasteryTableData";

const MasteryTableStructure = ({mastery}) => {


    return(
        <div>
            {mastery.map((Mastery, masteryIndex) => {
                const Name= Mastery[0].gamertag + "#" + Mastery[0].tagline
                const sortedMasters = Mastery.sort((a,b) => b.masterypoints - a.masterypoints).sort((c,d) => d.masterylevel - c.masterylevel)
                return(
                    <section key={masteryIndex} className="detailsMastery-Container">
                        <table  className="detailsMastery-Table">
                        <caption className="detailMastery-Summonername">
                            {Name}
                        </caption>
                        <thead className="detailsMastery-TableHead">
                            <tr>
                                <th>Champ</th>
                                <th>Masterypoints</th>
                                <th>Masterylevel</th>
                            </tr>
                        </thead>
                        <tbody>
                            <MasteryTableData player={sortedMasters}/>
                        </tbody>
                        </table>
                    </section>
                )
            })}
        </div>
    )
};


export default MasteryTableStructure;
