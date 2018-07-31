# zc-cris
import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet


def update_bullets(bullets, aliens, settings, screen, alien, game_stats, score_board):
    '''更新子弹列表（每个子弹的位置和子弹总数量）'''
    # 调用每颗子弹的update 方法
    bullets.update()
    # 从子弹列表中删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    # 子弹和外星人的碰撞检测
    check_alien_bullet_collisions(alien, aliens, bullets, screen, settings, game_stats, score_board)


def check_alien_bullet_collisions(alien, aliens, bullets, screen, settings, game_stats, score_board):
    '''检测每个子弹，判断每个外星人的位置是否和子弹的位置重合，如果重合，删除重合的子弹和外星人,返回每个子弹对应的碰撞alien列表的字典'''
    groupcollide = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # 如果击中外星人，就加分
    if groupcollide:
        # 字典的值就是一个个被击中的外星人的列表
        for aliens in groupcollide.values():
            game_stats.score += settings.alien_score * len(aliens)
            # 更新分数
            score_board.prep_score()
        # 更新最高分
        check_high_score(game_stats, score_board)
    # 如果外星人都被消灭了
    if len(aliens) == 0:
        # 删除所有的列表里的所有子弹
        bullets.empty()
        # 增加游戏难度
        settings.increase_speed()
        # 再度召唤外星人
        create_aliens(settings, screen, aliens, alien)


def check_high_score(game_stats, score_board):
    '''判断最高得分'''
    if game_stats.score > game_stats.high_score:
        game_stats.high_score = game_stats.score
        score_board.prep_high_score()


def key_down(event, ship, bullets, settings, screen):
    '''监视用户的键盘按下'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # 飞船发射子弹
        fire_bullet(bullets, screen, settings, ship)
        # 玩家/开发人员 可以通过按下q键退出游戏
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(bullets, screen, settings, ship):
    '''判断并发射子弹'''
    # 如果当前屏幕上的子弹数量不大于游戏规定的子弹数量
    if len(bullets) < settings.bullets_count_allowed:
        # 创建一颗子弹，放入到子弹列表中
        new_bullet = Bullet(settings, ship, screen)
        bullets.add(new_bullet)


def key_up(event, ship, bullets, settings, screen):
    '''监视用户的键盘弹起'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ship, bullets, settings, screen, game_stats, play_button, aliens, alien, score_board):
    '''监视用户的键盘和鼠标时间'''
    # 用户可以按下q退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            # 用户可以点击play 按钮开始游戏
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # 检查用户鼠标的坐标，确保点击的是play按钮
            check_play_button(game_stats, play_button, mouse_x, mouse_y, aliens, bullets, settings, screen, alien, ship,
                              score_board)

        # 通过控制飞船的标志位来使飞船自己移动
        elif event.type == pygame.KEYDOWN:
            key_down(event, ship, bullets, settings, screen)
        elif event.type == pygame.KEYUP:
            key_up(event, ship, bullets, settings, screen)


def check_play_button(game_stats, play_button, mouse_x, mouse_y, aliens, bullets, settings, screen, alien, ship,
                      score_board):
    '''在玩家点击play 按钮并且当前游戏是未激活状态才开始新游戏'''
    if not game_stats.game_active and play_button.rect.collidepoint(mouse_x, mouse_y):
        # 重置游戏动态设置
        settings.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏信息
        game_stats.game_active = True
        game_stats.reset_stats()

        score_board.prep_score()
        score_board.prep_ships()

        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人和飞船居中
        create_aliens(settings, screen, aliens, alien)
        ship.ship_center()


def update_screen(ship, bullets, settings, screen, aliens, game_stats, play_button, score_board):
    '''更新渲染屏幕'''
    # 每次while循环设置背景色
    screen.fill(settings.bg_color)
    # 绘制所有的子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 绘制飞船
    ship.blitme()
    # 绘制一群外星人
    aliens.draw(screen)
    # 绘制得分牌
    score_board.show_score()
    # 如果游戏处于非活动状态，就会绘制play按钮
    if not game_stats.game_active:
        play_button.draw_button()
    # 每次while循环绘制最新的屏幕画面
    pygame.display.flip()


def get_available_rows(settings, alien_height, ship_height):
    '''计算外星人的行数'''
    # 为了给飞船的射击留下空白，可用空间减去3倍的外星人高度和1倍的飞船高度
    available_y = settings.screen_height - (3 * alien_height) - ship_height
    # 每行外星人的高度应该是2倍外星人高度（避免太紧密）
    available_rows = int(available_y / (2 * alien_height))
    return available_rows


def create_aliens(settings, screen, aliens, alien):
    '''创建外星人群'''
    # 计算每行可用的空间和外星人总个数
    number_alien_x = get_available_alien_number(alien, settings, alien.rect.width)

    # 获取可用的行数
    available_rows = get_available_rows(settings, alien.rect.height, alien.rect.width)
    # 创建指定行数的外星人
    for row in range(available_rows):
        for alien_number in range(number_alien_x):
            create_alines_by_line(alien_number, aliens, screen, settings, row)


def create_alines_by_line(alien_number, aliens, screen, settings, row):
    '''创建一行外星人'''
    alien = Alien(screen, settings)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    # 第一个alien_width 就是我们空出来的左边的边框，每个alien占据两个alien_width的宽度
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    # 第一个alien_height 就是当前行的外星人的高度，加上每行空白和上一行外星人的高度（2个外星人高度）*行数（行数从0开始的）
    alien.rect.y = alien_height + 2 * alien_height * row
    aliens.add(alien)


def get_available_alien_number(alien, settings, alien_width):
    '''获取每行可用的外星人数量'''
    available_space_x = settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x


def check_alien_edges(settings, aliens):
    '''如果有外星人到达边缘，就采取响应的措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_aliens_direction(settings, aliens)
            break


def change_aliens_direction(settings, aliens):
    '''将所有外星人向下移动，并改变他们的左右移动方向'''
    for aline in aliens.sprites():
        aline.rect.y += settings.alien_drop_speed_factor
    settings.alien_direction *= -1


def update_aliens(screen, settings, aliens, ship, game_stats, bullets, alien, score_board):
    '''先判断，再改变aliens的位置'''
    check_alien_edges(settings, aliens)
    aliens.update()
    # 更新完外星人的位置后，检测是否和飞船发生碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, game_stats, screen, ship, aliens, bullets, alien, score_board)
    # 检测是否有外星人到达屏幕底部
    check_alien_bottom(settings, game_stats, screen, ship, aliens, bullets, alien, score_board)


def check_alien_bottom(settings, game_stats, screen, ship, aliens, bullets, alien, score_board):
    '''当外星人到达了屏幕底部时的处理方法'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船和外星人撞击一样处理
            ship_hit(settings, game_stats, screen, ship, aliens, bullets, alien, score_board)
            break


def ship_hit(settings, game_stats, screen, ship, aliens, bullets, alien, score_board):
    '''当外星人和飞船撞击后的处理方法'''
    # 将飞船可被撞击次数-1
    if (game_stats.allow_ship_destroy_count <= 0):
        pygame.mouse.set_visible(True)
        game_stats.game_active = False
    else:
        game_stats.allow_ship_destroy_count -= 1
        # 更新记分牌
        score_board.prep_ships()

        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人
        create_aliens(settings, screen, aliens, alien)
        ship.ship_center()

        # 暂停
        sleep(0.5)
