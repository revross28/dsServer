import pychromecast
services, browser = pychromecast.discovery.discover_chromecasts()
pychromecast.stop_discovery(browser)
test_name='Study Speaker'

cast = pychromecast.Chromecast('192.168.86.31')
cast.wait()
print(cast.device)

for s in services:
    print (s[3]+' - '+s[4])
    if s[3]==test_name:
        cast_ip=s[4]
        url='http://192.168.86.150:8200/FrontDoor.mp3'
        cast=pychromecast.Chromecast(cast_info=cast_ip)
        cast.wait()
        # Get the media controlls for the device and play passed media url
        mc = cast.media_controller
        mc.play_media(url, 'audio/mp3')
        cast.quit_app()




