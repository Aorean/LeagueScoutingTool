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

export default OptionCard