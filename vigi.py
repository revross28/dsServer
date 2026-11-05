#
# Custom module to handle vigi camera events.
# Returns notice on actions to cast to google speaker and/or turn on shelly carport light.
#
from app_settings import Settings
import json
import logging
from datetime import datetime,timezone,timedelta
logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.ERROR)

curr_settings=Settings()

# Do two things:
#
# 1. Check if the current time is between sunrise and sunset to determine if shelly carport night light should be triggered on. 
#    NOTE - Sunrise/Sunset is dumped to a json file by a daily cron job running sun_data.py that accesses the sunrise-sunset API.

# 2. Check previous event and don't cast voice alert via google speaker if previous alert was inside 3 minutes.
#    This avoids multiple voice alerts when someone is outside the front door for 3+ mins.
#
# 1 & 2 happen independently
def process_vigi_event():
    
    event_actions={'alert':False,'night_light': False}
    # Load previous vigi event data from json record (if any)
    last_event=read_vigi_event()

    # 1. Check if last event is within 3 mins of current time (local time) to determine if voice alert is needed.
    last_event_time=datetime.fromisoformat(last_event['date'])
    curr_time=datetime.now(timezone.utc).astimezone() 
    logger.debug(f"Current Time: {curr_time}, Last Event Time : {last_event_time}")
    if curr_time - last_event_time >= timedelta(minutes=3):
        event_actions['alert']=True
        # Only save the event once the alert is triggered to keep alerts within the 3 min window.
        save_vigi_event(curr_time)

    # 2. Check if current time is between sunrise and sunset to determine if night light should be triggered on.
    sun_data=read_sun_data()
    sunrise_time = datetime.fromisoformat(sun_data['sunrise'])
    # Take an hour off sunset to match other automation settings.
    sunset_time = datetime.fromisoformat(sun_data['sunset']) - timedelta(hours=1)
    logger.debug(f"Current Time: {curr_time}, Sunrise Time: {sunrise_time}, Sunset Time: {sunset_time}")
    if sunrise_time < curr_time > sunset_time:
        event_actions['night_light']=True

    return event_actions

def read_vigi_event():
    f = open('vigi_event.json')
    data = json.load(f)
    logger.debug(f"Saved vigi event data is {data}")
    return data

def read_sun_data():
    f = open('sun_data.json')
    data = json.load(f)
    #logger.debug(f"Saved sun data is {data}")
    return data

def save_vigi_event(curr_time):
    v_event={'date':curr_time.isoformat()}
    with open('vigi_event.json', 'w') as f:
        json.dump(v_event, f) 
    logger.debug(f"Saved vigi event data is {v_event}")
    return 
