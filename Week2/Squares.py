class Squares:
    # Đại diện cho những ô vuông trong bảng
    def __init__(self, x, y):
        self.neighbors = []
        self.symbol = ''
        self.visited = False
        self.location = (x, y)

    def add_neighbors(self, square):
        # thêm các ô vuông là hàng xóm của ô vuông hiện tại
        self.neighbors.append(square)

    def set_symbol(self, symbol):
        '''Tạo loại biểu tượng cho ô vuông trong các loại 
            Ô vuông đen, trắng hay có đèn nằm trên nó (ký hiệu B, W, L)'''
        self.symbol = symbol

    def set_visited(self, status):
        # Tạo trạng thái ô vuông được duyệt qua hay chưa (giá trị Boolean)
        self.visited = status

    def get_symbol(self):
        # Trả về loại ký hiệu của ô vuông (B, W, hay L)
        return self.symbol

    def get_neighbors(self):
        # Trả về các ô vuông hàng xóm
        return self.neighbors

    def get_location(self):
        # Trả về tọa độ của ô vuông dạng tuple
        return self.location

    def get_visited(self):
        # Trả về giá trị Bool thể hiện ô vuông đã được duyệt qua hay chưa
        return self.visited