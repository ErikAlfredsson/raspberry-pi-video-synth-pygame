from app import App
import pygame
import math
import time


class GridItem(object):
    def __init__(self, surface, x, y):
        self.surface = surface
        self.x = x
        self.y = y


class Line(App):
    def __init__(self):
        self.step = 0.0
        self.grid_items = []
        super(Line, self).__init__()

    def setup(self, screen, data):
        print("Setting up Line")
        self.rotation = 0
        self.filter_factor = 0.05
        self.filtered_magnitude = 0
        self.background_color = (153, 153, 0)
        self.line_color = (24, 24, 0)
        self.clockwise_rotation = True

        vertical_items = 3
        grid_size = screen.get_height() / vertical_items
        horizontal_items = int(screen.get_width() // grid_size)

        for i in range(0, vertical_items):
            for j in range(0, horizontal_items):
                surface = pygame.Surface((grid_size, grid_size))
                x = grid_size * j
                y = grid_size * i
                item = GridItem(surface, x, y)

                self.grid_items.append(item)

        print("{} grid items".format(len(self.grid_items)))

    def draw(self, screen, data):
        self.filtered_magnitude = (
            self.filter_factor * self.filtered_magnitude
            + (1.0 - self.filter_factor) * data["magnitude"]
        )

        for index, grid_item in enumerate(self.grid_items):
            start_pos = (
                grid_item.surface.get_width() // 2,
                grid_item.surface.get_height(),
            )  # pygame.math.Vector2(grid_width // 2, grid_height)
            end_pos = (
                grid_item.surface.get_width() // 2,
                0,
            )  # pygame.math.Vector2(grid_width // 2, 0)
            grid_item.surface.fill(self.background_color)

            pygame.draw.line(grid_item.surface, self.line_color, start_pos, end_pos, 5)
            blitted_rect = screen.blit(grid_item.surface, (grid_item.x, grid_item.y))

            old_center = blitted_rect.center
            rotated_surf = pygame.transform.rotate(grid_item.surface, self.rotation)
            rotated_rect = rotated_surf.get_rect()
            rotated_rect.center = old_center

            screen.blit(rotated_surf, rotated_rect)

        if data["onset"]:
            self.clockwise_rotation = not self.clockwise_rotation

        # delta_rotation = 0.25 #+ (5 * self.filtered_magnitude)
        delta_rotation = 0.25 + 20 * self.filtered_magnitude
        delta_rotation = delta_rotation if self.clockwise_rotation else -delta_rotation

        self.rotation = (self.rotation + delta_rotation) % 360
        self.step += 0.025
        # pygame.display.update(blitted_rect)
        pygame.display.flip()
