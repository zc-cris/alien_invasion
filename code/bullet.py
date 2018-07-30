# zc-cris
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, settings, ship, screen):
        super().__init__()
        self.screen = screen
        # 借助pygame 创建一个矩形，然后定位子弹的初始位置
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 使用小数定位子弹的位置
        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed_facotr = settings.bullet_speed_factor

    def update(self):
        '''向屏幕上方移动子弹'''
        self.y -= self.speed_facotr
        self.rect.y = self.y

    def draw_bullet(self):
        '''借助pygame 在屏幕上绘制子弹'''
        pygame.draw.rect(self.screen, self.color, self.rect)
