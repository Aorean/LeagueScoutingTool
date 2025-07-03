import Logo from "./components/Logo"
import ParentSearch from './components/ParentSearch'
import OptionCard from "./components/Frontpage/OptionCard"

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