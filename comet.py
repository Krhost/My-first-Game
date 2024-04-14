import pygame
import random


# créer une lcasse pour gérer cette comete
class Comet(pygame.sprite.Sprite):

    def __init__(self, comet_event):
        super().__init__()
        # l'inimage associé a cette comete
        self.image = pygame.image.load('assets/comet.png')
        self.rect = self.image.get_rect()
        self.velocity = random.randint(1, 4)
        self.rect.x = random.randint(20, 800)
        self.rect.y = - random.randint(0, 800)
        self.comet_event = comet_event

    def remove(self):
        self.comet_event.all_comets.remove(self)
        # jouer le son
        self.comet_event.game.soud_manager.play('meteorite')

        # si le nombre de comettes est de 0
        if len(self.comet_event.all_comets) == 0:
            # remttre la barre a 0
            self.comet_event.reset_percent()
            # apparaitre les monstres
            self.comet_event.game.start()

    def fall(self):
        self.rect.y += self.velocity

        # Tombe sur le sol
        if self.rect.y >= 520:
            # supprimer la comet
            self.remove()

            # si il n'y a plus de boule de feu
            if len(self.comet_event.all_comets):
                # remettre la jauge au départ
                self.comet_event.reset_percent()
                self.comet_event.fall_mode = False

        # verifie si la boule de feu touche le joueur
        if self.comet_event.game.check_collision(
                self, self.comet_event.game.all_players
        ):
            # retirer la boule de feu
            self.remove()
            # subir des degat
            self.comet_event.game.player.damage(20)
