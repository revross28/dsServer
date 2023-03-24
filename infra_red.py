

#
# This is custom IR handler for sony TV, Fetch Mighty, Panansonic and Samsung Sound Bar
# This calls a custom ESP module, with IR remote send/receive added to control stuff via IR.
#
import requests
from flask import request
from time import sleep
from app_settings import Settings
import logging
logger = logging.getLogger(__name__)
# These are sony 15 bit commands.
sony_commands={'Switch':2704,'Up':752,'Down':2800,'Left':720,'Right':3280,'Back':25321,'Exit':3184,'Home':112,'Select':2672,
              'Mute':656,'VolUp':1168,'VolDown':3216,'Louder':5,'Softer':5,'Voice':110,'Guide':27941,'TvInput':592,'ChnUp':144,
              'Pause':19689,'Play':11497,'Voice':15139,'ChnDown':2432,'0':2320,'1':16,'2':2064,'3':1040,'4':3088,'5':528,
              '6':2576,'7':1552,'8':3600,'9':272}
# These are 15 bit commands - this only happens with Sony IR               
sony15_commands=('Voice','Guide','Back','Pause','Play')
# Home=Menu for Fetch (For consistency)
fetch_commands={'Switch':644004421,'Up':643974076,'Down':643965916,'Left':643990396,'Right':644006716,'Back':644000596,'Exit':643966936,
                'ChanUp':643961836,'ChnDown':644012836,'Select':643964131,'Home':643996516,'Mute':20,'VolUp':18,'VolDown':19,'Louder':7,
                'Softer':7,'Voice':110,'Guide':643958776, 'Digits':643976371,'0':644010031,'1':643973311,'2':644005951,'3':643965151,
                '4':643997791,'5':643981471,'6':644014111,'7':643961071,'8':643993711,'9':643977391,'Reset':643961836}
# Panasonic commands          
panasonic_commands={'Switch':16825533,'VolUp':16778245,'VolDown':16811141,'0':16816281,'1':16779273,'2':16812169,
                    '3':16795721,'4':16828617,'5':16787497,'6':16820393,'7':16803945,'8':16836841,'9':16783385}
# Samsung soundbar commands
samsung_commands={'Switch':3472887537,'VolUp':3472944657,'VolDown':3472891617,'Mute':3472920177}

# Device kets
ir_address={'Sony':'SO','Panasonic':'PA','Fetch':'FE','Samsung':'SA'}

# Main dictionary of keys and commands
ir_codes={'SO':sony_commands,'FE':fetch_commands,'PA':panasonic_commands,'SA':samsung_commands}

curr_settings=Settings()
dsmart_ir_ip=curr_settings.dsmart_ir_ip
#
# Process calls to ir remote ESP8266 (NodeMcu)
# Must come from rpi's fixed ip address (good enough for now!)
# Path is to device /sony followed by command parameter, that must match
# with <device>_address dictionary. A decimal code relevant to the device/path
# is then sent to ir remote.
#
# Example url /rpi.local:8000/ir/Sony/?command="Switch" or /ir/Samsung/?command="VolUp"
# Must be one of the relevant command in the <device>_address dictionary.
#
def handle_ir(request):
    try:
        req_path=request.path.split('/')
        params = request.args
        command_key = params.get('command')
        if (len(req_path)<1) or (command_key is None):
            return "Invalid Request Parameters",400
        
        # Get device name and the key for that device
        device_name=req_path[len(req_path)-1]
        address_code=ir_address[device_name]
       
        # Check for numbers command
        if command_key=="number":
            nums=params.get("value")
            err=False
            if not nums:
                err=True
            elif not nums.isnumeric():
                err=True
            if err:
                return "Invalid Number Request",400
            # process each channel number digit sent in request.
            for i in range(len(nums)):
                num=nums[i]
                resp=send_ir(device_name,address_code,num)
                logger.info("Response from dSmart IR is "+resp[0])
                sleep(1)
            return "Numbers sent to IR",200
        else:
            resp_text,status=send_ir(device_name,address_code,command_key)
            return resp_text,status
    except Exception as e:
        logger.exception(e,exc_info=True)
        return "Error Processing request",500
#
# Send ir code, called from handler
# Can be called twice to cater for double digit commands
#
def send_ir(device_name,address_code,command_key):
    command_code=ir_codes[address_code][command_key]
    # "http://dsmart-ir.local:8000/ir_request"
    ir_URL="http://"+dsmart_ir_ip+"/ir_request?address="+address_code+"&command="+str(command_code)
    
    # Check if the command requires 15 bits (Sony only.)
    if device_name=='Sony' and (command_key in sony15_commands):
        ir_URL+="&bits=15"

        # Check for Softer/Louder requests and send repeats..
    if command_key in ('Louder','Softer'):
        ir_URL+="&repeats=7"
    logger.info("Sending url to dSmart IR now -"+ir_URL)
    resp=requests.get(ir_URL)
    logger.info("dsmart IR Request issue - status code "+str(resp.status_code))
    return resp.text,200