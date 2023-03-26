import requests
from cast import cast_it
from app_settings import Settings
import logging

curr_settings=Settings()
#
# pychromecast logs the crap out of the pi if this is any lower, due to 'nightly' disconnections from Google Speakers.
#
logger = logging.getLogger(__name__)

# Get local environment setup for Google Cast devices
mySpeakers=curr_settings.chromecast_devices
mp3_host_ip=curr_settings.mp3_host_ip

# Say / cast text to google speakers.
def say_it(device_id,say_text):
    exCount=0
    retFlag=False
    fname="temp.mp3"
    while True:
        try:
            url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={say_text}&tl=en&ttsspeed=1&total=1&idx=0&client=tw-ob&tk=838940.655735"
            doc = requests.get(url)
            with open("./static/"+fname, 'wb') as f:
                f.write(doc.content)
            retFlag=True
            break
        except Exception as Ex:
            print(Ex)
            exCount+=1
            logger.warning("Google Translatate request exception count is "+str(exCount))
            if (exCount==5):
                break
    if (exCount<5):
        # Note - Port 8200 is a http server, that only serves static content.
        # This is needed for pyChromecast (e.g. file:// doesnt work.
        #castURL="http://"+mp3_host_ip+"/"+fname
        #if (pDevice=="A"):
        #    pDevice = "L","D","B","S"
        success,response = cast_it(device_id,'temp.mp3')
    return success,response
