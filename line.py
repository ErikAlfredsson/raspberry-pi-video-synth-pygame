from app import App
import pygame
import math
import time

class Line(App):		
	def __init__(self):
		self.step = 0.0
		super(Line, self).__init__()

	def setup(self, screen, data):
		print("Setting up Line")			
		self.width = 10		
		self.rotation = 0		
		self.surf = pygame.Surface((screen.get_height(), screen.get_height()))
		self.start_pos = pygame.math.Vector2(self.surf.get_width() // 2, screen.get_height())
		self.end_pos = pygame.math.Vector2(self.surf.get_width() // 2, 0)
		self.surf_x = int(screen.get_width() // 2 - self.surf.get_width() // 2)		
	
	def draw(self, screen, data):
		color = (int(120 + 75 * math.sin(self.step * .5 + time.time())), 
				int(90 + 20 * math.sin(self.step * .11 + time.time())),
				int(75 + 75 * math.sin(self.step * .012 + time.time())))		

		self.surf.fill((0, 0, 0))

		pygame.draw.line(self.surf, color, self.start_pos, self.end_pos, self.width)		
		blitted_rect = screen.blit(self.surf, (self.surf_x, 0))		
		old_center = blitted_rect.center
		rotated_surf = pygame.transform.rotate(self.surf, self.rotation)		
		rotated_rect = rotated_surf.get_rect()
		rotated_rect.center = old_center

		screen.blit(rotated_surf, rotated_rect)

		# % 360 to keep the angle between 0 and 360.
		self.rotation = (self.rotation + 5) % 360
		self.step += 0.025
		pygame.display.update(blitted_rect)
		# pygame.display.flip()        