import os
import time
import json
import random
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Path to the server log file and player data directory
LOG_FILE_PATH = '~/pavlovserver/Pavlov/Saved/Logs/Pavlov.log'
PLAYER_DATA_DIR = '~/pavlovserver/Pavlov/Saved/Config/ModSave/WeaponSkinPack/playerdata'
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

#REQURMENT OF LUUCKY STEAL;
#  MUST NOT BE ON SAME TEAM
#  MUST NOT BE A SELF KILL
#  MUST BE A HEADSHOT
#  MUST BE A WEAPON ON LIST BELOW


# List of weapons that can trigger a lucky steal
LUCKY_WEAPONS = ["knife", "flash", "smoke", "snowball", "RepairTool", "webley"]

# Admin configurable luck percentage
LUCK_PERCENTAGE = 5

# Function to update the last activity timestamp and connection history for a user
def update_last_activity(username):
    for filename in os.listdir(PLAYER_DATA_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(PLAYER_DATA_DIR, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
            if username in data:
                now_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                data[username]['last_value_change'] = now_str
                if 'connection_history' not in data[username]:
                    data[username]['connection_history'] = []
                data[username]['connection_history'].append(now_str)
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                print(f'Updated last activity for {username}')
                return

# Function to update player statistics
def update_stats(killer, killed, headshot, killer_team, killed_team):
    for filename in os.listdir(PLAYER_DATA_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(PLAYER_DATA_DIR, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
            if killer in data:
                killer_data = data[killer]
                killer_data.setdefault('stats', {'kills': 0, 'deaths': 0, 'headshot_kills': 0, 'team_kills': 0, 'self_kills': 0})
                killer_data['stats']['kills'] += 1
                if headshot:
                    killer_data['stats']['headshot_kills'] += 1
                if killer_team == killed_team:
                    killer_data['stats']['team_kills'] += 1
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
            if killed in data:
                killed_data = data[killed]
                killed_data.setdefault('stats', {'kills': 0, 'deaths': 0, 'headshot_kills': 0, 'team_kills': 0, 'self_kills': 0})
                killed_data['stats']['deaths'] += 1
                if killer == killed:
                    killed_data['stats']['self_kills'] += 1
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)

# Function to handle kill events and potentially steal an item
def handle_kill_event(kill_data):
    killer = kill_data["Killer"]
    killed = kill_data["Killed"]
    killed_by = kill_data["KilledBy"]
    headshot = kill_data["Headshot"]
    killer_team = kill_data["KillerTeamID"]
    killed_team = kill_data["KilledTeamID"]

    update_stats(killer, killed, headshot, killer_team, killed_team)

    if killer != killed and killer_team != killed_team and headshot and killed_by in LUCKY_WEAPONS:
        # 5% chance to steal an item
        if random.randint(1, 100) <= LUCK_PERCENTAGE:
            stolen_item = steal_item(killer, killed)
            if stolen_item:
                send_webhook_notification(killer, killed, stolen_item, kill_data)

    if killer == killed:
        deduct_cash(killed, 300)
    elif killed_by == "knife":
        deduct_cash(killed, 500)
        if killer != killed and killer_team != killed_team:
            add_cash(killer, 500)
    elif killer_team != killed_team:
        deduct_cash(killed, 100)

def steal_item(killer, killed):
    killer_data = None
    killed_data = None

    for filename in os.listdir(PLAYER_DATA_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(PLAYER_DATA_DIR, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
            if killer in data:
                killer_data = data[killer]
            if killed in data:
                killed_data = data[killed]
            if killer_data and killed_data:
                break

    if not killer_data or not killed_data:
        return None

    if "OwnedSkins" in killed_data and killed_data["OwnedSkins"]:
        stolen_item = random.choice(killed_data["OwnedSkins"])
        killed_data["OwnedSkins"].remove(stolen_item)
        killer_data.setdefault("OwnedSkins", []).append(stolen_item)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print(f'{killer} stole {stolen_item} from {killed}')
        return stolen_item

    return None

def deduct_cash(player, amount):
    for filename in os.listdir(PLAYER_DATA_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(PLAYER_DATA_DIR, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
            if player in data:
                data[player]['Cash'] = max(data[player]['Cash'] - amount, 0)
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                print(f'Deducted ${amount} from {player}')
                return

def add_cash(player, amount):
    for filename in os.listdir(PLAYER_DATA_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(PLAYER_DATA_DIR, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
            if player in data:
                data[player]['Cash'] += amount
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                print(f'Added ${amount} to {player}')
                return

def send_webhook_notification(killer, killed, stolen_item, kill_data):
    webhook_data = {
        "content": None,
        "embeds": [
            {
                "title": "Item Stolen!",
                "description": f"**{killer}** stole **{stolen_item}** from **{killed}**.\n\n"
                               f"**Kill Details:**\n"
                               f"Killed By: {kill_data['KilledBy']}\n"
                               f"Headshot: {kill_data['Headshot']}\n"
                               f"Killer Team: {kill_data['KillerTeamID']}\n"
                               f"Killed Team: {kill_data['KilledTeamID']}\n"
                               f"Current Luck Percentage: {LUCK_PERCENTAGE}%",
                "color": 15158332
            }
        ]
    }
    response = requests.post(WEBHOOK_URL, json=webhook_data)
    if response.status_code == 204:
        print(f"Webhook notification sent for {killer} stealing {stolen_item} from {killed}.")
    else:
        print(f"Failed to send webhook notification: {response.status_code}, {response.text}")

# Function to watch the log file for join events and kill events
def watch_log():
    with open(LOG_FILE_PATH, 'r') as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            if 'Join succeeded:' in line:
                username = line.split('Join succeeded: ')[1].strip()
                update_last_activity(username)
            elif '"KillData":' in line:
                kill_data = {}
                while '}' not in line:
                    line = f.readline().strip()
                    if line.endswith(','):
                        line = line[:-1]
                    key, value = line.split(': ', 1)
                    key = key.strip('",')
                    value = value.strip('",')
                    if value.isdigit():
                        value = int(value)
                    elif value == 'true':
                        value = True
                    elif value == 'false':
                        value = False
                    kill_data[key] = value
                handle_kill_event(kill_data)

if __name__ == '__main__':
    watch_log()
