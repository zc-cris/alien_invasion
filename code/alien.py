# zc-cris
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, screen, settings):
        '''初始化外星人，并设置其起始位置'''
        super().__init__()
        self.settings = settings
        self.screen = screen
        # 加载外星人的位图，并且设置rect属性
        self.image = pygame.image.load("../images/alien.bmp")
        self.rect = self.image.get_rect()

        # 每个外星人都在屏幕的左上角的位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        '''在指定位置上绘制外星人'''
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        '''根据坐标检测外星人是否已经移动到了屏幕边缘'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <=  0:
            return True

    def update(self):
        '''控制外星人左右的移动，方向由alien_direction 控制（1 表示右移，-1表示左移）'''
        self.x += self.settings.alien_speed_factor*self.settings.alien_direction
        self.rect.x = self.x
