import json
import twitter
import json
import random

class Actor(object):
	def __init__(self,path="../auth.json"):
			keys = json.loads(file(path).read())

			auth = twitter.OAuth(keys['OAUTH_TOKEN'], keys['OAUTH_TOKEN_SECRET'],
                            keys['APP_KEY'], keys['APP_SECRET'])

			self.api = twitter.Twitter(auth=auth)

	def unfollow(self, count = 1):
		bad_friends = json.load(open('../bad_friends.json'))
		for i in range(count):
			if len(bad_friends) > 0:
				usr_id = bad_friends.pop()
				print 'Destroying friendship: ' + str(usr_id)
				self.api.friendships.destroy(user_id = usr_id)
		json.dump(bad_friends, open('../bad_friends.json','wb'))
		return count     # no. api calls

	def follow(self, favoritetwt = True, count = 1):
		new_friends = json.load(open('../new_friends.json'))
		for i in range(count):
			if len(new_friends) > 0:
				usr_id = new_friends.pop()
				print 'Created friendship: ' + str(usr_id)
				self.api.friendships.create(user_id = usr_id)
				if favoritetwt:
					status = self.api.statuses.user_timeline(user_id=usr_id, count = 1)[0]  # can be extended to favorite random twt
					to_favorite = json.load(open('../to_favorite.json'))
					json.dump(to_favorite.append(status['id']), open('../to_favorite.json', 'wb'))
		json.dump(new_friends, open('../new_friends.json','wb'))
		calls = count 
		if favoritetwt:
			calls += count
		return calls  # no. api calls

	def favoritePost(self, count = 1):  # Error in api... ?
		to_favorite = json.load(open('../to_favorite.json'))
		for i in range(count):
			if len(to_favorite) > 0:
				status_id = to_favorite.pop()
				print 'Favoriting status: ' + str(status_id)
				self.api.favorites.create(_id = status_id)
		json.dump(to_favorite, open('../to_favorite.json', 'wb'))
		return count # no. api calls

	def postTwt(self):
		twts = json.load(open('../to_tweet.json'))
		if len(twts) > 0:
			twt = twts.pop()
			print 'Posting twt: ' + twt
			self.api.statuses.update(status = twt)
		json.dump(twts, open('../to_tweet.json','wb'))
		return 1  # no. api calls
