import boto3
from discord.ext import commands
import phonenumbers
from Secrets import Access_Key, Secret_Access_Key, Discord_Token

# Command prefix not being used
client = commands.Bot(command_prefix='!')

# Client prints when bot starts
@client.event
async def on_ready():
    print("Bot is Ready!")

# Client on messages checks if starts with + then execute
# Sends text through amazon AWS SNS and sends SMS
@client.event
async def on_message(message):
    # !sms <command> <phone number> <message>
    if message.content.startswith('!sms'):
        # channel = message.channel
        tokenized_message = message.content.split(" ")

        # print(tokenized_message)

        # remove !sms flag
        tokenized_message.pop(0)

        if len(tokenized_message) == 0:
            await message.channel.send("Invalid Command!")

        # get the command argument
        command = tokenized_message.pop(0)

        if command == "send":
            # get the phone number argument
            sms_number = tokenized_message.pop(0)

            number_analysis = phonenumbers.parse(sms_number, None)
            if phonenumbers.is_valid_number(number_analysis):
                # ensure the phone number is a US number
                if number_analysis.country_code != 1:
                    await message.channel.send("Phone Number must be a US Number!")

                sms_message = " ".join(tokenized_message)

                # Create an SNS client
                sns_client = boto3.client(
                    "sns",
                    aws_access_key_id=Access_Key,
                    aws_secret_access_key=Secret_Access_Key,
                    region_name="us-west-2"
                )

                try:
                    sns_client.publish(
                        PhoneNumber=sms_number,
                        Message=sms_message
                    )

                    await message.channel.send("Message sent successfully!")
                except Exception as e:
                    await message.channel.send("An error occurred while sending a message. Error: " + str(e))

            else:
                await message.channel.send("Invalid Phone Number!")

        else:
            await message.channel.send("Invalid Command!")

# Token to run discord bot
client.run(Discord_Token)

