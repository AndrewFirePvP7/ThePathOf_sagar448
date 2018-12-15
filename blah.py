import discord
import time

client = discord.Client()

frozen = []

prefix = "-"


def getCmd(thing):
    return thing[int(len(prefix)):int(len(thing))].lower()


def checkAdmin(person):
    perms = person.server_permissions
    if perms.administrator:
        return True
    else:
        return False


def checkMentions(msg):
    try:
        guy = msg.mentions[0]
        return guy
    except:
        return False


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(prefix):
        command = getCmd(message.content)
        print(command)

        if command[0:6] == "freeze":
            if checkAdmin(message.author):
                print("yeet they're an admin")
                mention = checkMentions(message)
                if mention:
                    if not checkAdmin(mention):
                        frozen.append([mention, time.time(), False])

        if command[0:5] == "hello":
            await client.send_message(message.channel, "Hello!")

    for person in frozen:
        index = 0
        if person[0] == message.author:
            saidfrozen = False
            if message.content.lower() == "-frozen":
                print("they said -frozen")
                if not person[2]:
                    saidfrozen = True
                    print("first time saying it")
                    person[2] = True
                    await client.send_message(message.channel, "<@{0.author.id}> is frozen! DM them asking for proof, otherwise they will be banned from the server! Is this how it's supposed to work, Andrew? I'm not entirely sure I understand.".format(message))

            if not saidfrozen:
                if time.time() - person[1] < 210:
                    await client.send_message(message.author, "You are currently frozen. You will be banned in "+str(int(210) - int(time.time()-person[1]))+" seconds if you fail to provide evidence that you haven't cheated. Say -frozen in the server to alert the mods. If you already said -frozen, you aren't allowed to send it repeatedly. Wait for a DM from a mod.")
                    await client.delete_message(message)
                else:
                    del frozen[index]
        index += index


client.run('no token for you')
