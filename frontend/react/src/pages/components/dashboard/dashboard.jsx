import { useLocation, useParams, useNavigate } from "react-router-dom"; 
import { useState } from "react";
import DashboardMatchSwitch from "./dashboardMatchSwitch";
import DashboardPlayer from "./dashboardPlayer"
import DashboardMastery from "./dashboardMastery"
import DashboardChamppool from "./dashboardChamppool";
//import "./css/dashboard.css"

const Dashboard = () => {
  const [player, setPlayer] = useState([]);
  const { id } = useParams();
  const { state } = useLocation();
  const rawContent = state?.returnedBody ?? [];
  const content = JSON.parse(rawContent);
  console.log(content.player)



  //id = dashboard for me
  //state = content
  if (!state) {
    return <p>No {id} found</p>;
  }

return (
  <div className="DashboardParent">
    <DashboardPlayer content={content} />
    <DashboardMatchSwitch content={content} />
    <DashboardMastery content={content} />
    <DashboardChamppool content={content} />

  </div>
)
};
export default Dashboard