import json
def getFromEnv(name):
    f = open("src/env.json")
    path = json.load(f)
    f.close()
    return path[name]