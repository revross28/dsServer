import time
import pychromecast
def cast_it():
    media_url="http://192.168.86.153:8200/FRONTDOOR.MP3"
    # Discover and connect to chromecasts named Study Speaker
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Study Speaker"])
    cast = chromecasts[0]
    # Start worker thread and wait for cast device to be ready
    cast.wait()
    mc = cast.media_controller
    mc.play_media(media_url, 'audio/mp3')
    mc.block_until_active()
    pychromecast.stop_discovery(browser)
