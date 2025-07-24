import { HashRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/components/Frontpage/home"; 
import Dashboard from "./pages/components/dashboard/Dashboard"
import Champpool from "./pages/components/detailsChamppool/detailsChamppool"

import './App.css'


const App = () => {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/dashboard" element={<Dashboard/>}/>
        <Route path="/champpool" element={<Champpool/>} />
      </Routes>

    </Router>
  )
}






{
/*
<div>
  <a href="https://vite.dev" target="_blank">
    <img src={LstLogo} className="logo" alt="Vite logo" />
  </a>
  <a href="https://react.dev" target="_blank">
    <img src={LstLogo} className="logo react" alt="React logo" />
  </a>
</div>
<h1>Vite + React</h1>
<div className="card">
  <button onClick={() => setCount((count) => count + 1)}>
    count is {count}
  </button>
  <p>
    Edit <code>src/App.jsx</code> and save to test HMR
  </p>
</div>
<p className="read-the-docs">
  Click on the Vite and React logos to learn more
</p>
</>
*/
}
export default App
