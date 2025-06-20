import { useState } from 'react'
import Logo, {SearchBar} from './components'

import './App.css'
import { SearchButton } from './components'
import { OptionCard } from './components'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <Logo />
      <SearchBar />
      <SearchButton />
      <p>
        You can costumise your Output by clicking the Buttons below. <br/> If you need more information about the options, hover over the "i"
      </p>
      <OptionCard/>
    </div>

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
