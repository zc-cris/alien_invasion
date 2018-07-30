# zc-cris
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from alien import Alien
from game_stats import GameStats
from button import Button


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("狙击外星人")
    ship = Ship(screen, settings)
    alien = Alien(screen, settings)
    game_stats = GameStats(settings)
    play_button = Button(settings, screen, 'Play')
    # 创建一个用于存储子弹的编组
    bullets = Group()
    # 创建一个用于存储外星人的编组
    aliens = Group()
    gf.create_aliens(settings, screen, aliens, alien)

    # 从子弹列表中删除消失的子弹
    # 开始游戏的主旋律
    while 1:
        # 监视用户的键盘和鼠标时间
        gf.check_events(ship, bullets, settings, screen, game_stats, play_button, aliens, alien)
        # 只有游戏处于激活状态（飞船最大销毁次数不等于0），才会更新各种游戏元素
        if game_stats.game_active:
            ship.update()
            # 更新子弹列表（更新子弹位置和数量）
            gf.update_bullets(bullets, aliens, settings, screen, alien)
            # 更新外星人列表（外星人的位置）
            gf.update_aliens(screen, settings, aliens, ship, game_stats, bullets, alien)
        # 更新屏幕的渲染
        gf.update_screen(ship, bullets, settings, screen, aliens, game_stats, play_button)


run_game()
