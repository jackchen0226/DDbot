"""The main bot module containing :meth:`pizza` and :meth:`guess`.

Members
=======
"""

import discord
from discord.ext import commands
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
cmd_start = "+"
bot = commands.Bot(command_prefix=cmd_start, description=description)


def txt_save(file_name, username, inc_amt=1):
    file = open(file_name, "r")
    data = file.readlines()  # Gets list, named data, of all the lines form the text file.

    board = {}
    for i in range(0, len(data)):
        # Text file is saved as usernames on one line and their score right after the other.
        if i % 2 == 0:
            # Convert the list to dictionary
            board[data[i]] = int(data[i + 1])  # Convert the list to dictionary

    if username + "\n" in board:  # Each line when written has \n in order to create a line break.
        board[username + "\n"] += inc_amt
    else:
        board[username + "\n"] = inc_amt

    v = board.items()
    data.clear()

    # Convert dictionary back into list
    for i in v:
        for x in i:
            data.append(str(x))

    for i in range(0, len(data)):
        if not data[i].endswith("\n"):
            data[i] += "\n"

    file = open(file_name, "w")
    file.writelines(data)
    file.close()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def add(left: int, right: int):
    """Adds two numbers together."""
    await bot.say(left + right)


@bot.command()
async def roll(dice="1d20"):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)


@bot.command()
async def choose(*choices: str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))


@bot.command()
async def repeat(times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)


@bot.command()
async def joined(member: discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))


@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))


@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')


@bot.command(pass_context=True)
async def msg_test(ctx):
    """Purely for testing things"""
    print(ctx.message.author)
    await bot.send_message(ctx.message.author, "testering")


@bot.command()
async def pizza():
    """Gives a picture of pizza"""
    await bot.say(
        "https://images-1.discordapp.net/.eJwFwdtugjAAANB_4b0Q5CL41rDKVeQSqdkLYbSpbCAFShkz_vvOeSnr3Csn5SEEX06a1g0Nows4qKRb2nEmDefqkwpNpdFGdoSubIc5vHi1AyHukzuLjXmU5Tn8QUW7TeZ9qG23pK0ZGDjNbX06g8GBw14hU08X1wsjKrwqNFt6wGRC6NbhXoIi922LMGYEeOSAuM6X4xl-85GMW-IE39A66nLNjlUlcV3-TWBLfz_3rFH1jACx2nFZ3yIU71eEee0XMi6si8qfTHn_A2MwSWM.nP75fsEm6h7n1fYeThH6ZpNC-MI.png")


@bot.command()
async def logout():
    """Causes the bot to logout of Discord."""
    await bot.say("Logging out...")
    await bot.logout()


@bot.command(pass_context=True)
async def guess(ctx):
    """A simple guessing game."""
    await bot.say("Okay, {}, guess a number between 1 to 10".format(ctx.message.author.name))

    answer = random.randint(1, 10)
    print(answer)  # Filthy cheaters

    try:
        guess = await bot.wait_for_message(timeout=5.0, author=ctx.message.author)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await bot.say(fmt.format(answer))
            return
        guess_int = int(guess.content)
        print(guess_int)
        if guess_int == answer:
            await bot.say('You are right!')
            txt_save("guessing_game_scoreboard.txt", ctx.message.author.name)
        else:
            await bot.say('Sorry. It is actually {}.'.format(answer))
    except ValueError:
        await bot.say("That is not a number.")
        return


@bot.command(pass_context=True)
async def john(ctx, proc: str):
    """A betting system for a game called John."""
    if proc == "start":
        # bot.send_message(person, message) is used here for private messaging.
        await bot.send_message(ctx.message.author, "What is your maximum amount of points you can hold at once?")

        cap = await bot.wait_for_message(timeout=7.5)

        if cap is None:
            await bot.send_message(ctx.message.author, "Response timed out")
        if int(cap.content) == 7 or 10:
            await bot.send_message(ctx.message.author, "Max cap sent to " + str(cap.content))
        else:
            await bot.send_message(ctx.message.author, "Invalid bet amount")

    if proc == "bet":
        await bot.send_message(ctx.message.author, "Okay, how much?")

        def bet_check(x):
            return x.content.isdigit()

        try:
            bet = await bot.wait_for_message(timeout=5.0, author=ctx.message.author, check=bet_check)

            if bet is None:
                await bot.send_message(ctx.message.author, "Sorry, you took too long")
                return

            bet_test = int(bet.content)
            # Currently you can bet higher than the max amount, FIX THIS !!!!!!!!!!!
            await bot.send_message(ctx.message.author, "Okay, your current bet is set to" + str(bet.content))
            txt_save("John_bets.txt", ctx.message.author.name, inc_amt=int(bet.content))
        except ValueError:
            await bot.say("That is not a number.")


@bot.command(pass_context=True)
async def playsong(ctx, songname : str, file_ext="flac"):
    global voice
    global player
    if bot.is_voice_connected(ctx.message.server):
        pass
    else:
        voice = await bot.join_voice_channel(ctx.message.author.voice_channel)


    try:
        if player.is_playing():
            await bot.say(
                "A song is currently playing. Use {}queue add [\"filename\"] to add to the queue.".format(cmd_start))
        else:
            player = voice.create_ffmpeg_player(songname + "." + file_ext)
            player.start()           
    except NameError:
        player = voice.create_ffmpeg_player(songname + "." + file_ext)
        player.start()


@bot.command()
async def queue(queue_change=None, queue_add = "", file_ext="flac"):
    global queue
    global player
    if queue_change is None:
        temp_str = ""
        try:
            if len(queue) == 0:
                await bot.say("queue is empty!")
            else:
                for x in range(0, len(queue)):
                    temp_str += queue[x] + ". "
                if len(queue) == 1:
                    await bot.say("There is currently 1 item in the queue, {}".format(temp_str))
                else:
                    await bot.say("There are currently {} items in the queue".format(str(len(queue))))
                    await bot.say("Queue: " + temp_str)
        except Exception:
            queue = []
            await bot.say("Queue is empty!")
    elif queue_change == "add":
        if queue_add == "":
            await bot.say("You need to add a valid filename")
        else:
            queue.append(queue_add + "." + file_ext)
            await bot.say("Added {0}{3} to queue, there is now {1} items in queue".format(queue_add, str(len(queue)), file_ext))
    elif queue_change == "play" and not player.is_playing:
        while player.is_playing:
            player = voice.create_ffmpeg_player(queue[0])
            queue.pop([0])
            player.start()




@bot.command()
async def disconnect():
    """A simple command to disconnect from a voice channel."""
    try:
        await bot.say("Disconnecting from voice channel...")
        await voice.disconnect()
    except NameError:
        await bot.say("Bot is not in a voice channel!")


@bot.command()
async def volume(level):
    """Changes volume of the audio player, can set the level between 0 to 200 (0% and 200% respectively)"""
    player.volume = 0.1
    
@bot.command()
async def looptest():
    player.start()

@bot.command(pass_context=True)
async def rickroll(ctx):
    global voice
    voice = await bot.join_voice_channel(ctx.message.author.voice_channel)
    player = await voice.create_ytdl_player("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    player.start()
    player.volume = 0.1

# note that in order to run, the "token" must be replaced
bot.run("MTkwMjk2NTk0NTczMTY0NTQ1.Cmgoqw.0yyUwG_uRZKOz_5uxWJFkz7qCng")
