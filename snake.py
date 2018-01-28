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
		self.filter_factor = 0.005
		self.filtered_magnitude = 0
	
	def draw(self, screen, data):
		screen.fill((0, 0, 0))		
		start = self.size * 3
		end = self.height
		num_circles = end - start

		self.filtered_magnitude = self.filter_factor * self.filtered_magnitude + (1.0 - self.filter_factor) * data["magnitude"]		

		for i in xrange(start, end):			
			current_time = self.step
			xpos = int(screen.get_width() // 2 + self.size * math.sin(i * .02 + current_time))

			color = (int(127 + 127 * math.sin(i * (.01 + 0.02 * self.filtered_magnitude) + current_time)), 
				int(127 + 127 * math.sin(i * .011 + current_time)),
				int(127 + 127 * math.sin(i * .012 + current_time)))

			normalized_index = float(i - start) / float(num_circles)
			# radius = int(50 + 40 * math.sin(i * .005 + current_time))				
			radius = int(self.size + (self.size * 0.5 + (1 - normalized_index) * self.size * 0.5) * data["low_pass"])
			pygame.gfxdraw.filled_circle(screen, xpos, i, radius, color)    									

		self.step += 0.025 + 0.25 * self.filtered_magnitude
		pygame.display.update(self.draw_rect)		      