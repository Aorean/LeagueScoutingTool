import requests
# getting information from community dragon to convert ids (ex. item-id)
# into the actual name

items = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/items.json"
summonerspells = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/summoner-spells.json"
primary_rune = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json"

items_json = requests.get(items).json()
summonerspells_json =  requests.get(summonerspells).json()
primary_rune_json = requests.get(primary_rune).json()
#"https://raw.communitydragon.org/10.7/plugins/rcp-be-lol-game-data/global/default/v1/"
def cdragon_request(patch, request_object):
    cdragon_url = f"https://raw.communitydragon.org/{patch}/plugins/rcp-be-lol-game-data/global/default/v1/{request_object}.json"
    return_json = requests.get(cdragon_url ).json()

    obj_dict = {}
    for obj in return_json:
        id = obj["id"]
        name = obj["name"]
        name_edit = name.replace("'","")
        obj_dict[id] = name_edit

    return obj_dict

def get_id_name(json):
    obj_dict = {}
    for obj in json:
        id = obj["id"]
        name = obj["name"]
        name_edit = name.replace("'","")
        obj_dict[id] = name_edit

    return obj_dict


dict_items = get_id_name(items_json)
dict_summonerspells = get_id_name(summonerspells_json)
dict_primary_runes = get_id_name(primary_rune_json)



