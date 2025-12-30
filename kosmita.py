import pygame
import random

class Kosmita:
    def __init__(self, x, y, szerokosc_okna):
        self.obrazek = pygame.image.load("kosmita.png").convert()
        self.obrazek.set_colorkey((255, 255, 255))
        self.obrazek = pygame.transform.scale(self.obrazek, (60, 60))

        self.rect = self.obrazek.get_rect(center=(x, y))
        self.predkosc = 1
        self.kierunek = random.choice([-1, 1])
        self.szerokosc_okna = szerokosc_okna

    def ruch(self):
        self.rect.x += self.predkosc * self.kierunek

        if self.rect.right >= self.szerokosc_okna:
            self.rect.right = self.szerokosc_okna
            self.kierunek = -1

        if self.rect.left <= 0:
            self.rect.left = 0
            self.kierunek = 1