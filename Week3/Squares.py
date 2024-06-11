class Squares:
    # Đại diện cho những ô vuông trong bảng
    def __init__(self, x, y):
        self.__neighbors = []
        self.symbol = ''
        self.__visited = False
        self.__location = (x, y)

    def add_neighbors(self, square):
        # thêm các ô vuông là hàng xóm của ô vuông hiện tại
        self.__neighbors.append(square)

    def set_symbol(self, symbol):
        '''Tạo loại biểu tượng cho ô vuông trong các loại 
            Ô vuông đen, trắng hay có đèn nằm trên nó (ký hiệu B, W, L)'''
        self.symbol = symbol

    def set_visited(self, status):
        # Tạo trạng thái ô vuông được duyệt qua hay chưa (giá trị Boolean)
        self.__visited = status

    def get_symbol(self):
        # Trả về loại ký hiệu của ô vuông (B, W, hay L)
        return self.symbol

    def get_neighbors(self):
        # Trả về các ô vuông hàng xóm
        return self.__neighbors

    def get_location(self):
        # Trả về tọa độ của ô vuông dạng tuple
        return self.__location

    def get_visited(self):
        # Trả về giá trị Bool thể hiện ô vuông đã được duyệt qua hay chưa
        return self.__visited


class Black(Squares):
    # Đại diện cho ô vuông màu đen trong bảng
    def __init__(self, x, y):
        """
        Khởi tạo các đặc điểm của hình vuông màu đen
        """
        super().__init__(x, y)
        self.symbol = ''
        self.__number = ''

    def __str__(self):
        # Trả về số được in (kiểu string) trên hình vuông màu đen
        return '{self.__number}'.format(self=self)

    def set_number(self, num):
        # Tạo thuộc tính số của hình vuông (tức là "", 0, 1, 2, 3 hoặc 4).
        self.__number = num

    def get_number(self):
        # Trả về thuộc tính số của hình vuông (tức là "", 0, 1 , 2, 3 hoặc 4)
        return self.__number


class White(Squares):
    # Đại diện cho những ô vuông màu trắng
    def __init__(self, x, y):
        """
        Khởi tạo các đặc điểm mặc định của hình vuông màu trắng
        """
        super().__init__(x, y)
        self.__illuminated = False
        self.__bulb = False
        self.__overlap = False
        self.symbol = 'W'

    def __str__(self):
        """Trả về biểu tuơng của hình vuông thay vì đối tượng khi nó được in"""
        return '{self.symbol}'.format(self=self)

    def set_illuminated(self, trans):
        """
        Lấy giá trị boolean làm tham số, nếu True thì đặt thuộc tính được chiếu sáng là True 
        và thẻ thành '*', màn hình hiển thị nó được chiếu sáng hay không, (nó có màu vàng hay trắng)
        nếu không được chiếu sáng được đặt thành False và thẻ được chuyển đổi thành 'W'
        """
        # Nếu ô vuông được chỉ định là được chiếu sáng
        if trans is True:
            self.__illuminated = True
            self.symbol = '*'   # Đại diện cho ô được chiếu sáng

        # Ngược lại
        elif trans is False:
            self.__illuminated = False
            self.__bulb = False
            self.symbol = 'W'

    def set_overlap(self, overlap):
        # Tạo trạng thái overlap = True nếu có 2 bóng đèn chiếu sáng nhau, nếu không thì False
        self.__overlap = overlap

    def get_illuminated(self):
        # Trả về thuộc tính được chiếu sáng của hình vuông (True hoặc False)
        return self.__illuminated

    def get_bulb(self):
        # Trả về True hay False biểu thị hình vuông có bóng đèn hay không
        return self.__bulb

    def get_overlap(self):
        # Trả về True hay False biểu thị hình vuông có được chiếu sáng hay không"""
        return self.__overlap

    def trans_bulb(self):
        """
        Trả về xem hình vuông có bóng đèn trên nó hay không. 
        Nếu không có thì thêm một bóng đèn vào hình vuông và chiếu sáng ô đó nếu hiện tại không có. 
        Ngược lại, tháo bóng đèn của hình vuông
        """
        if self.__bulb is False:
            self.__bulb = True
            self.__illuminated = True
            self.symbol = 'L'
        else:
            self.__bulb = False
        return self.__bulb
