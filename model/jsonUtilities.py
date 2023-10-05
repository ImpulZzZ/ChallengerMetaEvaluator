import json

def extract_names_from_json(json_file):
    result = []
    with open(json_file) as jsonfile:
        data = json.load(jsonfile)

        for current in data["data"]:
            result.append(data["data"][current]["name"])

    return sorted(result)

def create_name_to_id_map(json_file):
    result = {}
    with open(json_file) as jsonfile:
        data = json.load(jsonfile)

        for current in data["data"]:
            result.update({data["data"][current]["name"] : data["data"][current]["id"]})

    return result


def create_name_to_icon_map(json_file, path_to_img):
    result = {}
    with open(json_file) as jsonfile:
        data = json.load(jsonfile)

        for current in data["data"]:
            result.update({data["data"][current]["name"] : f"{path_to_img}/{data['data'][current]['image']['full']}"})

    return result


def get_static_champion_data(json_file, path_to_img):
    result = {}
    with open(json_file) as jsonfile:
        data = json.load(jsonfile)

        for champion in data["data"]:
            result.update({data["data"][champion]["id"] : { "name":  data["data"][champion]["name"], 
                                                            "cost":  data["data"][champion]["tier"],
                                                            "image": f"{path_to_img}/{data['data'][champion]['image']['full']}"
                                                          }
                          })

    return result


def get_static_item_data(json_file, path_to_img):
    result = {}
    with open(json_file) as jsonfile:
        data = json.load(jsonfile)

        for item in data["data"]:
            result.update({data["data"][item]["id"] : { "name":  data["data"][item]["name"], 
                                                        "image": f"{path_to_img}/{data['data'][item]['image']['full']}"
                                                      }
                          })

    return result


def extract_one_unit_traits_from_json(json_file):
    result = []
    with open(json_file) as jsonfile:
        data = json.load(jsonfile)

        for current in data["data"]:
            for set in current["sets"]:
                if set["min"] == 1:
                    result.append(current["name"])

    return result