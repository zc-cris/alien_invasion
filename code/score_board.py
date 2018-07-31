# zc-cris
import pygame.ftfont
from pygame.sprite import Group

from ship import Ship


class ScoreBoard():
    '''显示得分信息的类'''

    def __init__(self, settings, screen, game_stats):
        self.settings = settings
        self.game_stats = game_stats
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 显示得分信息使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始得分图像
        self.prep_score()
        # 准备最高分图像
        self.prep_high_score()
        # 准备飞船图像
        self.prep_ships()

    def prep_score(self):
        '''将得分转换为图像'''
        # 将得分圆整化
        round_score = round(self.game_stats.score, -1)
        score_str = "{:,}".format(round_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # 将得分放在屏幕的右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        '''在屏幕上显示得分'''
        self.screen.blit(self.score_image, self.score_rect)
        # 显示最高分
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # 绘制飞船
        self.ships.draw(self.screen)

    def prep_high_score(self):
        '''最高分的图像'''
        high_score = round(self.game_stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)

        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)

        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_ships(self):
        '''显示还剩下多少飞船'''
        self.ships = Group()
        for ship_number in range(self.game_stats.allow_ship_destroy_count):
            ship = Ship(self.screen, self.settings)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 3
            self.ships.add(ship)
