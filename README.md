# ALU_Power_Mod
Files used for Modding ALU with Momentart Power Switch and Shelly relay. 

# Installation
`Shelly_In.js` and `Shelly_Out.js` get copied to the Shelly relay using the script editor. <br><BR>
`webhooks-start.sh` goes in the `rcade\share\userscripts\system-ready` folder on the ALU running Legends Unchained/RCADE.<br><BR>
`webhooks.py` and `shelly-shutdown.py` go into the `rcade\share\userscripts` folder.<br><BR>
`shelly-shutdown.sh` goes into the `rcade\share\userscripts\shutdown` folder on the ALU running Legends Unchained/RCADE.<br>

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
