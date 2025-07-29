import { useLocation, useParams, useNavigate } from "react-router-dom"; 
import { useState } from "react";

import MasteryTableStructure from "./masteryTableStructure";
import Navbar from "../Navbar/Navbar";
import "./css/DetailsMastery.css"

const DetailsMastery = () => {
    const [player, setPlayer] = useState([]);
    const { id } = useParams();
    const { state } = useLocation();
    const rawContent = state?.returnedBody ?? [];
    const content = JSON.parse(rawContent);
    console.log(content)

    const mastery = content.masteries
    
    
     


    return (
        <div className="Parent-DetailsMastery">
            <>
                <Navbar page={"Details Mastery"}/>
            </>
            <>
                <MasteryTableStructure mastery={mastery}/>
            </>

        </div>
    )
}
export default DetailsMastery;