import os
import discord
from stats import get_player_stats
import json

def add_player(username):
    usernames.append(username)
    update_players()
    return f'Added player {username}'

def remove_player(username):
    usernames.remove(username)
    update_players()
    return f'Removed player {username}'

def print_help():
    return 'Valid commands:\n!bbc mmr - Show MMR leaderboard\n!bbc add {username} - Add new player to leaderboard\n!bbc remove {username} - Remove player from leaderboard'

def show_leaderboard():
    if len(usernames):
        leaderboard = ''
        for username in usernames:
            player = get_player_stats(username)
            leaderboard += f'{player.name} | {player.rank} | {player.mmr}\n'
        return leaderboard
    else:
        return 'No players added to leaderboard yet. Use !bbc add {username}.'

def update_players():
    os.environ['USERNAMES'] = json.dumps(usernames)

TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise Exception('No authentication token provided!')

intents = discord.Intents(messages=True, message_content=True)
client = discord.Client(intents=intents)

un_str = os.getenv('USERNAMES')
usernames = json.loads(un_str) if un_str else []

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    print(f'Received message: {message}')
    if message.author != client.user:
        content = message.content
        print(f'Parsing content: {content}')
        if content.startswith('!bbc'):
            split = content.split(' ')
            if len(split) > 1:
                if split[1] == 'mmr':
                    response = show_leaderboard()
                elif split[1] == 'add':
                     response = add_player(split[2])
                elif split[1] == 'remove':
                    response = remove_player(split[2])
                else:
                    response = print_help()
            else:
                response = print_help()
            await message.channel.send(response)

client.run(TOKEN)