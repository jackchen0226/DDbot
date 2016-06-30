import discord
from discord.ext import commands
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='+', description=description)


def txt_save(file_name, username, inc_amt = 1):
    file = open(file_name, "r")
    data = file.readlines() #Gets list, named data, of all the lines form the text file.

    board = {}
    for i in range(0, len(data)):
        #Text file is saved as usernames on one line and their score right after the other.
        if i % 2 == 0:
            #Convert the list to dictionary 
            board[data[i]] = int(data[i+1]) #Convert the list to dictionary

    if username + "\n" in board: #Each line when written has \n in order to create a line break.
        board[username + "\n"] += inc_amt
    else:
        board[username + "\n"] = inc_amt

    v = board.items()
    data.clear()

    #Convert dictionary back into list
    for i in v:
        for x in i:
            data.append(str(x))

    for i in range(0, len(data)):
        if not data[i].endswith("\n"):
            data [i] = data[i] + "\n"

    file = open(file_name, "w")
    file.writelines(data)
    file.close()


@bot.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
@asyncio.coroutine
def add(left : int, right : int):
    """Adds two numbers together."""
    yield from bot.say(left + right)


@bot.command()
@asyncio.coroutine
def roll(dice="1d20"):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        yield from bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    yield from bot.say(result)



@bot.command()
@asyncio.coroutine
def choose(*choices : str):
    """Chooses between multiple choices."""
    yield from bot.say(random.choice(choices))


@bot.command()
@asyncio.coroutine
def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        yield from bot.say(content)


@bot.command()
@asyncio.coroutine
def joined(member : discord.Member):
    """Says when a member joined."""
    yield from bot.say('{0.name} joined in {0.joined_at}'.format(member))


@bot.group(pass_context=True)
@asyncio.coroutine
def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        yield from bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))


@cool.command(name='bot')
@asyncio.coroutine
def _bot():
    """Is the bot cool?"""
    yield from bot.say('Yes, the bot is cool.')


@bot.command(pass_context = True)
@asyncio.coroutine
def msg_test(ctx):
    """Purely for testing things"""
    print(ctx.message.author)
    yield from bot.send_message(ctx.message.author,"testering")

@bot.command()
@asyncio.coroutine
def pizza():
    """Gives a picture of pizza"""
    yield from bot.say("https://images-1.discordapp.net/.eJwFwdtugjAAANB_4b0Q5CL41rDKVeQSqdkLYbSpbCAFShkz_vvOeSnr3Csn5SEEX06a1g0Nows4qKRb2nEmDefqkwpNpdFGdoSubIc5vHi1AyHukzuLjXmU5Tn8QUW7TeZ9qG23pK0ZGDjNbX06g8GBw14hU08X1wsjKrwqNFt6wGRC6NbhXoIi922LMGYEeOSAuM6X4xl-85GMW-IE39A66nLNjlUlcV3-TWBLfz_3rFH1jACx2nFZ3yIU71eEee0XMi6si8qfTHn_A2MwSWM.nP75fsEm6h7n1fYeThH6ZpNC-MI.png")


@bot.command()
@asyncio.coroutine
def logout():
    """Causes the bot to logout of Discord."""
    yield from bot.say("Logging out...")
    yield from bot.logout()


@bot.command(pass_context = True)
@asyncio.coroutine
def guess(ctx):
    """A simple guessing game."""
    yield from bot.say("Okay, {}, guess a number between 1 to 10".format(ctx.message.author.name))

    answer = random.randint(1, 10)
    print(answer) #Filthy cheaters

    try:
        guess = yield from bot.wait_for_message(timeout=5.0, author=ctx.message.author)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            yield from bot.say(fmt.format(answer))
            return
        guess_int = int(guess.content)
        print(guess_int)
        if guess_int == answer:
            yield from bot.say('You are right!')
            txt_save("guessing_game_scoreboard.txt", ctx.message.author.name)
        else:
            yield from bot.say('Sorry. It is actually {}.'.format(answer))
    except ValueError:
        yield from bot.say("That is not a number.")
        return
        

@bot.command(pass_context = True)
@asyncio.coroutine
def john(ctx, proc: str):
    """A betting system for a game called John."""
    if proc == "start":
        #bot.send_message(person, message) is used here for private messaging. Messages to a server are using bot.say(message), equivalent to bot.send_message(channel, message)
        yield from bot.send_message(ctx.message.author, "What is your maximum amount of points you can hold at once?")
            
        cap = yield from bot.wait_for_message(timeout=7.5)

        if cap == None:
            yield from bot.send_message(ctx.message.author, "Response timed out")
        if int(cap.content) == 7 or 10:
            yield from bot.send_message(ctx.message.author, "Max cap sent to " + str(cap.content))                
        else:
            yield from bot.send_message(ctx.message.author, "Invalid bet amount")

    if proc == "bet":
        yield from bot.send_message(ctx.message.author, "Okay, how much?")

        def bet_check(x):
            return x.content.isdigit()

        try:
            bet = yield from bot.wait_for_message(timeout=5.0, author=ctx.message.author, check=bet_check)

            if bet == None:
                yield from bot.send_message(ctx.message.author, "Sorry, you took too long")
                return

            bet_test = int(bet.content)
            #Currently you can bet higher than the max amount, FIX THIS !!!!!!!!!!! 
            yield from bot.send_message(ctx.message.author, "Okay, your current bet is set to" + str(bet.content))
            txt_save("John_bets.txt", ctx.message.author.name, inc_amt = int(bet.content))
        except ValueError:
            yield from bot.say("That is not a number.")


#note that in order to run, the "token" must be replaced
bot.run("token")