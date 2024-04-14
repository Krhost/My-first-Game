import pygame
from projectile import Projectile
import animation


# creer notre joeur
class Player(animation.AnimateStripe):

    def __init__(self, game):
        super().__init__('player')
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 25
        self.velocity = 5
        self.all_projectiles = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500

    def damage(self, amout):
        if self.health - amout > amout:
            self.health -= amout
        else:
            # si le joueur n'a plus de points de vie
            self.game.game_over()

    def update_animation(self):
        self.animate()

    def update_health_bar(self, surface):
        # dessiner notre barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 50, self.rect.y + 20, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 50, self.rect.y + 20, self.health, 5])

    def launch_projectile(self):
        # creer une nouvelle instance de la classe Projectile
        self.all_projectiles.add(Projectile(self))
        # demarer l'animation du lancer
        self.start_animation()
        # jouer le son
        self.game.soud_manager.play('tir')

    def mouve_right(self):
        # si le joueur  n'est pas en collision
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity

    def mouve_left(self):
        self.rect.x -= self.velocity
