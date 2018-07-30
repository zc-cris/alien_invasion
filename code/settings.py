# zc-cris

class Settings():
    '''存储游戏所有配置的类'''

    def __init__(self):
        '''初始化游戏的设置参数'''
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_speed_factor = 1.5
        self.allow_max_ship_destroy_count = 2

        # 子弹设置
        self.bullet_speed_factor = 3
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_count_allowed = 4

        # 外星人设置
        self.alien_speed_factor = 1
        # 设置外星人向下的速度
        self.alien_drop_speed_factor = 40
        # 设置外星人自动左右摇摆,alien_direction 为1 表示向右移动，如果为-1表示向左移动
        self.alien_direction = 1

