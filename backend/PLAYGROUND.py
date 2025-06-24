

userinput = "https://op.gg/lol/multisearch/euw?summoners=Cοnni%23EUW%2CFenrirShadow%23TBS%2CAsoka30%23EUW%2CAorean%231311%2CQaQ%2300000%2C"

def process_input(userinput):
    if userinput.startswith("https://op.gg/lol/multisearch/"):
        processed_link = userinput.split("/")
        region_names = processed_link[-1]
        region = region_names.split("?")[0]
        names = region_names.split("?")[1].split("=")[1]
        single_names = names.split("%2C")[:-1]

        processed_names = []
        for gamertag_tagline in single_names:

            list_name = gamertag_tagline.split("%23")

            processed_names.append(list_name)

        processed_userinput = [region, processed_names]
        print(processed_userinput)
        return processed_userinput
    else:
        return False

asdf = process_input(userinput)


"""
class test:
    def __init__(self, data):
        self.value1 = data[0]
        self.value2 = data[1]
        self.value3 = data[2]
        self.value4 = data[3]


data = ["test1", "test2", "test3", "test4"]

testdata = test(data)

print(type(testdata.__dict__.keys()))
keys=testdata.__dict__.keys()
for key in keys:
    print(key)


champpool_data = get_data_for_champpool(db_connection)

with open("debug.txt", "w") as f:
    f.write(json.dumps(champpool_data[1], indent=4))

with open("test.json", "r") as f:
    file = json.load(f)
    participants = file["info"]["participants"][0]
    matchid = file["metadata"]["matchId"]
    puuid = participants["puuid"]



    test_class = Playerstats(participants, matchid, puuid, file)


    test_class.translate_ids
    cdragon_items = cdragon_request(test_class.patch, "items")
    cdragon_perks = cdragon_request(test_class.patch, "perks")
    cdragon_summonerspells = cdragon_request(test_class.patch, "summoner-spells")
    test_class.translate_ids(cdragon_items, cdragon_summonerspells, cdragon_perks)
    test_class.print_all()
"""

