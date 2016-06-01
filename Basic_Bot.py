import discord
import random

client = discord.Client()
cmd_start = "+"

@client.event
async def on_message(message):
    # we do not want the client to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith(cmd_start + 'guess'):
        await client.send_message(message.channel, 'Guess a number between 1 to 10')

        def guess_check(m):
            return m.content.isdigit()

        guess = await client.wait_for_message(timeout=5.0, author=message.author, check=guess_check)
        answer = random.randint(1, 10)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await client.send_message(message.channel, fmt.format(answer))
            return
        if int(guess.content) == answer:
            await client.send_message(message.channel, 'You are right!')
        else:
            await client.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))

    if message.content.startswith(cmd_start + "logout"):
        await client.logout()

    if message.content.startswith(cmd_start + "pizza"):
        await client.send_message(message.channel, "https://images-1.discordapp.net/.eJwFwdtugjAAANB_4b0Q5CL41rDKVeQSqdkLYbSpbCAFShkz_vvOeSnr3Csn5SEEX06a1g0Nows4qKRb2nEmDefqkwpNpdFGdoSubIc5vHi1AyHukzuLjXmU5Tn8QUW7TeZ9qG23pK0ZGDjNbX06g8GBw14hU08X1wsjKrwqNFt6wGRC6NbhXoIi922LMGYEeOSAuM6X4xl-85GMW-IE39A66nLNjlUlcV3-TWBLfz_3rFH1jACx2nFZ3yIU71eEee0XMi6si8qfTHn_A2MwSWM.nP75fsEm6h7n1fYeThH6ZpNC-MI.png")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#note that in order to run, the actual password to DDbot's account must be replacing "password"
client.run('moodhtaed@outlook.com','password')
