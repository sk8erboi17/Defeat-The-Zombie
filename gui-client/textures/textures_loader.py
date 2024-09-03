import pygame


class TextureLoader:
    def __init__(self, img_path, width, height):
        self.img_path = img_path
        self.width = width
        self.height = height

    def load(self):
        """
        Loads an image from the specified path and scales it to the given width and height.
        """
        img = pygame.image.load(self.img_path)
        scaled_image = pygame.transform.scale(img, (self.width, self.height))
        return scaled_image

    def flip(self, img, flip_x, flip_y):
        """
        Flips the given image horizontally and/or vertically.
        """
        return pygame.transform.flip(img, flip_x, flip_y)
