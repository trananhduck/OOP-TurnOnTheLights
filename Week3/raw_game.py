import pygame
from Board import *
from Squares import *


class Game:

    def __init__(self):
        """
        Tạo mã RGB để tham chiếu màu và các hằng số cho cài đặt cửa sổ
        """
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.red = (255, 102, 102)
        self.gray = (105, 105, 105)
        self.yellow = (255, 255, 30)
        # kích thước tính bằng pixel cho mỗi hình vuông
        self.width = 40
        self.height = 40

        # kích thước cho đường viền phân chia bảng
        self.square_with = 2
        # kích thước màn hình mặc định (width x height)
        self.windows = [380, 450]
        # bắt đầu hiển thị khi đối tượng được tạo
        self.screen = pygame.display.set_mode(self.windows)
        self.image = pygame.image.load(
            'assets/yellow_bulb.png').convert()    # đèn vàng
        self.image2 = pygame.image.load(
            'assets/red_bulb.png').convert()  # đèn đỏ

    def setup(self):
        """
        Phương thức không có tham số; tạo ra một ví dụ có thể giải quyết được.
        """
        board = Board()
        board.generate_white()
        board.generate_black()
        board.generate_edges()
        board.create_grid()
        board.assign_number()
        board.remove_bulbs()
        board.verify(board.get_supervise())
        board.remove_bulbs()

        # Khởi tạo Pygame và tiêu đề
        pygame.init()
        pygame.display.set_caption("Turn On The Lights")

        # 'save_user_answers' chuyển đổi giữa hiển thị/ẩn giải pháp trong trò chơi và câu trả lời của người chơi
        # 'solution_mode' cho biết Người chơi hiện có đang xem giải pháp trong trò chơi hay không
        save_user_answers = True
        solution_mode = False
        win = False

        # lưu những đáp án của người chơi dưới dạng Dictionary
        user_answers = dict()
        # Giữ vòng lặp của trò chơi tiếp tục chạy cho đến khi màn chơi vẫn tồn tại
        # hoặc nếu người chơi gửi giải pháp đã được xác minh
        while True:
            for event in pygame.event.get():

                # lấy tọa độ chuột của Người chơi khi nhấp vào màn hình
                coordinates = pygame.mouse.get_pos()
                # Phạm vi các nút submit và solution
                submit = 200 <= coordinates[0] <= 200 + \
                    110 and 370 <= coordinates[1] <= 370 + 40
                solution = 55 <= coordinates[0] <= 166 + \
                    115 and 376 <= coordinates[1] <= 370 + 40

                ESC = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                if event.type == pygame.QUIT or ESC:
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    column = coordinates[0] // (self.width +
                                                self.square_with)
                    row = coordinates[1] // (self.height + self.square_with)

                    # reset hệ thống thông báo sau khi thực hiện một hành động
                    board.set_message('', '', '')

                    # check xem người dùng có nhấn vào nút Submit không
                    # 'solution_mode' ngăn người chơi nộp Solution
                    if submit and solution_mode is False:
                        results = board.verify(user_answers)
                        if results is True:
                            board.set_message(
                                'Congratulations! You win!', '', '')
                            win = True

                    # Nếu người chơi nhấn Solution
                    elif solution:
                        if save_user_answers is True:
                            board.remove_bulbs()
                            board.verify(board.get_supervise())
                            save_user_answers = False
                            solution_mode = True

                        # Nếu nhấp vào nút lần thứ hai, xóa giải pháp trong trò chơi trên bảng
                        # và để người chơi tiếp tục trạng thái trước đó
                        elif save_user_answers is False:
                            board.remove_bulbs()
                            solution_mode = False
                            for i in user_answers:
                                square = user_answers[i]
                                board.generate_bulbs(square, 0, None)
                            save_user_answers = True

                    elif 44 <= coordinates[0] <= 336 and 44 <= coordinates[1] <= 336:
                        square = board.get_square((row, column))

                        if type(square) == White and solution_mode is False:
                            # nếu hình vuông màu trắng không phải là bóng đèn và không được chiếu sáng thì thêm
                            # một bóng đèn vào hình vuông này và thêm nó vào danh sách câu trả lời của Người chơi
                            if (row, column) not in user_answers:
                                square = board.get_square((row, column))
                                board.generate_bulbs(square, 0, None)
                                if square.get_bulb() is True:
                                    user_answers[(row, column)] = square

                            # Nếu người chơi nhấp chuột vào ô đã có đèn thì người chơi muốn gỡ đèn này
                            # Xóa ô đó khỏi bảng và user_answers
                            elif (row, column) in user_answers:
                                if square.get_bulb() is True:
                                    board.generate_light(square, False, False)
                                    square.set_illuminated(False)
                                    del user_answers[(row, column)]

                                    # Khi một đèn bị xóa đi thì những ô được nó chiếu sáng cũng bị ngắt sáng
                                    for i in board.get_board():
                                        for j in i:
                                            if type(j) == White and j.get_bulb() is True:
                                                board.generate_light(
                                                    j, True, False)

                    # Set hình ảnh các loại đèn tùy theo người chơi có mắc lỗi không
                    # Hoặc nếu người chơi sửa lại một lỗi sai thì xóa đèn màu đỏ đi
                    for i in board.get_board():
                        for j in i:
                            if type(j) == White and j.get_bulb() is True:
                                overlap = board.generate_light(j, False, True)
                                if overlap is False:
                                    j.set_overlap(True)
                                else:
                                    j.set_overlap(False)

            # Dựa trên yêu cầu cập nhật bóng đèn của người chơi ở trên, dùng bảng mới nhất
            # và cập nhật màu các ô vuông
            for row in range(1, 8):
                for column in range(1, 8):
                    color = self.black
                    square = board.get_square((row, column))
                    if square.get_symbol() == 'W':
                        color = self.white
                    elif square.get_symbol() == 'L' or square.get_symbol() == '*':
                        color = self.yellow

                    # vẽ bảng
                    pygame.draw.rect(self.screen, color, [(self.square_with + self.width) * column + self.square_with, (
                        self.square_with + self.height) * row + self.square_with, self.width, self.height])

                    # cập nhật biểu tượng của hình vuông
                    self.update_square_symbol(square, row, column)
                    # vẽ các đường biên
                    self.draw_borders()

            # hiển thị nút Solution và Submit
            self.add_buttons()
            # hiển thị thông báo cho người chơi
            self.update_message(board)
            # nếu người chơi thắng game thì gửi thông báo chúc mừng và thoát game
            if win is True:
                self.check_win(win, board)
            pygame.display.flip()

    def add_buttons(self):
        """ Tạo text cho các nút Submit, Solution và vị trí của chúng """
        font = pygame.font.SysFont('Calibri', 35)
        pygame.draw.rect(self.screen, self.gray, [200, 370, 100, 40])
        text = font.render('Submit', True, self.black)
        self.screen.blit(text, (200, 370))
        pygame.draw.rect(self.screen, self.gray, [50, 370, 115, 40])
        text = font.render('Solution', True, self.black)
        self.screen.blit(text, (50, 370))

    def draw_borders(self):
        '''Vẽ các đường viền cho bảng trò chơi'''
        # draw.line(surface, color, (starting column, starting row), (ending column, ending row), thickness)
        pygame.draw.line(self.screen, self.gray, (42, 42),
                         (336, 42), 2)        # biên trên
        pygame.draw.line(self.screen, self.gray, (42, 336),
                         (336, 336), 2)      # biên dưới
        pygame.draw.line(self.screen, self.gray, (42, 42),
                         (42, 336), 2)        # biên trái
        pygame.draw.line(self.screen, self.gray, (336, 42),
                         (336, 337), 2)      # biên phải

    def check_win(self, win, board):
        """
        Presents a countdown for the game to exit when the Player's
        solution is verified correct by the verification algorithm. -> check
        """
        if win is True:
            # Show the congratulatory message for 2 second
            pygame.time.wait(1000)
            pygame.display.flip()

            pygame.time.wait(1000)
            pygame.draw.rect(self.screen, self.black, [1, 1, 375, 35])

            # Change the message that the game ends in 5 seconds for the Player
            board.set_message('Game ends in 5 seconds...', '', '')
            warning_font = pygame.font.SysFont('Calibri', 15)
            warning = warning_font.render(
                board.get_message()[0], False, self.yellow)
            self.screen.blit(warning, (5, 5))
            pygame.display.flip()
            # Initiate a countdown from 5 to 0
            for i in range(5, -1, -1):
                pygame.time.wait(1000)
                board.set_message(str(i) + '...', '', '')

                warning_font = pygame.font.SysFont('Calibri', 15)
                warning = warning_font.render(
                    board.get_message()[0], False, self.yellow)
                self.screen.blit(warning, (185, 5))
                pygame.display.flip()

                # After displaying each second of the countdown, then erase it for the next number
                pygame.draw.rect(self.screen, self.black, [170, 1, 375, 35])
            pygame.quit()
            exit()

    def update_message(self, board):
        ''' Cập nhật loại thông báo được in ra '''
        if board.get_message()[0] != '' or board.get_message()[1] != '' or board.get_message()[2] != '':
            # Set phông chữ và vị trí của thông báo
            warning_font = pygame.font.SysFont('Calibri', 15)
            warning = warning_font.render(
                board.get_message()[0], False, self.white)
            self.screen.blit(warning, (5, 5))

            warning = warning_font.render(
                board.get_message()[1], False, self.white)
            self.screen.blit(warning, (5, 20))

            warning = warning_font.render(
                board.get_message()[2], False, self.white)
            self.screen.blit(warning, (60, 345))

        if board.get_message()[0] == '' and board.get_message()[1] == '' and board.get_message()[2] == '':
            pygame.draw.rect(self.screen, self.black, [5, 1, 375, 35])
            pygame.draw.rect(self.screen, self.black, [50, 345, 320, 20])

    def update_square_symbol(self, square, row, column):
        ''' Cập nhật màn hình với các thuộc tính biểu tượng mới nhất của mỗi ô vuông '''
        font = pygame.font.SysFont('Arial', 30)
        # với mỗi ô đen, hiển thị số mà nó được gán
        if type(square) == Black:
            font = pygame.font.SysFont('Arial', 30)
            text = font.render(square.get_symbol(), 1, (100, 255, 55))
            rect = column * (self.square_with + self.width) + \
                15, row * (self.square_with + self.height)
            self.screen.blit(text, rect)

        # với mỗi ô trắng, nếu có đèn ở trên thì hiển thị màu đèn tương ứng (vàng hay đỏ)
        if type(square) == White and square.get_bulb() is True:
            text = font.render(square.get_symbol(), 1, self.red)
            rect = column * (self.square_with + self.width) + \
                12, row * (self.square_with + self.height) + 3

            if square.get_overlap():
                self.screen.blit(self.image2, rect)
            else:
                self.screen.blit(self.image, rect)


# khởi tạo đối tượng Pygame và gọi hàm setup() để trò chơi chạy
game = Game()
game.setup()
