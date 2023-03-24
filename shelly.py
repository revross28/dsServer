#
# Custom module to handle requests to control Shelly Devices
# Currently we only have the Carport Light...
#
from requests import get
from app_settings import Settings
import logging
logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.ERROR)

curr_settings=Settings()
shelly_switch_ip=curr_settings.shelly_switch_ip
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
 