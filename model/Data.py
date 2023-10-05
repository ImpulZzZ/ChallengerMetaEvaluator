from model.jsonUtilities import extract_names_from_json, create_name_to_id_map, get_static_champion_data, get_static_item_data, create_name_to_icon_map, get_static_trait_data, extract_one_unit_traits_from_json

class Data:
    def __init__(self):
        self.current_patch             = "13.19"
        self.data_dir                  = "Set9_5_data"
        self.data_version              = "13.18.1"
        self.api_key                   = open("apikey.txt", "r").read()
        self.traits                    = extract_names_from_json(f"{self.data_dir}/traits.json")
        self.champions                 = extract_names_from_json(f"{self.data_dir}/champions.json")
        self.items                     = extract_names_from_json(f"{self.data_dir}/items.json")
        self.item_name_to_id_map       = create_name_to_id_map(f"{self.data_dir}/items.json")
        self.champion_static_data      = get_static_champion_data(f"{self.data_dir}/champions.json", f"{self.data_dir }/{self.data_version}/img/tft-champion")
        self.trait_static_data         = get_static_trait_data(f"{self.data_dir}/traits.json", f"{self.data_dir }/{self.data_version}/img/tft-trait")
        self.item_static_data          = get_static_item_data(f"{self.data_dir}/items.json", f"{self.data_dir }/{self.data_version}/img/tft-item")
        self.champion_name_to_icon_map = create_name_to_icon_map(f"{self.data_dir}/champions.json", f"{self.data_dir }/{self.data_version}/img/tft-champion")
        #self.one_unit_traits          = extract_one_unit_traits_from_json(f"{self.data_dir}/traits.json")