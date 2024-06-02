README
Overview

This project is a Discord bot for managing virtual cash and items for players in a game server. The bot provides various commands to manage user data, perform cash drops, and more.
Features

-Cash Management: Set and reset user cash values.
-Item Management: Give and remove items for users.
-Cash Drops: Perform automated cash drops for eligible users.
-Activity Monitoring: Track user activity based on log file events.
-Luck Mechanism: Implement a luck-based system for stealing items.
-Webhook Integration: Send notifications to a Discord channel via webhook.

Prerequisites

-Python 3.10+
-Discord bot token
-A valid items.json file with item definitions
-A valid cash_config.json file with cash drop configuration

<p><hr>
    <h3>Installation</h3><br>

```
git clone https://github.com/yourusername/skin-bot.git
cd skin-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

</p>

Set Up Environment Variables
Create a .env file in the project directory with the following content:

```
nano .env
```
<br>
```
    DISCORD_BOT_TOKEN=your_discord_bot_token
    DISCORD_WEBHOOK_URL=your_discord_webhook_url
```

<hr><br><h3>Start the Bot and Log Watcher</h3>

lets try and start the bot 

set variables for path in start_services.sh

```
sudo chmod +x start_services.sh
./start_services.sh
```


<p><hr>
    <h3>Bot Commands</h3><br>
    
```
        !setcash <amount>: Set the cash value for drops.
        !setluck <percentage>: Set the luck percentage for item stealing.
        !drop: Perform a cash drop for eligible users.
        !setinterval <hours>: Set the interval for cash drops.
        !resetcash: Reset all user cash values to 0.
        !giveitem <user_id> <item>: Give an item to a user.
        !resetusercash <user_id>: Reset a user's cash to 0.
        !listusers: List all users with their data.
        !removeitem <user_id> <item>: Remove an item from a user.
        !removeitems <user_id>: Remove all items from a user.
```
</p>


<p><hr>
    <h3>Planned Features</h3><br>
    
```

    Enhanced Activity Tracking: Track additional user activities and provide more detailed reports.
    Leaderboard: Display a leaderboard of users based on cash and items.
    More Detailed Logging: Improve logging to capture more events and details.
```

</p>
