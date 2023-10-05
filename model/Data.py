from model.jsonUtilities import *

class Data:
    def __init__(self):
        self.current_patch = "13.19"
        self.data_dir      = "Set9_5_data"
        self.data_version  = "13.18.1"
        self.api_key       = open("apikey.txt", "r").read()

        self.traits    = get_names_from_json(f"{self.data_dir}/traits.json")
        self.champions = get_names_from_json(f"{self.data_dir}/champions.json")
        self.items     = get_names_from_json(f"{self.data_dir}/items.json")

        self.champion_static_data = get_static_champion_data(f"{self.data_dir}/champions.json", f"{self.data_dir }/{self.data_version}/img/tft-champion")
        self.trait_static_data    = get_static_trait_data(f"{self.data_dir}/traits.json", f"{self.data_dir }/{self.data_version}/img/tft-trait")
        self.item_static_data     = get_static_item_data(f"{self.data_dir}/items.json", f"{self.data_dir }/{self.data_version}/img/tft-item")
        
        self.champion_name_to_icon_map = get_name_to_icon_map(f"{self.data_dir}/champions.json", f"{self.data_dir }/{self.data_version}/img/tft-champion")
        self.item_name_to_id_map       = get_name_to_id_map(f"{self.data_dir}/items.json")