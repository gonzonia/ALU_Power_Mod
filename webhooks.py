import json
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

import logging

# Configure logging to show INFO level and above
logging.basicConfig(
    filename="/rcade/share/userscripts/webhooks.log",
    filemode="w",  # Overwrites the file each time; use 'a' to append
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Optional shared secret. Anyone on the LAN can POST to this port by default,
# so set this to a long random string and add the same value to the Shelly
# script's JSON body (e.g. {"action":"shutdown","token":"..."}) if you want
# basic protection against something else on the network triggering a real
# shutdown. Leave as None to skip the check entirely.
EXPECTED_TOKEN = "<YOUR TOKEN HERE>"

SHUTDOWN_PATH = "/shutdown"

#Send signal to LCD Marquee shutdown, set to blank if not using. 
SIMPLE_CLIENT_SHUTDOWN_CMD = 'timeout 10 python3 /rcade/share/userscripts/simpleClient.py "SHUTDOWN"'
SIMPLE_CLIENT_REBOOT_CMD = 'timeout 10 python3 /rcade/share/userscripts/simpleClient.py "REBOOT"'

def trigger_shutdown():
    """
    Non-blocking: schedules the shutdown sequence a couple seconds out so
    this process (and the HTTP response already sent to the Shelly) has
    time to actually flush over the socket before Linux goes down.
 
    Sequence:
      1. Notify the marquee/display client (simpleClient.py) that we're
         shutting down, capped at 10s via `timeout` so a hung client
         script can't block the actual shutdown.
      2. `shutdown -h now` regardless of whether step 1 succeeded, timed
         out, or errored -- the `;` separators (not `&&`) are deliberate,
         so a broken notifier never prevents the real shutdown. The
         Shelly's own timer is the true fallback either way.
    """
    cmd = "%s; sleep 2; shutdown -h now" % SIMPLE_CLIENT_SHUTDOWN_CMD

    subprocess.Popen(["sh", "-c", cmd])
    
def trigger_reboot():
    """
    Non-blocking: schedules the shutdown sequence a couple seconds out so
    this process (and the HTTP response already sent to the Shelly) has
    time to actually flush over the socket before Linux goes down.
 
    Sequence:
      1. Notify the marquee/display client (simpleClient.py) that we're
         shutting down, capped at 10s via `timeout` so a hung client
         script can't block the actual shutdown.
      2. `shutdown -h now` regardless of whether step 1 succeeded, timed
         out, or errored -- the `;` separators (not `&&`) are deliberate,
         so a broken notifier never prevents the real shutdown. The
         Shelly's own timer is the true fallback either way.
    """
    cmd = "%s; sleep 2; reboot" % SIMPLE_CLIENT_REBOOT_CMD

    subprocess.Popen(["sh", "-c", cmd])    

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != SHUTDOWN_PATH:
            logging.info("Request received, wrong path")
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get('Content-Length', 0))
        raw_data = self.rfile.read(content_length).decode('utf-8')

        try:
            payload = json.loads(raw_data)
            logging.info("Request received: %s", payload)

        except json.JSONDecodeError:
            logging.info("Request received, JSON Error")        
            self.send_response(400)
            self.end_headers()
            return

        if EXPECTED_TOKEN and payload.get("token") != EXPECTED_TOKEN:
            logging.info("Request received, Missing Token")        
            self.send_response(403)
            self.end_headers()
            return 
        
        if payload.get("action") not in ("shutdown", "reboot"):
            logging.info("Unknown Request received")        
            self.send_response(400)
            self.end_headers()
            return
            
        logging.info("Shutdown request received:", payload)

        # Acknowledge first -- the Shelly only needs a 200 to know the ALU
        # heard it. The actual power cut happens on the Shelly's own timer
        # regardless of what happens next on this end.
        action = payload.get("action")
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status": "ok", "action": action}')

        if payload.get("action") == "shutdown":
            trigger_shutdown()
            return
            
        if payload.get("action") == "reboot":
            trigger_reboot()
            return

    def log_message(self, format, *args):
        # Keep default console logging. Override with `pass` here if you'd
        # rather silence per-request access logs.
        logging.info("%s - %s" % (self.address_string(), format % args))


httpd = HTTPServer(('0.0.0.0', 8000), WebhookHandler)
logging.info("Listening on port 8000...")
httpd.serve_forever()
