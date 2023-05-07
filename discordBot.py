import discord
import requests

API_URL = "http://ergast.com/api/f1/current/last/results.json"

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name} ({client.user.id})")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!f1result"):
        result = get_race_result()
        await message.channel.send(result)

def get_race_result():
    response = requests.get(API_URL)

    if response.status_code != 200:
        return "Error fetching F1 race result"

    data = response.json()
    race = data["MRData"]["RaceTable"]["Races"][0]
    result = f"Results for {race['raceName']}, {race['Circuit']['circuitName']}\n\n"

    for driver in race["Results"]:
        position = driver["position"]
        name = driver["Driver"]["givenName"] + " " + driver["Driver"]["familyName"]
        team = driver["Constructor"]["name"]
        time = driver["Time"]["time"] if "Time" in driver else "+0"

        result += f"{position}. {name} - {team} ({time})\n"

    return result

client.run("MTEwNDg5NzI0NDg5NDg1NTIxOQ.GHZZxK.pU5IjWbfS1P7zonx-VW6k8idqKAFFD3bJWk13g")
