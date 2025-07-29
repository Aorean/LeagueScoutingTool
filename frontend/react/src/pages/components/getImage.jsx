import { useState } from "react";


const GetImage = ({source, alt, className}) => {
    const [index, setIndex] = useState(0)

    const handleError = () => {

        if (index < source.length -1) {
            setIndex(index + 1)
        }
    }
    console.log(source[index])
return(
    <img
    className={className}
    src={source[index]}
    alt={alt}
    onError={handleError}
    />
);
}

export default GetImage