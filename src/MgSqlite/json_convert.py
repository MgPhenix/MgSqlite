import json

def _createFile(dict,name : str, indentVal : int)->None:
    json_str = json.dumps(dict, indent=indentVal)
    with open(f"{name}.json", "w") as f:
        f.write(json_str)
        f.close()

def _loadFile(file : str) -> dict:
    with open(f"{file}","r") as json_data:
        dict = json.load(json_data)
        json_data.close()
    return dict