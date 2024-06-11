import pygame
pygame.init()
screen = pygame.display.set_mode((1000, 820))
pygame.display.set_caption("Menu")
BG = pygame.image.load("assets/Background.png")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 102, 102)
GRAY = (105, 105, 105)
YELLOW = (255, 255, 30)
# kích thước tính bằng pixel cho mỗi hình vuông
WIDTH = 40
HEIGHT = 40

# kích thước cho đường viền phân chia bảng
SQUARE_WIDTH = 2
# kích thước màn hình mặc định (width x height)
WINDOWS = [1000, 820]
image = pygame.image.load('assets/yellow_bulb.png').convert()    # đèn vàng
image2 = pygame.image.load('assets/red_bulb.png').convert()  # đèn đỏ
font = pygame.font.Font(None, 74)  # Menu
"""
    Các thông số của các phần tử thuộc dictionary levels:
    [lv_size, start, end]
    Trong đó: 
    lv_size: kích thước màn chơi (lv_size * lv_size) 
    start, end: khoảng giá trị của số ô đen trong màn chơi
"""
levels = {1: [7, 15, 17], 2: [10, 35, 40], 3: [15, 84, 88]}


class Control:
    def __init__(self):
        self.lv = 1
        self.running = True
        self.mode = None
        self.solution_clicked = False
        self.gameover = False
        self.image_mode = YELLOW
        self.congrat = False


controller = Control()