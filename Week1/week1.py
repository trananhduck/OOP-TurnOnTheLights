import pygame
import random


class Board:
    def __init__(self):
        # Khởi tạo ma trận của câu đố
        # tạo ma trận không lưu dữ liệu gì
        self.board = [[''] * 9 for i in range(9)]
        self.squares = {}
        self.black = []
        self.supervise = {}
        # supervise dùng để theo dõi vị trí của các bóng đèn trên bảng trò chơi
        # và kiểm tra xem có bóng đèn nào chiếu sáng bóng đèn khác không
        self.message, self.message2, self.message3 = '', '', ''  # các thông báo

    def get_board(self):
        # Trả về bảng câu đố
        return self.board

    def get_square(self, coordinates):
        # Trả về hình vuông tại tọa độ đã chỉ định
        return self.squares[coordinates]

    def get_message(self):
        # Trả về các thông báo
        return self.message, self.message2, self.message3

    def set_board(self, x, y, square):
        # Đặt hình vuông vào vị trí xác định trên bảng
        self.board[x][y] = square
        self.squares[(x, y)] = square

    def set_message(self, message, message2, message3):
        # Đặt thông báo cho người chơi
        self.message = message
        self.message2 = message2
        self.message3 = message3

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
                        self.squares[(i, j)] = square

    def generate_black(self):
        # Tạo ngẫu nhiên từ 15-17 ô vuông màu đen trên toàn bảng và lưu vào coodinates
        coordinates = []

        # lấy ngẫu nhiên số lượng các ô đen
        position = random.randrange(15, 17)
        while len(coordinates) != position:
            x, y = random.randrange(1, 8), random.randrange(1, 8)
            if (x, y) not in coordinates:
                coordinates.append((x, y))
                square = Black(x, y)
                self.set_board(x, y, square)
                self.black.append(square)


class Squares:
    # Đại diện cho những ô vuông trong ma trận
    def __init__(self, x, y):
        self.neighbors = []
        self.tag = ''
        self.visited = False
        self.location = (x, y)

    def add_neighbors(self, square):
        # thêm các ô vuông là hàng xóm của ô vuông hiện tại
        self.neighbors.append(square)

    def set_symbol(self, symbol):
        '''Tạo loại biểu tượng cho ô vuông trong các loại 
            Ô vuông đen, trắng hay có đèn nằm trên nó (ký hiệu B, W, L)'''
        self.symbol = symbol

    def get_symbol(self):
        # Trả về loại ký hiệu của ô vuông (B, W, hay L)
        return self.symbol

    def get_neighbors(self):
        # Trả về các ô vuông hàng xóm
        return self.neighbors

    def get_location(self):
        # Trả về tọa độ của ô vuông dạng tuple
        return self.location


class White:
    pass


class Black:
    pass


class Pygame:
    pass
