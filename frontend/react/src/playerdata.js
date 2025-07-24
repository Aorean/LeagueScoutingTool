import axios from "axios"



const postLink = async (link) => {
    const baseUrl = "http://127.0.0.1:8000/post_url";
    console.log("POST: ", link)
    const { data } = await axios.post(baseUrl, link);
    return data
};

const postChamppool = async(player) => {
    const baseUrl = "http://127.0.0.1:8000/post_player";
    console.log("POST: ", player)
    const { data } = await axios.post(baseUrl, player);
    return data
};





const cDragonRequestIcon = async (patch, champ) => {
    /*
    Formats
    patch: 14.22
    champ: akali
    */ 
    const url = `https://raw.communitydragon.org/${patch}/plugins/rcp-be-lol-game-data/global/default/assets/characters/${champ}/skins/base/images/${champ}_splash_tile_0.jpg`
    const icon = await axios.get(url)
    return icon
}

const cDragonRequestRank = async (rank) => {
    /*
    Formats
    patch: 14.22
    champ: akali
    */ 
    const url = `https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-static-assets/global/default/ranked-emblem/emblem-${rank}.png`
    const icon = await axios.get(url)
    return icon
}

export default {postLink, cDragonRequestIcon, cDragonRequestRank, postChamppool};

