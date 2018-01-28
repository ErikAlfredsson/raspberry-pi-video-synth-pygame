from app import App
import pygame
import math
import time

class Circle(object):
    def __init__(self, x, y, color, size):
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def shrink(self):
        self.size -= 6 

class CircleDrawing(App):		
	def __init__(self):
		self.step = 0.0
		super(CircleDrawing, self).__init__()

	def setup(self, screen, data):
		print("Setting up CircleDrawing")		
		self.circle = Circle(int(screen.get_width() * 0.5), screen.get_height() * 0.5, (75, 50, 200), 50)
	
	def draw(self, screen, data):		
		color = (int(75 + 75 * math.sin(self.step * .5 + time.time())), 
				int(60 + 20 * math.sin(self.step * .11 + time.time())),
				int(75 + 50 * math.sin(self.step * .012 + time.time())))		

		y = screen.get_height() * 0.5 + math.sin(self.step + time.time()) * screen.get_height() * 0.5            
		self.circle.y = int(y)
		x = math.sin(self.step * 4 + time.time())                        
		circle_x = int(self.circle.x + (x * (screen.get_width() * 0.5)) * data["low_pass"])

		self.step += 0.05
		pygame.draw.circle(screen, color, (circle_x, self.circle.y), int(self.circle.size * (1 + data["magnitude"])))
		pygame.display.flip()
		# pygame.display.update(pygame.Rect(circle_x, self.circle.y, self.circle.size, self.circle.size))        