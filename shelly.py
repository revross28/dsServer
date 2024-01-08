#
# Custom module to handle requests to control Shelly Devices
# Currently we only have the Carport Light...
#

from requests import get
from app_settings import Settings
import json
import logging
logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.ERROR)

curr_settings=Settings()
shelly_switch_ip=curr_settings.shelly_switch_ip
shelly_button_ip=curr_settings.shelly_button_ip
global button_state

def handleShelly(switch_flag):
    try:
        if switch_flag.get("on") is not None:
            switch_URL="http://Admin:GoFloGo@"+shelly_switch_ip+"/relay/1?turn=on"
        if switch_flag.get("off") is not None:
            switch_URL="http://Admin:GoFloGo@"+shelly_switch_ip+"/relay/1?turn=off"
        resp=get(switch_URL)
        return resp.text,resp.status_code
    except Exception as e:
        logger.exception(e,exc_info=True)
        return "Shelly Request Failed",500

def setShellyButtonState(state):
    try:
        if state not in ['off','on']:
            logger.exception("Invalid Request to set Shelly")
        else:
            logger.info("Button State is changing to "+state)
        with open('button_state.json', 'w') as f:
            json.dump({'button_state':state}, f)
    except Exception as e:
        logger.exception(e,exc_info=True)
        return "Shelly Button Request Failed",500
    
def getShellyButtonState():
    # Opening JSON file
    f = open('button_state.json')
    data = json.load(f)
    logger.info("Returning button state of "+data['button_state'])
    return data['button_state'],200