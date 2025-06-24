const SearchBar = ({value, onChange}) => {

    return(
    <div>
        <label htmlFor="search-input" className="SearchBarLabel">
            Post op.gg link here: 
        </label>
        <br/>
        <textarea 
        id="search-input" 
        name="SearchBar" 
        className="SearchBar" 
        cols="40" 
        rows="5" 
        value={value}
        placeholder="https://op.gg/lol/multisearch/..."
        onChange={(e) => onChange(e.target.value)}
        /> 
    </div>
    )
}

export default SearchBar