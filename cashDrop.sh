#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' /path/to/your/.env | xargs)

DIRECTORY="/home/shack/pavlovserver008/Pavlov/Saved/Config/ModSave/WeaponSkinPack/playerdata"
WEBHOOK_URL="$DISCORD_WEBHOOK_URL"
CONFIG_FILE="/home/shack/pavlovserver008/Pavlov/Saved/Config/ModSave/cash_config.json"  # Path to the configuration file
MESSAGE="SKIN MENU CASH DROP"

# Read the cash value from the configuration file
CASH_VALUE=$(jq '.cash_value' "$CONFIG_FILE")

for file in "$DIRECTORY"/*.json; do
    if [ -f "$file" ]; then
        # Read the original cash values and calculate the new cash value
        NAMES_AND_CASH=$(jq -r 'to_entries[] | "\(.key) \(.value.Cash) \(.value.Cash + '"$CASH_VALUE"')" ' "$file")

        # Build the message content
        while IFS= read -r line; do
            NAME=$(echo "$line" | awk '{print $1}')
            ORIGINAL_CASH=$(echo "$line" | awk '{print $2}')
            NEW_CASH=$(echo "$line" | awk '{print $3}')
            MESSAGE="${MESSAGE}\n :money_mouth:  ${NAME}  had ~~ ${ORIGINAL_CASH} ~~  cash, now has ** ${NEW_CASH} ** cash. :moneybag:  \n  "
        done <<< "$NAMES_AND_CASH"

        # Save the updated file
        jq '.[] |= (.Cash += '"$CASH_VALUE"')' "$file" > tmp.json && mv tmp.json "$file"
        echo "Updated Cash value in $file"
    fi
done

# Escape special characters for JSON
ESCAPED_MESSAGE=$(echo -e "$MESSAGE" | jq -Rs .)

# Send the message to Discord
if [ ! -z "$MESSAGE" ]; then
    curl -H "Content-Type: application/json" -X POST -d "{\"content\":null,\"embeds\":[{\"title\":\"Cash Update\",\"description\":${ESCAPED_MESSAGE}}]}" "$WEBHOOK_URL"
    echo "Sent notification to Discord."
fi
