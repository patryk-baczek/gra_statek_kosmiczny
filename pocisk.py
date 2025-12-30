import pygame

class Pocisk:
    def __init__(self, x, y):
        self.obrazek = pygame.image.load("pocisk.png").convert_alpha()
        self.obrazek.set_colorkey((255, 255, 255))
        self.predkosc = 8

        self.rect = self.obrazek.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= self.predkosc

    def draw(self, ekran):
        ekran.blit(self.obrazek, self.rect)

    def poza_ekranem(self):
        return self.rect.bottom < 0