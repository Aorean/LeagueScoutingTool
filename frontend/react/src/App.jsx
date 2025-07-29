import { HashRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/components/Frontpage/home"; 
import Dashboard from "./pages/components/dashboard/Dashboard"
import Champpool from "./pages/components/detailsChamppool/detailsChamppool"
import Mastery from "./pages/components/detailsMastery/detailsMastery"
import Player from "./pages/components/detailsPlayer/detailsPlayer"
import HowTo from "./pages/howto/howto"

import './App.css'


const App = () => {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/dashboard" element={<Dashboard/>} />
        <Route path="/champpool" element={<Champpool/>} />
        <Route path="/mastery" element={<Mastery/>}/>
        <Route path="/player" element={<Player/>}/>
        <Route path="/tcmatches" /> 
        <Route path="/howto" element={<HowTo/>}/>
      </Routes>

    </Router>
  )
}

export default App
