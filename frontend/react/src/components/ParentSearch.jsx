import { useState } from "react"
import SearchBar from "./SearchBar"
import SearchButton from "./SearchButton"

const ParentSearch = () => {
    const [inputValue, setInputValue] = useState("")

    const handleSearch = () => {
        console.log("POST: ", inputValue);
    };
    return(
        <div>
            <SearchBar value={inputValue} onChange={setInputValue}/>
            <SearchButton onClick={handleSearch}/>
        </div>
    )
}

export default ParentSearch