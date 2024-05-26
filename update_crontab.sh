#!/bin/bash

CONFIG_FILE="/home/shack/pavlovserver008/Pavlov/Saved/Config/ModSave/cash_config.json"
DROP_SCRIPT="/home/shack/pavlovserver008/Pavlov/Saved/Config/ModSave/cashDrop.sh"

# Read the drop interval from the configuration file
DROP_INTERVAL_HOURS=$(jq '.drop_interval_hours' "$CONFIG_FILE")

# Calculate the cron schedule
CRON_SCHEDULE="0 */$DROP_INTERVAL_HOURS * * *"

# Update the crontab
(crontab -l 2>/dev/null; echo "$CRON_SCHEDULE $DROP_SCRIPT") | crontab -
