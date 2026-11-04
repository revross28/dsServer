from flask import Flask,request,jsonify,make_response,json
from pathlib import Path
from vigi import process_vigi_event
from infra_red import handle_ir
from shelly import handleShelly,setShellyButtonState,getShellyButtonState
from cast_via_gtts import say_it,cast_it
import logging

script_dir = Path(__file__).parent
log_file=script_dir / "log" / "dsServer.log"
logging.basicConfig(
        level="DEBUG",
        format="'%(asctime)s, %(levelname)-8s [%(filename)s:%(module)s:%(funcName)s:%(lineno)d] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ],           
    )
app = Flask(__name__)

logging.getLogger("urllib3").setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
@app.route("/")
def info():
    return "<p>This is The DS Server - I'm up and running.</p>"

@app.route("/FrontDoor")
def frontDoor():
    device_id=request.args.get('gd')
    if not check_device_id(device_id):
        return "<p>Invalid Device Id in URL<p>"
    ret,msg=cast_it(device_id,'FRONTDOOR.MP3')
    return "<p>"+msg+"</p>"

@app.route("/VigiEvent", methods=['POST'])
def vigiEvent():
    # Print the raw data for debugging/inspection
    event_data  = request.get_json()
    logger.debug("Received Vigi Event Payload: %s", json.dumps(event_data, indent=2))
    actions=process_vigi_event()
    if actions['alert']:
        logger.debug("Attempting to cast FRONTDOOR.MP3 to device D")
        ret,msg=cast_it('D','FRONTDOOR.MP3')
    if actions['night_light']:
        logger.debug("Attempting to turn on Shelly Carport Light")
        ret,msg=handleShelly({"on":True})
    return jsonify({"message": "Event processed successfully"}), 200

@app.route("/SayIt")
def testCast():
    device_id=request.args.get('gd')
    msg=request.args.get('msg')
    if not check_device_id(device_id):
        return "<p>Invalid Device Id in URL<p>"
    ret,msg=say_it(device_id,msg)
    return "<p>"+msg+"</p>"

@app.route("/ir/Sony")
def ir_sony():
    return ir_generic(request)

@app.route("/ir/Fetch")
def ir_fetch():
   return ir_generic(request)
@app.route("/ir/Samsung")

def ir_samsung(request):
   return ir_generic(request)

@app.route("/ir/Panasonic")
def ir_panasonic(request):
   return ir_generic(request)
@app.route("/carport_light_switch")

def carport_switch():
    switch_flag=request.args
    return handleShelly(switch_flag)

@app.route("/button_on")
def button_on():
    resp=make_response("<html><body>Ok</body></html>",200)
    return resp

@app.route("/button_off")
def button_off():
    setShellyButtonState("off")
    return jsonify("Button Off"),200

@app.route("/button_state")
def button_state():
    return getShellyButtonState()

# Helper to check device id.
def check_device_id(id):
    if id not in ['S','L','D','B']:
        return False
    return True
# Helper to process ir path/requests.
def ir_generic(request):
    msg,status=handle_ir(request)
    return "<p>"+msg+"</msg>",status
