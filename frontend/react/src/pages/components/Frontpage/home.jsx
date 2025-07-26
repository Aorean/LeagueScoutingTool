import Logo from "../Logo"
import ParentSearch from './ParentSearch'
import OptionCard from "./OptionCard"
import Navbar from "../Navbar/Navbar"
//import "./home.css"

const Home = () => {

  return(

    <div>
      <Navbar/>
      <section className="Home-Container">
      
      <Logo className="logo"/>
      <ParentSearch/>
      <p>
        You can costumise your Output by clicking the Buttons below. <br/> If you need more information about the options, hover over the "i"
      </p>
      <OptionCard/>
      </section>
    </div>

  )
}

export default Home;