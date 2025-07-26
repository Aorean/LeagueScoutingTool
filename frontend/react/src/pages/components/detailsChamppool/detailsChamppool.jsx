import { useLocation, useParams, useNavigate } from "react-router-dom"; 
import { useState } from "react";
import ChamppoolTableStructure from "./champpoolTableStructure";
import Navbar from "../Navbar/Navbar";
//import "./css/dashboard.css"

const DetailsChamppool = () => {
    const [player, setPlayer] = useState([]);
    const { id } = useParams();
    const { state } = useLocation();
    const rawContent = state?.returnedBody ?? [];
    const content = JSON.parse(rawContent);
    console.log(content)

    const champpool = content.champpools
    

     


    return (
        <div className="Parent-DetailsChamppool">
            <>
            <Navbar/>
            </>
            <>
            <ChamppoolTableStructure champpool={champpool}/>
            </>
        </div>
    )
}
export default DetailsChamppool;