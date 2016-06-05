import discord
import random

client = discord.Client()
cmd_start = "+" #in case a command is added to change this, for example using !


class bet_values():
	"""docstring for ClassName"""
	def __init__(self, username, max_cap, curr_val):
		self.username = username
		self.max_cap = max_cap
		self.curr_val = curr_val


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


	if message.content.startswith(cmd_start + "pizza"):
			await client.send_message(message.channel, "https://images-1.discordapp.net/.eJwFwdtugjAAANB_4b0Q5CL41rDKVeQSqdkLYbSpbCAFShkz_vvOeSnr3Csn5SEEX06a1g0Nows4qKRb2nEmDefqkwpNpdFGdoSubIc5vHi1AyHukzuLjXmU5Tn8QUW7TeZ9qG23pK0ZGDjNbX06g8GBw14hU08X1wsjKrwqNFt6wGRC6NbhXoIi922LMGYEeOSAuM6X4xl-85GMW-IE39A66nLNjlUlcV3-TWBLfz_3rFH1jACx2nFZ3yIU71eEee0XMi6si8qfTHn_A2MwSWM.nP75fsEm6h7n1fYeThH6ZpNC-MI.png")


	if message.content.startswith(cmd_start + "logout"):
			await client.send_message(message.channel, "Logging out...")
			await client.logout()


	if message.content.startswith(cmd_start + "john" + " start bet"):
		await client.send_message(message.author, "What is your maximum amount of points you can hold at once?")
		
		cap = await client.wait_for_message(timeout=7.5, author=message.author)

		if cap == None:
			await client.send_message(message.author, "Response timed out")
		if int(cap.content) == 7 or 10:
			await client.send_message(message.author, "Max cap sent to " + str(cap.content))
			betee = bet_values(message.author.name, cap.content, cap.content)
		else:
			await client.send_message(message.author, "Invalid bet amount")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


#note that in order to run, the 'token' must be replaced
client.run('moodhtaed@outlook.com',"BaconRocks42")
