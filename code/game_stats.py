# zc-cris

class GameStats():
    '''追踪统计游戏的信息'''

    def __init__(self, settings):
        self.settings = settings
        self.allow_ship_destroy_count = 0
        self.reset_stats()
        self.game_active = False
        # 任何情况下都不应重置最高分(除了当前得分打破了最高记录)
        self.high_score = 0

    def reset_stats(self):
        '''初始化在游戏运行期间可能变化的统计信息'''
        self.allow_ship_destroy_count = self.settings.allow_max_ship_destroy_count
        # 得分信息
        self.score = 0
