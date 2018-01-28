from app import App
import pygame
import math
import time

class Snake(App):		
	def __init__(self):
		self.step = 0.0
		super(Snake, self).__init__()

	def setup(self, screen, data):
		print("Setting up Snake")				
	
	def draw(self, screen, data):
		# screen.fill((0,0,0))

		for i in range(screen.get_height() - self.circle.size):
			y = screen.get_height() * 0.5 + math.sin(self.step) * screen.get_height() * 0.5
			self.circle.y = int(y)
			x = math.sin(self.step * 4 + 0.5)                        			
			xpos = int(screen.get_width() // 2 + 100 * math.sin(i * .02 + time.time()))

			color = (int(127 + 127 * math.sin(i * .01 + time.time())), 
				int(127 + 127 * math.sin(i * .011 + time.time())),
				int(127 + 127 * math.sin(i * .012 + time.time())))

			# radius = int(50 + 40 * math.sin(i * .005 + time.time()))
			radius = int(self.circle.size * max(0.3, data["low_pass"]))
			pygame.gfxdraw.filled_circle(screen, xpos, i, radius, color)    

		self.step += 0.1
		pygame.display.flip()        