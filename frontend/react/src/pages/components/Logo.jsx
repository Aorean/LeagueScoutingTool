import LstLogo from "./assets/LstLogo.png"

const Logo = ({className}) => {
    return(
        <div>
        <img src={LstLogo} alt="LeagueScoutingTool_Logo" className={className} />
        </div>
    )
}

export default Logo