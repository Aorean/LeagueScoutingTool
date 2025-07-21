import Logo from "../Logo"
import ParentSearch from './ParentSearch'
import OptionCard from "./OptionCard"
//import "./home.css"

const Home = () => {

  return (
    <div>
      <Logo />
      <ParentSearch/>
      <p>
        You can costumise your Output by clicking the Buttons below. <br/> If you need more information about the options, hover over the "i"
      </p>
      <OptionCard/>
    </div>

  )
}

export default Home;