# zc-cris
import pygame


class Ship():
    def __init__(self, screen, settings):
        '''初始化飞船的位置'''
        self.screen = screen
        self.settings = settings

        # 获取飞船位图的外接矩形和整个屏幕的外接矩形
        self.image = pygame.image.load('../images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将飞船放置在屏幕底部的中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.moving_right = False
        self.moving_left = False

        # 因为centerx无法存储小数，所以新建一个属性用于计算飞船的位置
        self.center = float(self.rect.centerx)

    def blitme(self):
        '''在指定位置上绘制飞船'''
        self.screen.blit(self.image, self.rect)

    def update(self):
        '''由飞船自己控制左右滑动,防止滑出屏幕'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.ship_speed_factor

        # 借助center属性更新centerx属性
        self.rect.centerx = self.center

    def ship_center(self):
        '''将飞船重新置于底部中央位置, 设置center属性即可，因为后面会调用update 方法的最后一句代码进行重绘'''
        self.center = self.screen_rect.centerx
