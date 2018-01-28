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
		self.size = 50
		self.height = screen.get_height() - self.size * 2
		self.draw_rect = pygame.Rect(int(screen.get_width() // 4), 0, int(screen.get_width() // 2 + self.size * 2), int(screen.get_height()))
	
	def draw(self, screen, data):
		for i in xrange(self.size * 3, self.height):			
			current_time = time.time()
			xpos = int(screen.get_width() // 2 + self.size * math.sin(i * .02 + current_time))

			color = (int(127 + 127 * math.sin(i * .01 + current_time)), 
				int(127 + 127 * math.sin(i * .011 + current_time)),
				int(127 + 127 * math.sin(i * .012 + current_time)))

			radius = int(50 + 40 * math.sin(i * .005 + current_time))
			pygame.gfxdraw.filled_circle(screen, xpos, i, radius, color)    			

		self.step += 0.025
		pygame.display.update(self.draw_rect)
		# pygame.display.flip()        