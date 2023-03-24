import os
import json

# Class to load/manage app settings from json file.
class Settings:
    def __init__(self,s_path=None):
        self.path=s_path
        self.load_settings()
    adafruit_io_username=""
    adafruit_io_key=""
    db_path=""
    shelly_switch_ip=""
    mp3_host_ip=""
    dsmart_ir_ip=""
    chromecast_devices=[]
    def load_settings(self):
        # Dev Home - Uncomment to use.
        # project_home = '/Users/trevorthomas/Dev/Dev-Apps/dsServer'

        # PI Prod/home - Uncomment to use
        project_home = '/home/pi/apps/dsServer'

        print("Loading settings")
        print("json file path is "+project_home)
        json_file=project_home+"/app_settings.json"
        if os.path.exists(json_file):
            data = ""
            try:
                with open(json_file) as f:
                    data = json.load(f)
                f.close()
                self.chromecast_devices=data['chromecast_devices']
                self.shelly_switch_ip=data['shelly_switch_ip']
                self.mp3_host_ip=data["mp3_host_ip"]
                self.dsmart_ir_ip=data["dsmart_ir_ip"]
            except Exception as err:
                print("Exception while openning json file", str(err))
        else:
            print("Error loading settings from json file")