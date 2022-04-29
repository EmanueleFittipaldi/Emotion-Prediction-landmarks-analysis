import json
def getFromEnv(name):
    f = open("env.json")
    path = json.load(f)
    f.close()
    return path[name]