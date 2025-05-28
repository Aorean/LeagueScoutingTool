from backend.config import db_connection
from backend.process_data.avrg_stats import get_data_for_champpool
import json

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