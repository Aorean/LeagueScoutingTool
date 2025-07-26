import Logo from "../Logo"


const Navbar = () => {

    return(
        <div className="Navbar-Container">
            <Logo className="NavbarLogo"/>
            <ul className="Navbar">
                <li>Home</li>
                <li>How to..</li>
                <li>Save files</li>
                <li>About</li>
            </ul>
        </div>
    )
}

export default Navbar