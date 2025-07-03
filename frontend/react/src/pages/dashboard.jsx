import { useLocation, useParams, useNavigate } from "react-router-dom"; 
import { useState } from "react";

const Dashboard = () => {
  const [player, setPlayer] = useState([]);
  const { id } = useParams();
  const { state } = useLocation();
  const rawContent = state?.returnedBody ?? [];
  const content = JSON.parse(rawContent);
  console.log("STATE: ", state)

  //id = dashboard for me
  //state = content
  if (!state) {
    return <p>No {id} found</p>;
  }
  console.log(state)
return (
  <div>
    <h1>Gamertags</h1>
    {Object.values(content)
      .filter(entry => Array.isArray(entry.player))
      .map((entry, index) =>
        entry.player.map((playerObj, innerIndex) => (
          <p key={`${index}-${innerIndex}`}>{playerObj.gamertag}</p>
        ))
      )
      .flat()}
  </div>
)
};
export default Dashboard