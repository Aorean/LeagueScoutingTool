const SearchButton = ({onClick}) => {
    return(
        <div>
            <button 
            type='button' 
            className="SearchButton"
            onClick = {onClick}>
                Search
            </button>
        </div>
    )
}

export default SearchButton