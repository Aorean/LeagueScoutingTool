import { useState } from "react"
import SearchBar from "./SearchBar"
import SearchButton from "./SearchButton"
import { useNavigate } from "react-router-dom"

import playerdataService from "../../playerdata"

const ParentSearch = () => {
    const [inputValue, setInputValue] = useState("")
    const navigate = useNavigate()

    /*
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
        console.log("!!!!!!!!!!!!!!!!!!" , rawResponse)
        navigate("/dashboard", {state: {content}})
        console.log(content)
    };
    */

    const handleSearch = () => {

        playerdataService.postLink({link:inputValue}).then((returnedData) => {
            const returnedBody = returnedData.Body; 

            navigate("/dashboard", {state: {returnedBody}})

            
        })

    }


    return(
        <div>
            <SearchBar value={inputValue} onChange={setInputValue}/>
            <SearchButton onClick={handleSearch}/>
        </div>
    )
}

export default ParentSearch