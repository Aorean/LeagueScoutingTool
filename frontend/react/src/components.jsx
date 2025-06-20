import LstLogo from './assets/LstLogo.png'

const SearchBar = () => {

    return(
    <div>
        <label htmlFor="search-input" className="SearchBarLabel">
            Post op.gg link here: 
        </label>
        <br/>
        <textarea id="search-input" name="SearchBar" className="SearchBar" cols="40" rows="5"/>
    </div>
    )
}

const Logo = () => {
    return(
        <div>
        <img src={LstLogo} className="logo" alt="LeagueScoutingTool_Logo" />
        </div>
    )
}

const SearchButton = () => {
    return(
        <div>
            <button type='submit' className="SearchButton">
                Search
            </button>
        </div>
    )
}

const OptionCard = () => {

    return(
        <div>
            <br/>
            <input type="checkbox" id="option-card" name="OptionCard" className="OptionCard"></input>
            <label htmlFor='option-card'>PDF Output </label>
            <span className="tooltip">
                <strong> ⓘ </strong>
                <span className="tooltip-text">
                    Exports a PDF that has graphs and tables about the scouted players
                </span>
            </span>
            
        </div>
    )
}



export default Logo
export { SearchBar }
export { SearchButton }
export { OptionCard }