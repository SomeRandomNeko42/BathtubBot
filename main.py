import praw
import links
import hidden # this is a file on my pc with hidden info such as the IP address of the bot


def main():
	reddit = praw.Reddit(
		client_id=hidden.BotClientId,
		client_secret=hidden.BotClientSecret,
		password=hidden.BotPassword,
		user_agent="Bathtub Bot V0.1",
		username="BathtubBot"
	)
	subreddit = reddit.subreddit("BathtubPaintedBrown")
	print(reddit.user.me().name + " logged in successfully")
	# Sort the list so that we dont have to worry about overlap
	newWikiLinks = dict(sorted(links.WikiLinks.items()).reverse())


	for submission in subreddit.stream.comments():
		processThis(submission, newWikiLinks)


def processThis(submission, wikLinks):
	if "u/bathtubbot" in submission.body.lower():
		print("Found a comment by " + submission.author.name)
		strippedComment = submission.body.lower().strip().strip('u/bathtubbot')
		replylink = None
		replyphrase = None
		reply = ""
		replysuffix = "\n\n^(I am a bot, this action was done automatically, message me if you have any issues)"

		# find the block
		for link in wikLinks:
			if link in strippedComment:
				replylink = wikLinks[link]
				replyphrase = link
				break
		if replylink == None:
			print("No block or vanity found")
			reply = "Sorry, i couldnt find anything in your comment to link to"
			reply += replysuffix
			submission.reply(reply)
			return
		
		# reply
		if type(replylink) == type(["lol"]):
			reply = "I couldn't understand you completely, but I recognized the word " + replyphrase + ", which could be referring to...\n"
			for each in replylink:
				reply += each + "\n\n"
			reply += "Hopefully I was helpful"
		else:
			reply = "Here you go! \n\n" + replylink
		reply += replysuffix

		submission.reply(reply)


if __name__ == "__main__":
	main()