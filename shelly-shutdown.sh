
#!/bin/bash

# DEBUG: Log all arguments to a file
LOGFILE="/rcade/share/userscripts/shutdown/shelly-shutdown-debug.log"
rm -f "$LOGFILE"
touch &LOGFILE
echo "Initiating arcade shutdown sequence..." >> $LOGFILE

# Send shutdown command to shelly
echo "Sending shutdown to shelly relay..." >> $LOGFILE
python3 /rcade/share/userscripts/shelly-shutdown.py

echo "Shutdown sequence complete">> $LOGFILE
