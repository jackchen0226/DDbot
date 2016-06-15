import discord
import random

bot = discord.Client()
cmd_start = "+" #in case a command is added to change this, for example using !


def txt_save(file_name, username, inc_amt = 1):
	file = open(file_name, "r")
	data = file.readlines()

	board = {}
	for i in range(0, len(data)):
		if i % 2 == 0:
			board[data[i]] = int(data[i+1])

	if username + "\n" in board:
		board[username + "\n"] += inc_amt
	else:
		board[username + "\n"] = inc_amt

	v = board.items()
	data.clear()
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
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == bot.user:
		return

	if message.content.startswith(cmd_start + 'guess'):
		await bot.send_message(message.channel, "Okay, " + message.author.name + ', guess a number between 1 to 10')

		def guess_check(m):
			return m.content.isdigit()

		answer = random.randint(1, 10)
		print(answer) #Filthy cheaters

		guess = await bot.wait_for_message(timeout=5.0, author=message.author)

		if guess is None:
			fmt = 'Sorry, you took too long. It was {}.'
			await bot.send_message(message.channel, fmt.format(answer))
			return
		if int(guess.content) == answer:
			await bot.send_message(message.channel, 'You are right!')

			txt_save("guessing_game_scoreboard.txt", message.author.name)

		else:
			await bot.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))


	if message.content.startswith(cmd_start + "pizza"):
		#pizza
		await bot.send_message(message.channel, "https://images-1.discordapp.net/.eJwFwdtugjAAANB_4b0Q5CL41rDKVeQSqdkLYbSpbCAFShkz_vvOeSnr3Csn5SEEX06a1g0Nows4qKRb2nEmDefqkwpNpdFGdoSubIc5vHi1AyHukzuLjXmU5Tn8QUW7TeZ9qG23pK0ZGDjNbX06g8GBw14hU08X1wsjKrwqNFt6wGRC6NbhXoIi922LMGYEeOSAuM6X4xl-85GMW-IE39A66nLNjlUlcV3-TWBLfz_3rFH1jACx2nFZ3yIU71eEee0XMi6si8qfTHn_A2MwSWM.nP75fsEm6h7n1fYeThH6ZpNC-MI.png")


	if message.content.startswith(cmd_start + "logout"):
		await bot.send_message(message.channel, "Logging out...")
		await bot.logout()


	john_inv = cmd_start + "john"
	if message.content.startswith(john_inv):
		john_cmd = message.content 
		if john_cmd.endswith("start"):
			await bot.send_message(message.author, "What is your maximum amount of points you can hold at once?")
			
			cap = await bot.wait_for_message(timeout=7.5, author=message.author)

			if cap == None:
				await bot.send_message(message.author, "Response timed out")
			if int(cap.content) == 7 or 10:
				await bot.send_message(message.author, "Max cap sent to " + str(cap.content))
				
			else:
				await bot.send_message(message.author, "Invalid bet amount")
		elif john_cmd.endswith(john_cmd + "bet"):
			await bot.send_message(message.author, "Okay, how much?")

			def bet_check(x):
				return x.content.isdigit()

			bet = await bot.wait_for_message(timeout=5.0, author=message.author, check=bet_check)
			if bet == None:
				await bot.send_message(message.author, "Sorry, you took too long")
			else:
				txt_save("John_bets.txt", message.author.name, inc_amt = int(bet.content))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


#note that in order to run, the "token" must be replaced
#MTkwMjk2NTk0NTczMTY0NTQ1.CjprAw.rDP5z_CuVOWeb6wSnC8OdE1qK0M, bot token once I get OAuth2 working
bot.run("token")