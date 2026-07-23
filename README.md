***Full Disclosure: AI was used to aid in this development.***

# ALU_Power_Mod
Files used for Modding ALU running Legends Unchained (R-CADE) with Momentary Power Switch and Shelly relay. 

# Installation
`Shelly_In.js` and `Shelly_Out.js` get copied to the Shelly relay using the script editor. <br><BR>
`webhooks-start.sh` goes in the `rcade\share\userscripts\system-ready` directory on the ALU running Legends Unchained/RCADE.<br><BR>
`webhooks.py`,`shelly-shutdown.py`, and `countdown_shutdown.py` go into the `rcade\share\userscripts` directory.<br><BR>
`shelly-shutdown.sh` goes into the `rcade\share\userscripts\shutdown` directory on the ALU running Legends Unchained/RCADE.<br>
Add the `frames` directory to `rcade\share\userscripts` (if you want to generate your own, you can use generate_frames.py

# Setup
## Shelly_In
Set `EXPECTED_TOKEN` - This is the passcode just to add a minor bit of protection to the webhook calls. **They should all match.**

## Shelly_Out 
Set `SHUTDOWN_URL` - This is the IP address of the ALU.<br>
Set `EXPECTED_TOKEN`. 

## shelly-shutdown.py
Set `EXPECTED_TOKEN`.<BR>
Set `SHELLY_IP` - This is the IP address of the Shelly relay.<BR>
Set `SCRIPT_ID` - This is the Script ID of the Shelly_In script on the Shelly. You can get it from the URL when editing the script. <BR>

## webhooks.py
Set `EXPECTED_TOKEN`.<BR>
If you're also using my LCD Marquee project, you can leave in the `SIMPLE_CLIENT_SHUTDOWN_CMD` and `SIMPLE_CLIENT_REBOOT_CMD`, otherwise set them to ''

## countdown_shutdown.py
If you want to change the default countdown, change it here. 

## generate_frames.py
If you want to generate your own frames (different font perhaps, you can run this file). You can also edit the text that gets output if you want it to say something different. 


***R-Cade is legal property of Retro-Center. 
See the LICENSE.md file at the top-level directory of the Retro-Center github releases
at https://github.com/retro-center/rcade_releases/blob/master/LICENSE.md***
