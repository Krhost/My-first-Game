import pygame
import math
from game import Game
pygame.init()

# definir une clock
clock = pygame.time.Clock()
FPS = 300

# generer la fenetre de notre jeu
pygame.display.set_caption("Comet fall Game")
screen = pygame.display.set_mode((1080, 750))

# importer l'image background
background = pygame.image.load('assets/bg.jpg')

# importter charger notre bannière
banner = pygame.image.load('assets/banner.png')
banner = pygame.transform.scale(banner, (500, 500))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)

# import charger noter bouton pour lancer la partie
play_buton = pygame.image.load('assets/button.png')
play_buton = pygame.transform.scale(play_buton, (400, 150))
play_buton_rect = play_buton.get_rect()
play_buton_rect.x = math.ceil(screen.get_width() / 3.33)
play_buton_rect.y = math.ceil(screen.get_height() / 2)

# charger notre jeu
game = Game()

running = True

# bouvle tant que cette condition est vrai
while running:

    # appliquer l'arrier plan
    screen.blit(background, (0, -200))

    # verifier si notre jeu a commencé
    if game.is_playing:
        # declencher les instruction de la partie
        game.update(screen)
    # verifier si le jeu n'a pas commencé
    else:
        # ajouter le home screen
        screen.blit(play_buton, play_buton_rect)
        screen.blit(banner, banner_rect)

    # mettre a jour
    pygame.display.flip()

    # si le joueur ferme cette fenetre
    for event in pygame.event.get():
        # que l'evenement est fermeture de fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture du jeu")
        # detecter deplacement au clavier
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            # detecter si la touche espace est déclenchée pour lancer le projectile
            if event.key == pygame.K_SPACE:
                game.player.launch_projectile()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # verification pour savoir si la souris est sur le boudon
            if play_buton_rect.collidepoint(event.pos):
                # mettre le jeu en mode "lancé"
                game.start()
                # jouer le son
                game.soud_manager.play('click')
    # fixer le nombre de fps
    clock.tick(FPS)
