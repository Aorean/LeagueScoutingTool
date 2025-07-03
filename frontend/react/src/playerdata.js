import axios from "axios"

const baseUrl = "http://127.0.0.1:8000/post_url";

const postLink = async (link) => {
    console.log("POST: ", link)
    const { data } = await axios.post(baseUrl, link);
    return data
};

export default {postLink};