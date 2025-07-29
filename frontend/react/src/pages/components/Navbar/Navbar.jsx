import Logo from "../Logo"
import "./Navbar.css"
import { useNavigate } from "react-router-dom"


const Navbar = ({page}) => {
    const navigate = useNavigate()

    const onClickRouter = ({route}) => {
        navigate(route)
    }



    return(
        <div className="Navbar-Container">
            
            <Logo className="NavbarLogo"/>
            <p className="Title">{page}</p>
            <ul className="Navbar">
                <li onClick={() => onClickRouter({route: "/"})}>
                    Home
                    </li>
                <li onClick={() => onClickRouter({route: "/howto"})}>
                    How to..
                    </li>
                <li>Save files</li>
                <li>About</li>
            </ul>
        </div>
    )
}

export default Navbar