import praw
import links
import hidden # this is a file on my pc with hidden info such as the IP address of the bot


def main():
	reddit = praw.Reddit(
		client_id=hidden.BotClientId,
		client_secret=hidden.BotClientSecret,
		#password=hidden.BotPassword,
		user_agent="Bathtub Bot V0.1",
		#username="BathtubBot"
	)
	subreddit = reddit.subreddit("BathtubPaintedBrown")
	print("Logged in!")


	for submission in subreddit.stream.comments():
		processThis(submission)


def processThis(submission):
	if "u/bathtubbot" in submission.body.lower():
		print("Found a comment by " + submission.user)
		strippedComment = submission.body.lower().strip().strip('u/bathtubbot')
		replylink = None
		replyphrase = None

		# find the block
		for link in links.WikiLinks.keys():
			if link in strippedComment:
				replylink = links.WikiLinks[link]
				replyphrase = link
				break
		if replylink == None:
			print("No block or vanity found")
			return
		
		# reply
		replysuffix = "^(I am a bot, this action was done automatically, message me if you have any issues)"
		reply = ""
		if type(replylink) == type(["lol"]):
			reply = "I couldn't understand you, but I recognized the word " + replyphrase + ", which could be referring to...\n"
			for each in replylink:
				reply += each + "\n"
			reply += "Hopefully I was helpful"
		else:
			reply = "Here you go! \n" + replylink
		reply += replysuffix

		submission.reply(reply)


if __name__ == "__main__":
	main()