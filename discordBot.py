import requests
import discord
from discord.ext import tasks

# Set up your Discord bot token
TOKEN = "MTEwNDg5NzI0NDg5NDg1NTIxOQ.GHZZxK.pU5IjWbfS1P7zonx-VW6k8idqKAFFD3bJWk13g
"

# Define a function to retrieve the F1 race results and post them in the Discord channel
def post_race_results():
    # Retrieve the race results from the Ergast API
    response = requests.get("https://ergast.com/api/f1/current/last/results.json")
    results = response.json()["MRData"]["RaceTable"]["Races"][0]["Results"]

    # Create a message to post in the Discord channel
    message = "**F1 Race Results**\n"
    for result in results:
        message += f"{result['Driver']['familyName']}: {result['position']}\n"

    # Get the channel where you want to post the message
    channel = client.get_channel("1104877246994460843")

    # Post the message in the channel
    channel.send(message)

# Set up a client to interact with the Discord API
client = discord.Client()

# Define a background task that runs every minute and posts the race results
@tasks.loop(minutes=1)
async def post_results_task():
    await client.wait_until_ready()
    await post_race_results()

# Start the background task
post_results_task.start()

# Run the bot
client.run(TOKEN)
