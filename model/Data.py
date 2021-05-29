from model.jsonUtilities import extract_names_from_json, create_name_to_id_map, extract_one_unit_traits_from_json

class Data:
    def __init__(self):
        self.current_patch       = "11.11"
        self.data_dir            = "Set5_static_data"
        self.traits              = extract_names_from_json(f"{self.data_dir}/traits.json")
        self.champions           = extract_names_from_json(f"{self.data_dir}/champions.json")
        self.items               = extract_names_from_json(f"{self.data_dir}/items.json")
        self.item_name_to_id_map = create_name_to_id_map(f"{self.data_dir}/items.json")
        self.one_unit_traits     = extract_one_unit_traits_from_json(f"{self.data_dir}/traits.json")