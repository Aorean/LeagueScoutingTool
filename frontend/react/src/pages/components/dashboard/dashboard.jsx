import { useLocation, useParams, useNavigate } from "react-router-dom"; 
import { useState } from "react";
import DashboardMatchSwitch from "./dashboardMatchSwitch";
import DashboardPlayer from "./dashboardPlayer"
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
  <div>
    <div>
      <DashboardMatchSwitch content={content} />
      <DashboardPlayer content={content} />
    </div>
  </div>
)
};
export default Dashboard