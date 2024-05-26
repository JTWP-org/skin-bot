import discord
import json
import os
import subprocess
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Load configuration file
CONFIG_FILE = os.path.expanduser('~/pavlovserver008/Pavlov/Saved/Config/ModSave/cash_config.json')
ITEMS_FILE = os.path.expanduser('~/pavlovserver008/Pavlov/Saved/Config/ModSave/items.json')

def load_config():
    with open(CONFIG_FILE, 'r') as file:
        return json.load(file)

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

def load_items():
    with open(ITEMS_FILE, 'r') as file:
        return json.load(file)

# Load items from the JSON file
items_data = load_items()
GHOST_ITEMS = items_data['ghost_items']
ITEMS_LIST = items_data['items_list']

# Define the intents
intents = discord.Intents.default()
intents.message_content = True  # Enable access to message content

# Create a bot instance with the command prefix '!' and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# List of authorized user IDs
AUTHORIZED_USER_IDS = [
    407796281570754560  # Replace with actual user IDs
]

def count_ghost_items(user_data):
    return sum(1 for item in user_data.get('OwnedSkins', []) if item in GHOST_ITEMS)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def setcash(ctx, new_cash_value: int):
    if ctx.author.id in AUTHORIZED_USER_IDS:
        try:
            # Update configuration
            config = load_config()
            config['cash_value'] = new_cash_value
            save_config(config)

            await ctx.send(f'Cash value updated to {new_cash_value}')
        except Exception as e:
            await ctx.send(f'Error: {e}')
    else:
        await ctx.send('You do not have permission to use this command.')

@bot.command()
async def setluck(ctx, new_luck_value: int):
    if ctx.author.id in AUTHORIZED_USER_IDS:
        try:
            global LUCK_PERCENTAGE
            LUCK_PERCENTAGE = new_luck_value
            await ctx.send(f'Luck percentage updated to {new_luck_value}%')
        except Exception as e:
            await ctx.send(f'Error: {e}')
    else:
        await ctx.send('You do not have permission to use this command.')

