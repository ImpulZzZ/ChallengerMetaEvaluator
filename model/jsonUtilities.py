import json

def extract_names_from_json(json_file):
    result = []
    with open(json_file) as jsonfile:
        data = json.load(jsonfile)

        for current_stats in data:
            result.append(current_stats["name"])

    return sorted(result)

def create_name_to_id_map(json_file):
    result = {}
    with open(json_file) as jsonfile:
        data = json.load(jsonfile)

        for current_stats in data:
            result.update({current_stats["name"] : current_stats["id"]})

    return result

def extract_one_unit_traits_from_json(json_file):
    result = []
    with open(json_file) as jsonfile:
        data = json.load(jsonfile)

        for current_stats in data:
            for set in current_stats["sets"]:
                if set["min"] == 1:
                    result.append(current_stats["name"])

    return result