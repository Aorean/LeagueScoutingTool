import requests
# getting information from community dragon to convert ids (ex. item-id)
# into the actual name

items = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/items.json"
summonerspells = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/summoner-spells.json"
primary_rune = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json"

items_json = requests.get(items).json()
summonerspells_json =  requests.get(summonerspells).json()
primary_rune_json = requests.get(primary_rune).json()

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


print(dict_items)
print(dict_summonerspells)
print(dict_primary_runes)
