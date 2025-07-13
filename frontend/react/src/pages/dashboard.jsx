import { useLocation, useParams, useNavigate } from "react-router-dom"; 
import { useState } from "react";
import DashboardTcMatches from "./components/dachboardTcMatches";
import DashboardMatchSwitch from "./components/dashboardMatchSwitch";

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

return (
  <div>
    <div>
      <DashboardMatchSwitch content={content} />
    </div>
  </div>
)
};
export default Dashboard