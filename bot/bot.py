import os
import discord
from stats import get_player_stats
import json

USERNAME_FILE_NAME = 'usernames.json'

def add_username(username):
    if not username in usernames:
        usernames.append(username)
        write_usernames()
        return f'Added player {username}'
    else:
        return f'Player {username} is already on the leaderboard!'


def remove_username(username):
    if username in usernames:
        usernames.remove(username)
        write_usernames()
        return f'Removed player {username}'
    else:
        return f'Player {username} is not on the leaderboard!'


def print_help():
    return 'Valid commands:\n!bbc mmr - Show MMR leaderboard\n!bbc add {username} - Add new player to leaderboard\n!bbc remove {username} - Remove player from leaderboard'


def show_leaderboard():
    if len(usernames):
        players = [get_player_stats(un) for un in usernames]
        players.sort(key=lambda x: x.mmr, reverse=True)
        leaderboard = f'```Username            | Rank           | MMR\n{"-" * 45}\n' 
        for player in players:
            name_padding = ' ' * (20 - len(player.name))
            rank_padding = ' ' * (15 - len(player.rank))
            leaderboard += f'{player.name}{name_padding}| {player.rank}{rank_padding}| {player.mmr}\n'
        leaderboard += '```'
        return leaderboard
    else:
        return 'No players added to leaderboard yet. Use !bbc add {username}.'


def write_usernames():
    path = os.path.join(os.getcwd(), USERNAME_FILE_NAME)
    with open(path, 'w') as f:
        json.dump(usernames, f)


def read_usernames():
    path = os.path.join(os.getcwd(), USERNAME_FILE_NAME)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    else:
        return []


TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise Exception('No authentication token provided!')

intents = discord.Intents(messages=True, message_content=True)
client = discord.Client(intents=intents)

usernames = read_usernames()

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
                     response = add_username(split[2])
                elif split[1] == 'remove':
                    response = remove_username(split[2])
                else:
                    response = print_help()
            else:
                response = print_help()
            await message.channel.send(response)

client.run(TOKEN)