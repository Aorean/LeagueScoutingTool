import { useState } from "react"
import SearchBar from "./SearchBar"
import SearchButton from "./SearchButton"
import { useNavigate } from "react-router-dom"

import playerdataService from "../../../playerdata"
//import "./ParentSearch.css"

const ParentSearch = () => {
    const [inputValue, setInputValue] = useState("")
    const navigate = useNavigate()

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