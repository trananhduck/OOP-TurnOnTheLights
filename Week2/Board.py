import pygame
import random
from Squares import *
from Black_n_White import *


class Board:
    def __init__(self):
        # Khởi tạo bảng của câu đố
        # tạo bảng không lưu dữ liệu gì
        self.board = [[''] * 9 for i in range(9)]
        self.squares = {}
        self.black = []
        self.supervise = {}
        # supervise dùng để theo dõi vị trí của các bóng đèn trên bảng trò chơi
        # và kiểm tra xem có bóng đèn nào chiếu sáng bóng đèn khác không
        self.message, self.message2, self.message3 = '', '', ''  # các thông báo

    def set_board(self, x, y, square):
        # Đặt hình vuông vào vị trí xác định trên bảng
        self.board[x][y] = square
        self.squares[(x, y)] = square

    def set_message(self, message, message2, message3):
        # Đặt thông báo cho người chơi
        self.message = message
        self.message2 = message2
        self.message3 = message3

    def get_board(self):
        # Trả về bảng câu đố
        return self.board

    def get_square(self, coordinates):
        # Trả về hình vuông tại tọa độ đã chỉ định
        return self.squares[coordinates]

    def get_supervise(self):
        # Trả về supervise
        return self.supervise

    def get_message(self):
        # Trả về các thông báo
        return self.message, self.message2, self.message3

    def generate_white(self):
        """
        Tạo các ô vuông màu trắng trên toàn bảng.
        """
        for i in range(9):
            for j in range(9):
                if i == 0 or i == 8 or j == 0 or j == 8:
                    # Điều kiện này kiểm tra nếu vị trí (i, j) nằm ở biên của bảng
                    # (hàng đầu tiên, hàng cuối cùng, cột đầu tiên, hoặc cột cuối cùng).
                    self.set_board(i, j, '-')
                else:
                    if self.board[i][j] == '':
                        square = White(i, j)
                        self.board[i][j] = square
                        self.squares[(i, j)] = square  # list các ô vuông
    '''CẦN XEM XÉT LẠI CÁCH TẠO MÀN CHƠI'''

    def generate_black(self):
        # Tạo ngẫu nhiên từ 15-17 ô vuông màu đen trên toàn bảng và lưu vào coodinates
        coordinates = []
        position = random.randrange(15, 17)
        while len(coordinates) != position:
            x, y = random.randrange(1, 8), random.randrange(1, 8)
            if (x, y) not in coordinates:
                coordinates.append((x, y))
                square = Black(x, y)
                # Đặt các ô vuông màu đen vào bảng
                self.set_board(x, y, square)
                self.black.append(square)

    def generate_edges(self):
        # Tạo danh sách các ô vuông hàng xóm của ô vuông hiện tại
        # Duyệt bảng, thực hiện với mỗi ô vuông
        for i in range(1, 8):
            for j in range(1, 8):
                # Các hướng trên, dưới, trái, phải
                up = self.board[i - 1][j]
                left = self.board[i][j - 1]
                right = self.board[i][j + 1]
                down = self.board[i + 1][j]

                # Thêm các hàng xóm của ô vuông tìm thấy ở 4 hướng vào một danh sách
                neighbors = [up, left, right, down]

                # Duyệt qua các hàng xóm và thêm vào các cạnh giữa nó và ô vuông hiện tại
                for p in neighbors:
                    if p != '-':   # Nếu đối tượng đang xét là biên thì bỏ qua
                        curr = self.board[i][j]
                        # Gọi phương thức add_neighbor trong lớp Squares
                        curr.add_neighbors(p)

    def assign_number(self):
        # Gán giá trị từ 0 đến 4 (hoặc có thể là không gán giá trị) cho các ô màu đen
        for j in range(len(self.black)):
            sq = self.black[j]
            location = sq.get_location()    # Phương thức thuộc lớp Squares
            x, y = location[0], location[1]
            needed_bulbs = 0
            # Thăm các ô vuông liền kề và lưu vào danh sách neighbors
            up = self.get_board()[x - 1][y]
            left = self.get_board()[x][y - 1]
            right = self.get_board()[x][y + 1]
            down = self.get_board()[x + 1][y]
            neighbors = [up, left, right, down]

            for p in neighbors:
                if p != '-':
                    # Đếm số ô vuông hàng xóm có chứa bóng đèn
                    if p.get_symbol() == 'L':
                        needed_bulbs += 1
            # Cập nhật số bóng đèn liền kề của ô vuông đen hiện tại
            if needed_bulbs > 0:
                sq.set_number(str(needed_bulbs))  # Phương thức của lớp Black
                sq.set_symbol(str(needed_bulbs))  # Phương thức của lớp Squares
            # gán xác suất để ô vuông màu đen có số là 0, ở đây đặt là 10%
            else:
                if random.random() >= 0.9:
                    sq.set_number(str(0))
                    sq.set_symbol(str(0))

    def generate_bulbs(self, sq, probability, user):
        # Hàm đặt bóng đèn vào các ô vuông với tỉ lệ cho trước
        if random.random() >= probability and type(sq) == White and sq.get_bulb() is False:
            if user == 'admin':
                self.supervise[sq.get_location()] = sq
            status = sq.trans_bulb()
            # Hàm trans_bulb chuyển đổi trạng thái đèn,
            # Nghĩa là nếu tại một ô có đèn thì xóa nó, nếu không thì đặt đèn vào ô đó
            # Trả về trạng thái của bóng đèn

            if status is True:
                self.generate_light(sq, True, False)

    def generate_light(self, square, trans, check):
        """
        curr - đối tượng hình vuông sẽ bắt đầu phát ra ánh sáng
        trans - True/False, trạng thái bật hay tắt đèn
        check, trans - thực hiện kiểm tra hay chiếu sáng (True or False)
        """

        loca = square.get_location()
        index = 1
        directions = [
            [loca[0], loca[1] + index],  # right
            [loca[0], loca[1] - index],  # left
            [loca[0] + index, loca[1]],  # up
            [loca[0] - index, loca[1]]   # down
        ]

        # duyệt theo các hướng
        for x in range(4):
            next_square = self.get_square((directions[x][0], directions[x][1]))

            while type(next_square) == White:
                # Nếu thực hiện chiếu sáng hay tắt đèn các ô vuông thì dừng lại khi next_square là bóng đèn
                if check is False and next_square.get_symbol() == 'L':
                    break
                # kiểm tra xem bóng đèn hiện tại có đang chiếu sáng bóng đèn khác không
                if check is True:
                    if next_square.get_bulb() is True:
                        return False  # Nếu trong hàng dọc hoặc ngang chứa bóng đèn đó chứa các đèn khác thì return False

                # Thực hiện chiếu sáng/hủy chiếu sáng các ô vuông (Gọi set_illuminated)
                if check is False:
                    next_square.set_illuminated(trans)
                index += 1

                if x == 0:
                    next_square = self.get_square((loca[0], loca[1] + index))
                elif x == 1:
                    next_square = self.get_square((loca[0], loca[1] - index))
                elif x == 2:
                    next_square = self.get_square((loca[0] + index, loca[1]))
                elif x == 3:
                    next_square = self.get_square((loca[0] - index, loca[1]))

            index = 1

        if check:
            return True

    def remove_bulbs(self):
        # Xóa tất cả bóng đèn trên bảng
        """
        Thăm các ô vuông trắng, nếu nó được chiếu sáng thì xóa ánh sáng ở ô đó
        Ô đặt bóng đèn là ô tự chiếu sáng chính nó
        """
        for row in self.board:
            for j in row:
                if j != '-':
                    if type(j) == White and j.get_illuminated() is True:
                        j.set_illuminated(False)  # Phương thức thuộc lớp White
                        j.set_visited(False)  # Phương thức thuộc lớp Squares

    def create_grid(self):
        # tạo màn chơi ví dụ
        """
        Duyệt bảng và đặt một cách ngẫu nhiên các bóng đèn
        lên các ô trắng chưa được chiếu sáng, sau đó điền các số lên các ô đen đã được tạo
        sao cho luôn tồn tại cách giải và xóa các bóng đèn đi
        """
        no_white = False  # Kiểm tra xem còn ô nào chưa được chiếu sáng không
        while no_white is False:

            not_lighted = []  # chứa các ô chưa được chiếu sáng
            for row in self.get_board():
                for j in row:
                    if j != '-':
                        # Đặt trạng thái được duyệt qua của các ô không phải biên thành False
                        j.set_visited(False)
                        if j.get_symbol() == 'W':
                            not_lighted.append(j)

            # trả về kết quả tất cả ô trắng đã được chiếu sáng hay chưa
            if len(not_lighted) == 0:
                no_white = True

            elif len(not_lighted) == 1:
                self.generate_bulbs(not_lighted[0], 0, 'admin')
                no_white = True

            if no_white is False:
                start = self.board[1][1]
                self.BFS('fill_board', start)
                not_lighted = []

    def verify(self, supervise):
        # Xác minh giải pháp của người chơi xem có đáp ứng tất cả các tiêu chí chiến thắng hay không
        # ban đầu giả định rằng không có bóng đèn nào chiếu sáng bóng đèn khác.
        single_bulbs = True
        # Duyệt qua các bóng đèn và xác minh
        for i in supervise:
            self.generate_bulbs(supervise[i], 0, None)
            # Kiểm tra xem bóng đèn tại vị trí supervise[i] có chiếu sáng bóng đèn khác hay không.
            single_bulbs = self.generate_light(supervise[i], False, True)
            # Nếu biến single_bulbs là False thì bóng đèn này chiếu sáng các bóng đèn khác
            # Sau đó đánh dấu hình vuông này bằng cách đặt biến overlap thành True
            if single_bulbs is False:
                supervise[i].set_overlap(True)

        # kiểm tra xem tất cả các ô màu trắng đã được chiếu sáng hay chưa
        all_illuminated = self.BFS('check_lights', self.board[1][1])

        # kiểm tra xem tất cả các ô màu đen có số bóng đèn xung quanh đúng theo yêu cầu hay không.
        surrounding_black = self.BFS('check_numbers', self.black[0])

        # hiển thị thông báo khi điều kiện thắng chưa được thỏa mãn
        if all_illuminated is True and single_bulbs is True and surrounding_black is True:
            return True
        else:
            if all_illuminated is False:
                self.message = 'Not all squares are illuminated!'
            if surrounding_black is False:
                self.message2 = 'Some Black square(s) have wrong # of surrounding light bulbs!'
            if single_bulbs is False:
                self.message3 = 'A light bulb is illuminating another light bulb!'
            return False

    def BFS(self, option, start):
        # với mỗi ô vuông, đặt trạng thái ban đầu là chưa được duyệt qua
        for row in self.board:
            for j in row:
                if type(j) == White or type(j) == Black:
                    j.set_visited(False)

        # tạo queue với ô vuông bắt đầu để duyệt bảng
        # group là các ô hàng xóm của ô hiện tại
        queue = [start]
        group = None
        while queue:
            square = queue.pop(0)
            if option == 'check_lights':
                group = square.get_neighbors()
            elif option == 'fill_board':
                group = square.get_neighbors()
            elif option == 'check_numbers':
                group = self.black

            # nếu ô vuông chưa được thăm thì đến thăm nó
            for i in group:
                if i.get_visited() is False:
                    i.set_visited(True)

                    # nếu lựa chọn là 'fill_board' một ô vuông trắng chưa được chiếu sáng
                    # và chưa được đặt bóng đèn thì có xác suất 40% đèn được đặt trên nó
                    if option == 'fill_board':
                        if type(i) == White and i.get_illuminated() is False and i.get_bulb() is False:
                            probability = 0.40
                            self.generate_bulbs(i, probability, 'admin')

                    # Nếu lựa chọn là 'check_light' (kiểm tra xem các ô trắng đã được chiếu sáng hoàn toàn hay chưa)
                    # và nếu có 1 ô vuông là trắng chưa được chiếu sáng thì trả về False
                    elif option == 'check_lights' and type(i) == White:
                        if i.get_illuminated() is False:
                            return False

                    # Nếu lựa chọn là 'check_numbers' (kiểm tra xem số đèn xung quang các ô đen có thỏa mãn không)
                    # (chỉ kiểm tra các ô đen có số), nếu số lượng các bóng đèn không thỏa mãn trả về False
                    elif option == 'check_numbers' and type(i) == Black:
                        if i.get_number() != '':
                            total = 0
                            for x in i.get_neighbors():
                                if type(x) == White and x.get_bulb() is True:
                                    total += 1
                            if str(total) != i.get_number():
                                return False
                    # Thêm i (1 trong các ô hàng xóm) vào hàng đợi và tiếp tục duyệt bảng đến khi queue rỗng
                    queue.append(i)

            square.set_visited(True)  # Đánh dấu ô vuông hiện tại đã được duyệt

        if option == 'check_lights' or option == 'check_numbers':
            return True
