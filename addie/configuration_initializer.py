import json


class ConfigurationInitializer:

    def __init__(self, parent=None):

        with open(parent.addie_config_file) as f:
            data = json.load(f)

        parent.instrument["full_name"] = data["instrument"]["current"]["full_name"]
        parent.instrument["short_name"] = data["instrument"]["current"]["short_name"]
        parent.list_instrument = data["instrument"]["list"]

        parent.config_calibration_folder = data["calibration_folder"]
        parent.config_characterization_folder = data["characterization_folder"]

        parent.calibration_extension = data["calibration_extension"]
        parent.characterization_extension = data["characterization_extension"]