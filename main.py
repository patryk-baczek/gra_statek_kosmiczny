import pygame
import random
import threading
import time
from kosmita import Kosmita
from pocisk import Pocisk

pygame.init()
pygame.display.set_caption("Gra")

SCREEN_WIDTH = 540
SCREEN_HEIGHT = 960

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 40)

background = pygame.image.load("mapa.png").convert()
przegrana_image = pygame.image.load("przegrana.png").convert()

def load_image(position):
    image = pygame.image.load("statek.png").convert()
    image.set_colorkey((255, 255, 255))
    rect = image.get_rect(center=position)
    return image, rect

player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 190]
player_image, player_rect = load_image(player_pos)

def movement(keys):
    if keys[pygame.K_a] and player_pos[0] > 10:
        player_pos[0] -= 5
    if keys[pygame.K_d] and player_pos[0] < SCREEN_WIDTH - 60:
        player_pos[0] += 5


kosmici = []

SPAWN_KOSMITA = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_KOSMITA, 2000)

pociski = []
score = 0
game_status = True

def przyspieszanie_kosmitow():
    while game_status:
        for kosmita in kosmici:
            kosmita.predkosc += 0.1
        time.sleep(0.5)

watek = threading.Thread(target=przyspieszanie_kosmitow)
watek.start()

while game_status:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_status = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_status = False
            if event.key == pygame.K_SPACE:
                pociski.append(Pocisk(player_pos[0] + 40, player_pos[1]))


        if event.type == SPAWN_KOSMITA:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT // 2)
            kosmici.append(Kosmita(x, y, SCREEN_WIDTH))

    movement(pygame.key.get_pressed())

    for kosmita in kosmici:
        kosmita.ruch()


    for pocisk in pociski[:]:
        pocisk.update()
        for kosmita in kosmici[:]:
            if pocisk.rect.colliderect(kosmita.rect):
                pociski.remove(pocisk)
                kosmici.remove(kosmita)
                score += 150
                break
        if pocisk.poza_ekranem():
            pociski.remove(pocisk)

    if len(kosmici) > 4:
        screen.blit(przegrana_image, (0, 0))

        font = pygame.font.SysFont(None, 60)
        score_text = font.render(f"Punkty: {score}", True, (255, 255, 0))
        text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_text, text_rect)

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    game_status = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        game_status = False



    screen.blit(background, (0, 0))
    screen.blit(player_image, player_pos)

    for pocisk in pociski:
        pocisk.draw(screen)

    for kosmita in kosmici:
        screen.blit(kosmita.obrazek, kosmita.rect)

    score_text = font.render(f"Punkty: {score}", True, (255, 255, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()