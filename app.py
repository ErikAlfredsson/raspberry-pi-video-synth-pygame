
class App(object):	
	def __init__(self):
		super(App, self).__init__()

	def setup(screen, data):
		raise NotImplementedError		
	
	def draw(screen, data):
		raise NotImplementedError