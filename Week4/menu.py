from config import *
from game import *
import pygame
import sys
import time


class Button():
    """ Class đại diện cho các nút bấm trong menu."""

    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
        Khởi tạo nút bấm.
        Args:
            image (pygame.Surface): Hình ảnh của nút.
            pos (tuple): Vị trí (x, y) của nút.
            text_input (str): Văn bản hiển thị trên nút.
            font (pygame.font.Font): Phông chữ của văn bản.
            base_color (str): Màu sắc cơ bản của văn bản.
            hovering_color (str): Màu sắc của văn bản khi di chuột qua.
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        Cập nhật và hiển thị nút trên màn hình.
        Args:
            screen (pygame.Surface): Bề mặt màn hình để hiển thị nút.
        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """
        Kiểm tra xem vị trí chuột có nằm trên nút không.
        Args:
            position (tuple): Vị trí (x, y) của chuột.
        Returns:
            bool: True nếu chuột nằm trên nút, False nếu không.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        """
        Thay đổi màu sắc văn bản khi di chuột qua nút.
        Args:
            position (tuple): Vị trí (x, y) của chuột.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(
                self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(
                self.text_input, True, self.base_color)


class Menu:
    """Class đại diện cho menu chính và các menu con của trò chơi."""

    def __init__(self):
        """ Khởi tạo menu chính và các menu con của trò chơi."""
        self.screen = screen
        self.MENU_TEXT = self.get_font(100).render(
            "MAIN MENU", True, "#b68f40")
        self.MENU_RECT = self.MENU_TEXT.get_rect(center=(500, 100))
        self.FINISHED_RECT = self.MENU_TEXT.get_rect(center=(600, 250))
        self.FINISHED_TEXT = self.get_font(70).render(
            "YOU WIN!!!", True, "#b68f40")
        self.PLAY_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(500, 250),
                                  text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.PRACTICE_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(500, 400),
                                      text_input="PRACTICE", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.QUIT_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(500, 700),
                                  text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.NORMAL_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(500, 250),
                                    text_input="NORMAL", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.HARD_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(500, 400),
                                  text_input="HARD", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.TUTORIAL_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(500, 550),
                               text_input="TUTORIAL", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.GAMEOVER_TEXT = self.get_font(
            100).render("GAME OVER", True, "#b68f40")
        self.GAMEOVER_RECT = self.GAMEOVER_TEXT.get_rect(center=(500, 100))
        self.CONGRAT_TEXT = self.get_font(60).render(
            "CONGRATULATIONS", True, "#b68f40")
        self.CONGRAT_RECT = self.CONGRAT_TEXT.get_rect(center=(500, 100))
        self.BACK_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(500, 550),
                                  text_input="BACK", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.color = YELLOW

    def get_font(self, size):
        """
        Trả về phông chữ với kích thước mong muốn.
        Args:
            size (int): Kích thước phông chữ.
        Returns:
            pygame.font.Font: Phông chữ với kích thước đã cho.
        """
        return pygame.font.Font("assets/font.ttf", size)

    def countdown(self, i):
        """
        Hiển thị đếm ngược trên màn hình trước khi bắt đầu mỗi cấp độ.
        Args:
            i (int): Số cấp độ hiện tại.
        """
        for j in range(3, -1, -1):
            screen.fill("black")  # Điền màu nền đen
            text = font.render(str(j), True, "white")
            text_rect = text.get_rect(center=(500, 350))
            screen.blit(text, text_rect)
            if j == 0:
                screen.fill("black")  # Điền màu nền đen
                pygame.display.flip()
            else:
                pygame.display.flip()
                time.sleep(1)  # Chờ 1 giây
        text = font.render(f"Level {i}", True, "white")
        text_rect = text.get_rect(center=(500, 350))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(1)  # Chờ 1 giây

    def choose_difficulty(self, controller, color):
        """
        Chọn độ khó của trò chơi và bắt đầu các cấp độ.
        Args:
            controller (Controller): Đối tượng điều khiển trạng thái trò chơi.
            color (str): Màu sắc của chế độ chơi.
        """
        controller.image_mode = color
        while controller.lv <= 3:
            self.countdown(controller.lv)
            a = Game()
            a.setup(color)
            if controller.running is False:
                controller.lv = 1
                break
            controller.lv += 1
        controller.running = False
        if controller.gameover is True:
            self.gameover()
        elif not controller.gameover and not controller.congrat:
            self.main_menu(controller)
        else:
            self.congratulations()

    def start_game(self, controller):
        """
        Bắt đầu trò chơi với chế độ đã chọn (Bình thường hoặc Khó).
        Args:
            controller (Controller): Đối tượng điều khiển trạng thái trò chơi.
        """
        while True:
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            self.screen.blit(pygame.transform.scale(BG, (1000, 820)), (0, 0))
            self.screen.blit(self.MENU_TEXT, self.MENU_RECT)
            for button in [self.NORMAL_BUTTON, self.HARD_BUTTON, self.BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.NORMAL_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.choose_difficulty(controller, YELLOW)
                    elif self.HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.choose_difficulty(controller, WHITE)
                    elif self.BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.main_menu(controller)

            pygame.display.update()

    def main_menu(self, controller):
        """
        Hiển thị menu chính và điều khiển các hành động của nút bấm.
        Args:
            controller (Controller): Đối tượng điều khiển trạng thái trò chơi.
        """
        while True:
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            self.screen.blit(pygame.transform.scale(BG, (1000, 820)), (0, 0))
            self.screen.blit(self.MENU_TEXT, self.MENU_RECT)
            for button in [self.PLAY_BUTTON, self.PRACTICE_BUTTON, self.QUIT_BUTTON, self.TUTORIAL_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        controller.mode = 'PLAY'
                        self.start_game(controller)
                    elif self.PRACTICE_BUTTON.checkForInput(MENU_MOUSE_POS):
                        controller.mode = 'PRACTICE'
                        self.start_game(controller)
                    elif self.QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
                    elif self.TUTORIAL_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.tutorial()

            pygame.display.update()

    def tutorial(self):
        """
        Hiển thị màn hình hướng dẫn.
        """
        while True:
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            self.screen.blit(pygame.transform.scale(BG, (1000, 850)), (0, 0))

            TUTORIAL_TEXT = self.get_font(60).render(
                "TUTORIAL", True, "#b68f40")
            TUTORIAL_RECT = TUTORIAL_TEXT.get_rect(center=(500, 100))

            # Hướng dẫn chi tiết
            INSTRUCTIONS_TEXT = [
                "1. Use the mouse to control the game.",
                "2. Click on buttons to perform actions.",
                "3. Complete 3 levels to win.",
                "Game Rules for Turn On The Lights:",
                "1. Place light bulbs in empty cells to illuminate the grid.",
                "2. A light bulb illuminates its entire row and column ",
                "until it hits a wall.",
                "3. A number in a cell indicates how many light bulbs",
                "must be adjacent to it.",
                "4. No light bulb can illuminate another light bulb.",
                "5. Light up the entire grid without breaking any rules."
            ]

            # Hiển thị từng dòng hướng dẫn
            for i, line in enumerate(INSTRUCTIONS_TEXT):
                line_text = self.get_font(16).render(line, True, "#d7fcd4")
                line_rect = line_text.get_rect(topleft=(20, 200 + i * 40))
                self.screen.blit(line_text, line_rect)

            self.screen.blit(TUTORIAL_TEXT, TUTORIAL_RECT)

            # Đặt nút BACK ở phía dưới của màn hình để không đè lên các quy tắc
            self.BACK_BUTTON.rect.center = (500, 750)
            self.BACK_BUTTON.text_rect.center = (500, 750)
            self.BACK_BUTTON.changeColor(MENU_MOUSE_POS)
            self.BACK_BUTTON.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.main_menu(controller)

            pygame.display.update()

    def gameover(self):
        """
        Hiển thị màn hình Game Over.
        """
        while True:
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            self.screen.blit(pygame.transform.scale(BG, (1000, 820)), (0, 0))
            self.screen.blit(self.GAMEOVER_TEXT, self.GAMEOVER_RECT)
            self.QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
            self.QUIT_BUTTON.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def congratulations(self):
        """
        Hiển thị màn hình Chúc mừng khi người chơi chiến thắng.
        """
        while True:
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            self.screen.blit(pygame.transform.scale(BG, (1000, 820)), (0, 0))
            self.screen.blit(self.CONGRAT_TEXT, self.CONGRAT_RECT)
            self.screen.blit(self.FINISHED_TEXT, self.FINISHED_RECT)
            self.QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
            self.QUIT_BUTTON.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
