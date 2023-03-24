import logging
import pychromecast
from app_settings import Settings
curr_settings=Settings()
#
# pychromecast logs the crap out of the pi if this is any lower, due to 'nightly' disconnections from Google Speakers.
#
logging.getLogger("pychromecast").setLevel(logging.CRITICAL)

# Get local environment setup for Google Cast devices
mySpeakers=curr_settings.chromecast_devices
mp3_host_ip=curr_settings.mp3_host_ip
#
# Based on the request passed device_id, cast the passed the passed file name to a Google Chrome device.
#
def cast_it(device_id,cast_file):
    media_url="http://"+mp3_host_ip+"/"+cast_file
    devName=mySpeakers.get(device_id,None)
    if not devName:
        return False, 'No Configuration Available for Device Id '+device_id
    # Discover and connect to chromecasts named Study Speaker
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[devName])
    if not chromecasts:
        return False, 'No Cast Device found with Name '+devName
    cast = chromecasts[0]
    # Start worker thread and wait for cast device to be ready
    cast.wait()
    # Get the media controlls for the device and play passed media url
    mc = cast.media_controller
    mc.play_media(media_url, 'audio/mp3')
    mc.block_until_active()
    pychromecast.stop_discovery(browser)
    return True,'Cast Successfully'
