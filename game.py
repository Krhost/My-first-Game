import pygame

from player import Player
from monster import Mummy, Alien
from comet_event import CometFallEvent
from sounds import SoundManager


class Game:

    def __init__(self):
        # definir si notre jeu a commencé ou no,
        self.is_playing = False
        # generer notre joeur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        # gerer le son
        self.soud_manager = SoundManager()
        # generer l'evenement
        self.comet_event = CometFallEvent(self)
        # goupe de monstre
        self.all_monsters = pygame.sprite.Group()
        # mettre le score a 0
        self.score = 0
        self.pressed = {}


    def start(self):
        self.is_playing = True
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)

    def game_over(self):
        # remettre le jeu à neuf, retirer les monstres, remettre le joueur a 100 point de vie
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.comet_event.reset_percent()
        self.is_playing = False
        self.score = 0
        # jouer le son
        self.soud_manager.play('game_over')

    def add_score(self, points = 10):
        self.score += points

    def update(self, screen):
        # afficher le score sur l'ecran
        font =  pygame.font.SysFont("monospace", 16,)
        score_text = font.render(f"Score : {self.score}", 1, (0, 0, 0))
        screen.blit(score_text, (20, 20))

        # appliquer l'image de mon joeur
        screen.blit(self.player.image, self.player.rect)

        # actualiser la barre de vie du joueur
        self.player.update_health_bar(screen)

        # actualiser la barre d'evenement
        self.comet_event.update_bar(screen)

        # actualiser l'animation du joeur
        self.player.update_animation()

        # recupere les projectiles du joeur
        for projectile in self.player.all_projectiles:
            projectile.move()

        # recuperer les monstres de notre jeu
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update()

        # recuperer les comtes de notre
        for comet in self.comet_event.all_comets:
            comet.fall()

        # appliquer l'ensemble des images de mon groupe de projectiles
        self.player.all_projectiles.draw(screen)

        # applier l'ensemble des images de mon groupe de montre
        self.all_monsters.draw(screen)

        # appliquer l'esnsemble des images de mon groupe de comettes
        self.comet_event.all_comets.draw(screen)

        # verifier si le joueur souhaite aller a gauche ou a droite
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.mouve_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.mouve_left()

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self, monster_class_name):
        self.all_monsters.add(monster_class_name.__call__(self))
