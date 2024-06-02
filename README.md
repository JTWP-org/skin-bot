README
Overview

This project is a Discord bot for managing virtual cash and items for players in a game server. The bot provides various commands to manage user data, perform cash drops, and more.
Features

    Cash Management: Set and reset user cash values.
    Item Management: Give and remove items for users.
    Cash Drops: Perform automated cash drops for eligible users.
    Activity Monitoring: Track user activity based on log file events.
    Luck Mechanism: Implement a luck-based system for stealing items.
    Webhook Integration: Send notifications to a Discord channel via webhook.

Prerequisites

    Python 3.10+
    Discord bot token
    A valid items.json file with item definitions
    A valid cash_config.json file with cash drop configuration

Installation

    Clone the Repository

    bash

git clone https://github.com/yourusername/skin-bot.git
cd skin-bot

Create a Virtual Environment

bash

python3 -m venv venv
source venv/bin/activate

Install Dependencies

bash

pip install -r requirements.txt

Set Up Environment Variables
Create a .env file in the project directory with the following content:

env

    DISCORD_BOT_TOKEN=your_discord_bot_token
    BOT_VERSION=1.0.0
    BOT_URL=https://JTWP.org
    DISCORD_WEBHOOK_URL=your_discord_webhook_url

    Ensure Configuration Files Exist
        items.json: Contains item definitions.
        cash_config.json: Contains cash drop configuration.

Configuration Files
items.json

json

{
    "ghost_items": [
        "knife_ghost", "57_ghost", "m4_ghost", "ak47_ghost", "1911_ghost", "akshorty_ghost",
        "ar9_ghost", "ump_ghost", "aug_ghost", "awp_ghost", "de_ghost", "autosniper_ghost",
        "galil_ghost", "glock_ghost", "huntingrifle_ghost", "knife_ghost_generic", "kriss_ghost",
        "m9_ghost", "revolver_ghost", "m16_ghost", "vanas_ghost", "cet9_ghost", "supp_rifle_ghost",
        "holo_ghost", "p90_ghost"
    ],
    "all_items": [
        // Add all other items here...
    ]
}

cash_config.json

json

{
    "cash_value": 1000,
    "drop_interval_hours": 24
}

Usage

    Start the Bot and Log Watcher

    bash

    ./start_services.sh

    Bot Commands
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

Planned Features

    Enhanced Activity Tracking: Track additional user activities and provide more detailed reports.
    Leaderboard: Display a leaderboard of users based on cash and items.
    More Detailed Logging: Improve logging to capture more events and details.
