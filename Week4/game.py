import pygame
from board import *
from squares import *
from collections import deque
from config import *


class Game:
    def __init__(self):
        """
        Khởi tạo đối tượng Game.
        Thiết lập màn hình, đồng hồ đếm thời gian và các biến cần thiết khác cho trò chơi.
        """
        self.screen = pygame.display.set_mode(WINDOWS)
        self.clock = pygame.time.Clock()
        self.color_mode = None
        self.solution = False

    def draw_timer(self):
        """
        Vẽ bộ đếm thời gian ở tọa độ (700, 40).
        Nếu controller.mode = 'Play', đếm ngược 5 phút rồi thoát,
        nếu không thì giữ nguyên chức năng hiện tại của hàm.
        """
        start_time = pygame.time.get_ticks() // 1000
        current_time = pygame.time.get_ticks()  # Lấy thời gian hiện tại
        elapsed_time = current_time - start_time  # Tính thời gian đã trôi qua

        # Chọn phông chữ và kích thước cho bộ đếm thời gian
        timer_font = pygame.font.SysFont('Arial', 36)

        if controller.mode == 'PLAY':
            countdown_time = 5 * 61 * 1000 + 500  # 5 phút = 5 * 60 * 1000 milliseconds
            time_left = max(0, countdown_time - elapsed_time)
            minutes = str(time_left // 60000).zfill(2)
            seconds = str((time_left // 1000) % 60).zfill(2)
            milliseconds = str((time_left % 1000) // 10).zfill(2)
            # Tạo văn bản bộ đếm thời gian
            timer_text = timer_font.render(
                f"{minutes}:{seconds}:{milliseconds}", True, WHITE)

            # Nếu thời gian đếm ngược đã hết, thoát khỏi Pygame
            if time_left <= 0:
                controller.running = False
                controller.gameover = True
                return
            # Vẽ bộ đếm thời gian lên màn hình
            self.screen.blit(timer_text, (700, 40))

    def setup(self, color_mode=YELLOW):
        """
        Thiết lập và khởi tạo các thành phần của trò chơi.

        Tạo bảng chơi, tạo các ô trắng, ô đen, cạnh của bảng và các thành phần khác.
        Khởi tạo Pygame và cài đặt tiêu đề, lưu trữ trạng thái của trò chơi và chạy vòng lặp trò chơi chính.
        """
        global board
        board = Board(controller.lv)
        board.generate_white()
        board.generate_black()
        board.generate_edges()
        board.create_grid()
        board.assign_number()
        board.remove_bulbs()
        board.verify(board.get_supervise())
        board.remove_bulbs()

        pygame.init()
        pygame.display.set_caption("Turn On The Lights")

        # 'save_user_answers' chuyển đổi giữa hiển thị/ẩn giải pháp trong trò chơi và câu trả lời của người chơi
        # 'solution_mode' cho biết Người chơi hiện có đang xem giải pháp trong trò chơi hay không
        save_user_answers = True
        solution_mode = False
        win = False
        # lưu những đáp án của người chơi trong stack
        user_answers = deque()
        undo_stack = deque()
        redo_stack = deque()
        # Giữ vòng lặp của trò chơi tiếp tục chạy cho đến khi màn chơi vẫn tồn tại
        # hoặc nếu người chơi gửi giải pháp đã được xác minh
        # tọa độ của điểm cuối các cạnh trong bảng
        end_pos = (levels[board.lv][0]*40 + (levels[board.lv][0] - 1)*2+44)
        controller.running = True
        controller.congrat = True
        while True:
            self.screen.fill(BLACK, (700, 40, 300, 40))
            self.draw_timer()  # Vẽ bộ đếm thời gian
            pygame.display.flip()  # Cập nhật màn hình

            self.clock.tick(60)  # Giới hạn tốc độ khung hình
            for event in pygame.event.get():

                # lấy tọa độ chuột của Người chơi khi nhấp vào màn hình
                coordinates = pygame.mouse.get_pos()
                # Phạm vi các nút submit và solution
                submit = 700 <= coordinates[0] <= 820 and 100 <= coordinates[1] <= 140
                solution = 700 <= coordinates[0] <= 815 and 150 <= coordinates[1] <= 190
                undo = 700 <= coordinates[0] <= 815 and 200 <= coordinates[1] <= 240
                redo = 700 <= coordinates[0] <= 820 and 250 <= coordinates[1] <= 290
                restart = 700 <= coordinates[0] <= 950 and 300 <= coordinates[1] <= 340
                back = 700 <= coordinates[0] <= 820 and 350 <= coordinates[1] <= 390
                ESC = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                if event.type == pygame.QUIT or ESC:
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    column = coordinates[0] // (WIDTH +
                                                SQUARE_WIDTH)
                    row = coordinates[1] // (HEIGHT + SQUARE_WIDTH)

                    # reset hệ thống thông báo sau khi thực hiện một hành động
                    board.set_message('', '', '', '')

                    # check xem người dùng có nhấn vào nút Submit không
                    # 'solution_mode' ngăn người chơi nộp Solution
                    if submit and solution_mode is False:
                        results = board.verify(
                            {(sq.get_location()): sq for sq in user_answers})
                        if results is True:
                            win = True

                    # Nếu người chơi nhấn Solution
                    elif solution:
                        if controller.mode == 'PLAY':
                            controller.solution_clicked = True
                            board.set_message(
                                '', '', '', 'Not allowed to use Solution in Play Mode')
                        else:
                            board.remove_bulbs()
                            if save_user_answers is True:
                                board.verify(board.get_supervise())
                                save_user_answers = False
                                solution_mode = True

                            # Nếu nhấp vào nút lần thứ hai, xóa giải pháp trong trò chơi trên bảng
                            # và để người chơi tiếp tục trạng thái trước đó
                            elif save_user_answers is False:
                                solution_mode = False
                                save_user_answers = True
                                for i in user_answers:
                                    square = user_answers[i]
                                    board.generate_bulbs(square, 0, None)
                    elif undo:
                        if user_answers:
                            last_action = user_answers.pop()
                            redo_stack.append(last_action)
                            board.generate_light(last_action, False, False)
                            last_action.set_illuminated(False)
                            for i in board.get_board():
                                for j in i:
                                    if type(j) == White and j.get_bulb() is True:
                                        board.generate_light(j, True, False)

                    elif redo:
                        if redo_stack:
                            last_action = redo_stack.pop()
                            user_answers.append(last_action)
                            board.generate_bulbs(last_action, 0, None)

                    elif restart:
                        while user_answers:
                            last_action = user_answers.pop()
                            undo_stack.append(last_action)
                            board.generate_light(last_action, False, False)
                            last_action.set_illuminated(False)
                            for i in board.get_board():
                                for j in i:
                                    if type(j) == White and j.get_bulb() is True:
                                        board.generate_light(j, True, False)
                        save_user_answers = True
                        solution_mode = False
                        win = False
                    elif back:
                        controller.running = False
                        controller.congrat = False
                        break
                    elif 44 <= coordinates[0] <= end_pos and 44 <= coordinates[1] <= end_pos:
                        square = board.get_square((row, column))

                        if type(square) == White and solution_mode is False:
                            # nếu hình vuông màu trắng không phải là bóng đèn và không được chiếu sáng thì thêm
                            # một bóng đèn vào hình vuông này và thêm nó vào danh sách câu trả lời của Người chơi
                            if square not in user_answers:
                                board.generate_bulbs(square, 0, None)
                                if square.get_bulb() is True:
                                    user_answers.append(square)

                            # Nếu người chơi nhấp chuột vào ô đã có đèn thì người chơi muốn gỡ đèn này
                            # Xóa ô đó khỏi bảng và user_answers
                            elif square in user_answers:
                                if square.get_bulb() is True:
                                    board.generate_light(square, False, False)
                                    square.set_illuminated(False)
                                    user_answers.remove(square)

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
            for row in range(1, levels[board.lv][0] + 1):
                for column in range(1, levels[board.lv][0] + 1):
                    color = BLACK
                    square = board.get_square((row, column))
                    if square.get_symbol() == 'W':
                        color = WHITE
                    elif square.get_symbol() == 'L' or square.get_symbol() == '*':
                        color = color_mode

                    # vẽ bảng
                    pygame.draw.rect(self.screen, color, [(SQUARE_WIDTH + WIDTH) * column + SQUARE_WIDTH, (
                        SQUARE_WIDTH + HEIGHT) * row + SQUARE_WIDTH, WIDTH, HEIGHT])

                    # cập nhật biểu tượng của hình vuông
                    self.update_square_symbol(square, row, column)
                    # vẽ các đường biên
                    self.draw_borders()
            if controller.running == False:
                if controller.gameover is False and not back:
                    controller.congrat = True
                return
            # hiển thị nút Solution và Submit
            self.add_buttons()
            # hiển thị thông báo cho người chơi
            self.update_message(board)
            # nếu người chơi thắng game thì gửi thông báo chúc mừng và thoát game
            if win is True:
                return
            pygame.display.flip()

    def add_buttons(self):
        """ Thêm các nút chức năng lên màn hình trò chơi."""
        font = pygame.font.SysFont('Arial', 35)
        pygame.draw.rect(self.screen, WHITE, [700, 100, 115, 40])
        text = font.render('Submit', True, BLACK)
        self.screen.blit(text, (700, 100))
        pygame.draw.rect(self.screen, WHITE, [700, 150, 115, 40])
        text = font.render('Solution', True, BLACK)
        self.screen.blit(text, (700, 150))
        pygame.draw.rect(self.screen, WHITE, [700, 200, 115, 40])
        text = font.render('Undo', True, BLACK)
        self.screen.blit(text, (700, 200))
        pygame.draw.rect(self.screen, WHITE, [700, 250, 115, 40])
        text = font.render('Redo', True, BLACK)
        self.screen.blit(text, (700, 250))
        pygame.draw.rect(self.screen, WHITE, [700, 300, 115, 40])
        text = font.render('Restart', True, BLACK)
        self.screen.blit(text, (700, 300))
        pygame.draw.rect(self.screen, WHITE, [700, 350, 115, 40])
        text = font.render('Back', True, BLACK)
        self.screen.blit(text, (700, 350))

    def draw_borders(self):
        '''Vẽ các đường viền cho bảng trò chơi'''
        # draw.line(surface, color, (starting column, starting row), (ending column, ending row), thickness)
        # tọa độ của điểm cuối các cạnh trong bảng
        end_pos = (levels[board.lv][0]*40 + (levels[board.lv][0] - 1)*2+44)

        pygame.draw.line(self.screen, GRAY, (42, 42),
                         (levels[board.lv][0]*40 + (levels[board.lv][0] - 1)*2+44, 42), 2)        # biên trên
        pygame.draw.line(self.screen, GRAY, (42, end_pos),
                         (end_pos, end_pos), 2)      # biên dưới
        pygame.draw.line(self.screen, GRAY, (42, 42),
                         (42, end_pos), 2)        # biên trái
        pygame.draw.line(self.screen, GRAY, (end_pos, 42),
                         (end_pos, end_pos), 2)      # biên phải

    def update_message(self, board):
        ''' Cập nhật loại thông báo được in ra '''
        if board.get_message()[0] != '' or board.get_message()[1] != '' or board.get_message()[2] != '' or board.get_message()[3] != '':
            # Set phông chữ và vị trí của thông báo
            msg_font = pygame.font.SysFont('Arial', 25)
            msg = msg_font.render(
                board.get_message()[0], False, WHITE)
            self.screen.blit(msg, (60, 680))

            msg = msg_font.render(
                board.get_message()[1], False, WHITE)
            self.screen.blit(msg, (60, 710))

            msg = msg_font.render(
                board.get_message()[2], False, WHITE)
            self.screen.blit(msg, (60, 740))

            msg = msg_font.render(
                board.get_message()[3], False, WHITE)
            self.screen.blit(msg, (60, 770))
        if board.get_message()[0] == '' and board.get_message()[1] == '' and board.get_message()[2] == '' and board.get_message()[3] == '':
            pygame.draw.rect(self.screen, BLACK, [58, 680, 820, 120])

    def update_square_symbol(self, square, row, column):
        ''' Cập nhật màn hình với các thuộc tính biểu tượng mới nhất của mỗi ô vuông '''
        font = pygame.font.SysFont('Arial', 30)
        # với mỗi ô đen, hiển thị số mà nó được gán
        if type(square) == Black:
            font = pygame.font.SysFont('Arial', 30)
            text = font.render(square.get_symbol(), 1, WHITE)
            rect = column * (SQUARE_WIDTH + WIDTH) + \
                15, row * (SQUARE_WIDTH + HEIGHT)
            self.screen.blit(text, rect)
        # với mỗi ô trắng, nếu có đèn ở trên thì hiển thị màu đèn tương ứng (vàng hay đỏ)
        if type(square) == White and square.get_bulb() is True:
            text = font.render(square.get_symbol(), 1, RED)
            rect = column * (SQUARE_WIDTH + WIDTH) + \
                12, row * (SQUARE_WIDTH + HEIGHT) + 3
            if square.get_overlap():
                if controller.image_mode == YELLOW:
                    self.screen.blit(image2, rect)
                else:
                    self.screen.blit(image, rect)
            else:
                self.screen.blit(image, rect)
# khởi tạo đối tượng Pygame và gọi hàm setup() để trò chơi chạy