@bot.command()
async def drop(ctx):
    if ctx.author.id in AUTHORIZED_USER_IDS:
        try:
            directory = os.path.expanduser('/home/shack/pavlovserver008/Pavlov/Saved/Config/ModSave/WeaponSkinPack/playerdata')
            cash_value = load_config()['cash_value']
            missed_out_message = ""
            updated_message = ""

            now = datetime.now()
            threshold_time = now - timedelta(hours=24)

            eligible_users = []
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    file_path = os.path.join(directory, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)

                    for user, user_data in data.items():
                        last_value_change = datetime.strptime(user_data.get('last_value_change', '1970-01-01T00:00:00'), '%Y-%m-%dT%H:%M:%S')
                        if last_value_change > threshold_time:
                            user_data['Cash'] += cash_value
                            eligible_users.append(user)
                            updated_message += f"{user} had {user_data['Cash'] - cash_value} cash, now has {user_data['Cash']} cash. Ghost Items: {count_ghost_items(user_data)}/25\n"
                        else:
                            missed_out_message += f"{user} missed out. Ghost Items: {count_ghost_items(user_data)}/25\n"

                    with open(file_path, 'w') as file:
                        json.dump(data, file, indent=4)

            # Create webhook message
            if eligible_users:
                webhook_message = "SKIN MENU CASH DROP\n"
                for user in eligible_users[:15]:
                    webhook_message += f"{user} received {cash_value} cash.\n"
                webhook_message += missed_out_message

                # Escape special characters for JSON
                escaped_message = json.dumps({"content": None, "embeds": [{"title": "Cash Update", "description": webhook_message}]})

                # Send the message to Discord
                subprocess.run(['curl', '-H', 'Content-Type: application/json', '-X', 'POST', '-d', escaped_message, os.getenv('DISCORD_WEBHOOK_URL')], check=True)

            # Create full list of users
            user_list = []
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    file_path = os.path.join(directory, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                    for user, user_data in data.items():
                        last_value_change = user_data.get('last_value_change', 'Never')
                        cash = user_data.get('Cash', 0)
                        items = user_data.get('OwnedSkins', [])
                        ghost_item_count = count_ghost_items(user_data)
                        connection_history = user_data.get('connection_history', [])
                        user_list.append(f'User: {user}\nCash: {cash}\nItems: {items}\nLast Paid: {last_value_change}\nGhost Items: {ghost_item_count}/25\nConnection History: {connection_history}\n')

            if user_list:
                # Save user list to a text file
                with open('user_list.txt', 'w') as f:
                    f.write("\n".join(user_list))

                # Send the text file as an attachment
                await ctx.send(file=discord.File('user_list.txt'))
            else:
                await ctx.send('No users found.')

            await ctx.send('Cash drop script executed successfully.')
        except subprocess.CalledProcessError as e:
            await ctx.send(f'Error executing cash drop script: {e}')
        except Exception as e:
            await ctx.send(f'Error: {e}')
    else:
        await ctx.send('You do not have permission to use this command.')

@bot.command()
async def setinterval(ctx, hours: int):
    if ctx.author.id in AUTHORIZED_USER_IDS:
        try:
            # Update configuration
            config = load_config()
            config['drop_interval_hours'] = hours
            save_config(config)

            # Update crontab
            subprocess.run(['/home/shack/pavlovserver008/Pavlov/Saved/Config/ModSave/update_crontab.sh'], check=True)

            await ctx.send(f'Drop interval updated to {hours} hours')
        except Exception as e:
            await ctx.send(f'Error: {e}')
    else:
        await ctx.send('You do not have permission to use this command.')

@bot.command()
async def resetcash(ctx):
    if ctx.author.id in AUTHORIZED_USER_IDS:
        try:
            directory = os.path.expanduser('/home/shack/pavlovserver008/Pavlov/Saved/Config/ModSave/WeaponSkinPack/playerdata')
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    file_path = os.path.join(directory, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                    for user_data in data.values():
                        user_data['Cash'] = 0
                        user_data['last_value_change'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                    with open(file_path, 'w') as file:
                        json.dump(data, file, indent=4)
            await ctx.send('All user cash values have been reset to 0.')
        except Exception as e:
            await ctx.send(f'Error resetting cash values: {e}')
    else:
        await ctx.send('You do not have permission to use this command.')

@bot.command()
async def giveitem(ctx, user_id: str, item: str):
    if ctx.author.id in AUTHORIZED_USER_IDS:
        if item not in ITEMS_LIST:
            await ctx.send(f'Invalid item: {item}')
            return

        try:
            directory = os.path.expanduser('/home/shack/pavlovserver008/Pavlov/Saved/Config/ModSave/WeaponSkinPack/playerdata')
            user_found = False
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    file_path = os.path.join(directory, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                    if user_id in data:
                        user_data = data[user_id]
                        user_data.setdefault('OwnedSkins', []).append(item)
                        user_data['last_value_change'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                        with open(file_path, 'w') as file:
                            json.dump(data, file, indent=4)
                        user_found = True
                        await ctx.send(f'Item "{item}" given to user {user_id}.')
                        break
            if not user_found:
                await ctx.send(f'User ID {user_id} not found.')
        except Exception as e:
            await ctx.send(f'Error giving item to user: {e}')
    else:
        await ctx.send('You do not have permission to use this command.')

@bot.command()
async def resetusercash(ctx, user_id: str):
    if ctx.author.id in AUTHORIZED_USER_IDS:
        try:
            directory = os.path.expanduser('/home/shack/pavlovserver008/Pavlov/Saved/Config/ModSave/WeaponSkinPack/playerdata')
            user_found = False
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    file_path = os.path.join(directory, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                    if user_id in data:
                        user_data = data[user_id]
                        user_data['Cash'] = 0
                        with open(file_path, 'w') as file:
                            json.dump(data, file, indent=4)
                        user_found = True
                        await ctx.send(f'Cash for user {user_id} has been reset to 0.')
                        break
            if not user_found:
                await ctx.send(f'User ID {user_id} not found.')
        except Exception as e:
            await ctx.send(f'Error resetting cash for user: {e}')
    else:
        await ctx.send('You do not have permission to use this command.')

@bot.command()
async def listusers(ctx):
    if ctx.author.id in AUTHORIZED_USER_IDS:
        try:
            directory = os.path.expanduser('/home/shack/pavlovserver008/Pavlov/Saved/Config/ModSave/WeaponSkinPack/playerdata')
            user_list = []
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    file_path = os.path.join(directory, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                    for user, user_data in data.items():
                        last_value_change = user_data.get('last_value_change', 'Never')
                        cash = user_data.get('Cash', 0)
                        items = user_data.get('OwnedSkins', [])
                        ghost_item_count = count_ghost_items(user_data)
                        connection_history = user_data.get('connection_history', [])
                        user_list.append(f'User: {user}\nCash: {cash}\nItems: {items}\nLast Paid: {last_value_change}\nGhost Items: {ghost_item_count}/25\nConnection History: {connection_history}\n')

            if user_list:
                # Send user list as an embed
                embed = discord.Embed(title="User List")
                embed.description = "\n".join(user_list[:2048])  # Limit to Discord's embed character limit

                await ctx.send(embed=embed)

                # Save full user list to a text file
                with open('user_list.txt', 'w') as f:
                    f.write("\n".join(user_list))

                # Send the text file as an attachment
                await ctx.send(file=discord.File('user_list.txt'))
            else:
                await ctx.send('No users found.')
        except Exception as e:
            await ctx.send(f'Error listing users: {e}')
    else:
        await ctx.send('You do not have permission to use this command.')

@bot.command()
async def removeitem(ctx, user_id: str, item: str):
    if ctx.author.id in AUTHORIZED_USER_IDS:
        try:
            directory = os.path.expanduser('/home/shack/pavlovserver008/Pavlov/Saved/Config/ModSave/WeaponSkinPack/playerdata')
            user_found = False
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    file_path = os.path.join(directory, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                    if user_id in data:
                        user_data = data[user_id]
                        if item in user_data.get('OwnedSkins', []):
                            user_data['OwnedSkins'].remove(item)
                            user_data['last_value_change'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                            with open(file_path, 'w') as file:
                                json.dump(data, file, indent=4)
                            user_found = True
                            await ctx.send(f'Item "{item}" removed from user {user_id}.')
                        else:
                            await ctx.send(f'User {user_id} does not have item "{item}".')
                        break
            if not user_found:
                await ctx.send(f'User ID {user_id} not found.')
        except Exception as e:
            await ctx.send(f'Error removing item from user: {e}')
    else:
        await ctx.send('You do not have permission to use this command.')

@bot.command()
async def removeitems(ctx, user_id: str):
    if ctx.author.id in AUTHORIZED_USER_IDS:
        try:
            directory = os.path.expanduser('/home/shack/pavlovserver008/Pavlov/Saved/Config/ModSave/WeaponSkinPack/playerdata')
            user_found = False
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    file_path = os.path.join(directory, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                    if user_id in data:
                        user_data = data[user_id]
                        user_data['OwnedSkins'] = []
                        user_data['last_value_change'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                        with open(file_path, 'w') as file:
                            json.dump(data, file, indent=4)
                        user_found = True
                        await ctx.send(f'All items removed from user {user_id}.')
                        break
            if not user_found:
                await ctx.send(f'User ID {user_id} not found.')
        except Exception as e:
            await ctx.send(f'Error removing items from user: {e}')
    else:
        await ctx.send('You do not have permission to use this command.')

# Run bot
bot.run(TOKEN)
