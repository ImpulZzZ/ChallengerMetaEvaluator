import json

def get_names_from_json(json_file):
    result = []
    with open(json_file) as jsonfile:
        data = json.load(jsonfile)

        for current in data["data"]:
            result.append(data["data"][current]["name"])

    return sorted(result)

def get_name_to_id_map(json_file):
    result = {}
    with open(json_file) as jsonfile:
        data = json.load(jsonfile)

        for current in data["data"]:
            result.update({data["data"][current]["name"] : data["data"][current]["id"]})

    return result


def get_name_to_icon_map(json_file, path_to_img):
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


def get_static_trait_data(json_file, path_to_img):
    result = {}
    with open(json_file) as jsonfile:
        data = json.load(jsonfile)

        for trait in data["data"]:
            result.update({data["data"][trait]["id"] : { "name":  data["data"][trait]["name"], 
                                                         "image": f"{path_to_img}/{data['data'][trait]['image']['full']}"
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