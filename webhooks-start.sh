
#!/bin/bash

# DEBUG: Log all arguments to a file
LOGFILE="/rcade/share/userscripts/system-ready/webhooks-ready.log"
rm -f "$LOGFILE"


echo "Starting webhooks server" >> $LOGFILE

python3 /rcade/share/userscripts/webhooks.py >> $LOGFILE 2>&1

echo "Script completed" >> $LOGFILE
