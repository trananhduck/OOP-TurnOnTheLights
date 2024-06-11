import random
from squares import *
from config import *


class Board:
    """
    Lớp Board đại diện cho bảng trò chơi. Lớp này chứa các phương thức để khởi tạo bảng,
    đặt các ô vuông, đặt các thông báo, và tạo các bóng đèn trên bảng.
    """

    def __init__(self, lv):
        """
        Khởi tạo bảng của câu đố không lưu dữ liệu gì.

        Tham số:
        lv (int): Cấp độ của trò chơi.
        """
        self.lv = lv
        self.__board = [[''] * (levels[self.lv][0] + 2)
                        for i in range(levels[self.lv][0] + 2)]
        self.__squares = {}
        self.__black = []
        self.supervise = {}

        # supervise dùng để theo dõi vị trí của các bóng đèn trên bảng trò chơi
        # và kiểm tra xem có bóng đèn nào chiếu sáng bóng đèn khác không
        self.__message, self.__message2, self.__message3, self.__message4 = '', '', '', ''

    def set_board(self, x, y, square):
        """
        Đặt hình vuông vào vị trí xác định trên bảng.

        Tham số:
        x (int): Tọa độ x trên bảng.
        y (int): Tọa độ y trên bảng.
        square (Square): Hình vuông được đặt vào bảng.
        """
        self.__board[x][y] = square
        self.__squares[(x, y)] = square

    def set_message(self, message, message2, message3, message4):
        ''' Đặt thông báo cho người chơi '''
        self.__message = message
        self.__message2 = message2
        self.__message3 = message3
        self.__message4 = message4

    def get_board(self):
        # Trả về bảng câu đố
        return self.__board

    def get_square(self, coordinates):
        # Trả về hình vuông tại tọa độ đã chỉ định
        return self.__squares[coordinates]

    def get_supervise(self):
        # Trả về supervise
        return self.supervise

    def get_message(self):
        # Trả về các thông báo
        return self.__message, self.__message2, self.__message3, self.__message4

    def generate_white(self):
        """
        Tạo các ô vuông màu trắng trên toàn bảng.
        """
        for i in range(levels[self.lv][0] + 2):
            for j in range(levels[self.lv][0] + 2):
                if i == 0 or i == levels[self.lv][0] + 1 or j == 0 or j == levels[self.lv][0] + 1:
                    # Điều kiện này kiểm tra nếu vị trí (i, j) nằm ở biên của bảng
                    # (hàng đầu tiên, hàng cuối cùng, cột đầu tiên, hoặc cột cuối cùng).
                    self.set_board(i, j, '-')
                else:
                    if self.__board[i][j] == '':
                        square = White(i, j)
                        self.__board[i][j] = square
                        self.__squares[(i, j)] = square  # list các ô vuông

    def generate_black(self):
        '''Tạo ngẫu nhiên một số ô vuông màu đen trên toàn bảng và lưu vào coodinates'''
        coordinates = []
        position = random.randrange(levels[self.lv][1], levels[self.lv][2])
        while len(coordinates) != position:
            x, y = random.randrange(
                1, levels[self.lv][0] + 1), random.randrange(1, levels[self.lv][0] + 1)
            if (x, y) not in coordinates:
                coordinates.append((x, y))
                square = Black(x, y)
                # Đặt các ô vuông màu đen vào bảng
                self.set_board(x, y, square)
                self.__black.append(square)

    def generate_edges(self):
        '''Tạo danh sách các ô vuông hàng xóm của ô vuông hiện tại
        Duyệt bảng, thực hiện với mỗi ô vuông'''
        for i in range(1, levels[self.lv][0] + 1):
            for j in range(1, levels[self.lv][0] + 1):
                # Các hướng trên, dưới, trái, phải
                up = self.__board[i - 1][j]
                left = self.__board[i][j - 1]
                right = self.__board[i][j + 1]
                down = self.__board[i + 1][j]

                # Thêm các hàng xóm của ô vuông tìm thấy ở 4 hướng vào một danh sách
                neighbors = [up, left, right, down]

                # Duyệt qua các hàng xóm và thêm vào các cạnh giữa nó và ô vuông hiện tại
                for p in neighbors:
                    if p != '-':   # Nếu đối tượng đang xét là biên thì bỏ qua
                        curr = self.__board[i][j]
                        # Gọi phương thức add_neighbor trong lớp Squares
                        curr.add_neighbors(p)

    def assign_number(self):
        ''' Gán giá trị từ 0 đến 4 (hoặc có thể là không gán giá trị) cho các ô màu đen'''
        for j in range(len(self.__black)):
            sq = self.__black[j]
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

    def generate_bulbs(self, square, probability, user):
        """
        Đặt bóng đèn vào các ô vuông với tỉ lệ cho trước.

        Tham số:
        square (Square): Ô vuông được đặt bóng đèn.
        probability (float): Xác suất đặt bóng đèn.
        user (str): Người thực hiện hành động.
        """
        if random.random() >= probability and type(square) == White and square.get_bulb() is False:
            if user == 'admin':
                self.supervise[square.get_location()] = square
            status = square.trans_bulb()
            # Hàm trans_bulb chuyển đổi trạng thái đèn,
            # Nghĩa là nếu tại một ô có đèn thì xóa nó, nếu không thì đặt đèn vào ô đó
            # Trả về trạng thái của bóng đèn

            if status is True:
                self.generate_light(square, True, False)

    def generate_light(self, square, trans, check):
        """
        Chiếu sáng các ô vuông
        Tham số:
        square (Square): Ô vuông bắt đầu phát ra ánh sáng.
        trans (bool): Trạng thái bật hay tắt đèn.
        check (bool): Thực hiện kiểm tra hay chiếu sáng.
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
        """Xóa tất cả bóng đèn trên bảng
        Thăm các ô vuông trắng, nếu nó được chiếu sáng thì xóa ánh sáng ở ô đó
        Ô đặt bóng đèn là ô tự chiếu sáng chính nó
        """
        for row in self.__board:
            for j in row:
                if j != '-':
                    if type(j) == White and j.get_illuminated() is True:
                        j.set_illuminated(False)  # Phương thức thuộc lớp White
                        j.set_visited(False)  # Phương thức thuộc lớp Squares

    def create_grid(self):
        """
        tạo màn chơi ví dụ
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
                start = self.__board[1][1]
                self.BFS('fill_board', start)
                not_lighted = []

    def verify(self, supervise):
        """
        Xác minh giải pháp của người chơi xem có đáp ứng tất cả các tiêu chí chiến thắng hay không.

        Tham số:
        supervise (dict): Dictionary theo dõi vị trí của các bóng đèn.
        """
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
        all_illuminated = self.BFS('check_lights', self.__board[1][1])

        # kiểm tra xem tất cả các ô màu đen có số bóng đèn xung quanh đúng theo yêu cầu hay không.
        surrounding_black = self.BFS('check_numbers', self.__black[0])
        # hiển thị thông báo khi điều kiện thắng chưa được thỏa mãn
        if all_illuminated is True and single_bulbs is True and surrounding_black is True:
            return True
        else:
            if all_illuminated is False:
                self.__message = 'Not all squares are illuminated!'
            if surrounding_black is False:
                self.__message2 = 'Some Black square(s) have wrong of surrounding light bulbs!'
            if single_bulbs is False:
                self.__message3 = 'A light bulb is illuminated by another light bulb!'
            if controller.solution_clicked is True:
                self.__message4 = 'Not allowed to use Solution in Play Mode'
            return False

    def BFS(self, option, start):
        """
        Thực hiện duyệt theo chiều rộng (BFS) để kiểm tra và cập nhật trạng thái của các ô vuông trên bảng.

        Tham số:
        option (str): Lựa chọn hành động ('check_lights', 'fill_board', hoặc 'check_numbers').
        start (Square): Ô vuông bắt đầu để duyệt bảng.

        Trả về:
        bool: Kết quả kiểm tra tùy theo lựa chọn hành động.
        """
        # với mỗi ô vuông, đặt trạng thái ban đầu là chưa được duyệt qua
        for row in self.__board:
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
                group = self.__black

            # nếu ô vuông chưa được thăm thì đến thăm nó
            for i in group:
                if i.get_visited() is False:
                    i.set_visited(True)

                    # nếu lựa chọn là 'fill_board', nếu một ô vuông trắng chưa được chiếu sáng
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
