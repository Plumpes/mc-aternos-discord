import discord
import asyncio
import requests
from python_aternos import Client

TOKEN = 'MTQ4NzUxOTIxMDE0MDczMzU0MA.GxJQv_.DtVx74-fNHQS7nEuTW-6TJdiyGO25YE0ttz-Zs'

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# ✅ Setup session with your Aternos cookie
session = requests.Session()
session.cookies.set(
    "ATERNOS_SESSION",
    "dyZZw6myfwaIgZsOHlAMN1UjqmvDUFjzpmohE2Is3uRNE3uEDTnGuDrvErvIMJd7OQjYXrMcxIkJDnqvMwKnvbORKxyHdm8TjKJW",  # 👈 your cookie
    domain=".aternos.org"
)

# ✅ Login using cookie
aternos = Client()
aternos.session = session

# fetch servers
aternos.fetch_servers()
servers = aternos.servers
myserv = servers[0]  # change if you have multiple servers


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name != 'bot-cmnds':
        return

    username = str(message.author).split('#')[0]
    msg = message.content.lower()

    # 👋 hello
    if msg == '?hello':
        await message.channel.send(f'Hello {username}!')

    # ▶️ start server
    elif msg == '?server_start':
        await message.channel.send("Starting server...")

        try:
            myserv.start()
        except Exception as e:
            await message.channel.send(f"Failed to start server: {e}")
            return

        # ⏳ wait instead of mcstatus (Discloud safe)
        await asyncio.sleep(90)

        await message.channel.send(
            "Server should be online now!\n"
            "Join using:\n"
            "||McFishySMP.aternos.me:55884||"
        )

    # ⏹ stop server
    elif msg == '?server_stop':
        try:
            myserv.stop()
            await message.channel.send("Server stopped.")
        except Exception as e:
            await message.channel.send(f"Failed to stop server: {e}")


client.run(TOKEN)
