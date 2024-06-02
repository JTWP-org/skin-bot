Installation Instructions
Prerequisites

    Python 3.8+: Ensure you have Python 3.8 or later installed.
    pip: Ensure you have pip installed.
    git: Ensure you have git installed.
    jq: Ensure you have jq installed.

Step 1: Clone the Repository

Clone the repository from GitHub to your local machine:



```
git clone https://github.com/JTWP-org/skin-bot.git
cd your-repository
```

Step 2: Create and Activate a Virtual Environment

Create and activate a Python virtual environment:

```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Step 3: Install Python Dependencies
```
pip install -r requirements.txt
```

Step 4: Configure Environment Variables

Create a .env file in the root directory of your project and add the following environment variables:
```
nano .env
```
```
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url
```
Replace your_discord_bot_token and your_webhook_url with your actual Discord bot token and webhook URL.
Step 5: Configure Crontab (Optional)

If you want to set up automated cash drops, you can configure a cron job. Update the update_crontab.sh script as needed and make it executable:

#BE sure to update path here use a full path too not ~
```
chmod +x /path/to/your/update_crontab.sh
./update_crontab.sh
```

Running the Bot and Log Watcher
Step 1: Start the Log Watcher
```
python watch_logs.py
```
```
python bot.py
```

<hr>
Bot Commands

Here are the available bot commands:

    !setcash <value>: Set the cash drop value.
    !setluck <value>: Set the luck percentage for stealing items.
    !drop: Run the cash drop script manually.
    !setinterval <hours>: Set the interval for automated cash drops.
    !resetcash: Reset all user cash values to 0.
    !giveitem <user_id> <item>: Give an item to a user.
    !resetusercash <user_id>: Reset a user's cash to 0.
    !listusers: List all users with their details.
    !removeitem <user_id> <item>: Remove an item from a user.
    !removeitems <user_id>: Remove all items from a user.

Cash Loss System

The cash loss system works as follows:

    -100: Lose 100 cash on death by another team member.
    -300: Lose 300 cash on self-kill.
    -500: Lose 500 cash if killed by a knife.
    +500: Gain 500 cash if you kill another team member with a knife.

Planned Features

Here are some planned features for future development:

    Enhanced Statistics: Track additional player statistics such as total playtime, accuracy, and more.
    Leaderboard: Create a leaderboard to display top players based on various metrics.
    Item Trading: Allow users to trade items with each other.
    Achievements: Implement an achievements system to reward players for specific actions.
    In-Game Events: Create special in-game events with unique rewards.
    award for getting all 25 ghost  items 

TROUBLESHOOTING

    Bot Not Responding: Ensure the bot token is correct and the bot has permissions to read and send messages in the channel.
    Crontab Issues: Verify the cron job is set up correctly and the paths in the update_crontab.sh script are accurate.
    Log Watcher Issues: Ensure the log file path is correct and the script has read permissions for the log file.
