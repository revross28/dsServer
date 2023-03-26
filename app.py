from flask import Flask,request
from cast import cast_it
from os import getcwd
from infra_red import handle_ir
from shelly import handleShelly
from cast_via_gtts import say_it
import logging

curr_path=getcwd()
log_file=curr_path.replace('dsServer','dsServer/log/dsServer.log') 
logging.basicConfig(
        level="DEBUG",
        format="'%(asctime)s, %(levelname)-8s [%(filename)s:%(module)s:%(funcName)s:%(lineno)d] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ],
    )
app = Flask(__name__)
logging.getLogger("urllib3").setLevel(logging.ERROR)
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
# Helper to check device id.
def check_device_id(id):
    if id not in ['S','L','D','B']:
        return False
    return True
# Helper to process ir path/requests.
def ir_generic(request):
    msg,status=handle_ir(request)
    return "<p>"+msg+"</msg>",status
