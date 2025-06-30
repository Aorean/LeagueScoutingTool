import { useState } from "react"
import SearchBar from "./SearchBar"
import SearchButton from "./SearchButton"

const ParentSearch = () => {
    const [inputValue, setInputValue] = useState("")

    const handleSearch = async () => {
        console.log("POST: ", inputValue);
        
        const rawResponse = await fetch("http://127.0.0.1:8000/post_url", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            
            body: JSON.stringify({link: inputValue})
            });
        const content = await rawResponse.json();
        console.log(content)
    };
    return(
        <div>
            <SearchBar value={inputValue} onChange={setInputValue}/>
            <SearchButton onClick={handleSearch}/>
        </div>
    )
}

export default ParentSearch