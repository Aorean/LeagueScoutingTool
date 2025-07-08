import { useLocation, useParams, useNavigate } from "react-router-dom"; 
import { useState } from "react";
import DashboardTcMatches from "./components/dachboardTcMatches";

const Dashboard = () => {
  const [player, setPlayer] = useState([]);
  const { id } = useParams();
  const { state } = useLocation();
  const rawContent = state?.returnedBody ?? [];
  const content = JSON.parse(rawContent);





  //id = dashboard for me
  //state = content
  if (!state) {
    return <p>No {id} found</p>;
  }
  console.log(content)
return (
  <div>
    {content.tc_Matches.map((match, index) => (<DashboardTcMatches key={index} {...match} />))
    
    }
  </div>
)
};
export default Dashboard