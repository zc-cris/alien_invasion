# zc-cris
import pygame.ftfont


class Button():
    def __init__(self, settings, screen, msg):
        '''初始化按钮的属性'''
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的其他尺寸和属性
        self.width, self.height = 200, 50
        self.button_color = (123, 123, 123)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮的rect 对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需要创建一次
        self.prep_msg(msg)

    def prep_msg(self, msg):
        '''将msg 渲染为图像，并使其在按钮上居中（了解即可）'''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        '''绘制按钮,然后绘制文本'''
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
