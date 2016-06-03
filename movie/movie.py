class Movie():
	"""movie data structure for holding related information """
	def __init__(self, poster_image_url,trailer_youtube_url,story,title):
		self.poster_image_url = poster_image_url
		self.trailer_youtube_url = trailer_youtube_url
		self.story = story
		self.title = title