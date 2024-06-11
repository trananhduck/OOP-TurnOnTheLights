from Squares import *


class Black(Squares):
    # Đại diện cho ô vuông màu đen trong bảng
    def __init__(self, x, y):
        """
        Khởi tạo các đặc điểm của hình vuông màu đen
        """
        super().__init__(x, y)
        self.edges = []
        self.number = ''
        self.symbol = ''

    def __str__(self):
        # Trả về số được in (kiểu string) trên hình vuông màu đen
        return '{self.number}'.format(self=self)

    def set_number(self, num):
        # Tạo thuộc tính số của hình vuông (tức là "", 0, 1, 2, 3 hoặc 4).
        self.number = num

    def get_number(self):
        # Trả về thuộc tính số của hình vuông (tức là "", 0, 1 , 2, 3 hoặc 4)
        return self.number


class White(Squares):
    # Represents a White square on the Board.
    def __init__(self, x, y):
        """
        Khởi tạo các đặc điểm mặc định của hình vuông màu trắng
        """
        super().__init__(x, y)
        self.illuminated = False
        self.bulb = False
        self.symbol = 'W'
        self.overlap = False

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
            self.illuminated = True
            self.symbol = '*'   # Đại diện cho ô được chiếu sáng

        # Ngược lại
        elif trans is False:
            self.illuminated = False
            self.symbol = 'W'
            self.bulb = False

    def set_overlap(self, overlap):
        # Tạo trạng thái overlap = True nếu có 2 bóng đèn chiếu sáng nhau, nếu không thì False
        self.overlap = overlap

    def get_illuminated(self):
        # Trả về thuộc tính được chiếu sáng của hình vuông (True hoặc False)
        return self.illuminated

    def get_bulb(self):
        # Trả về True hay False biểu thị hình vuông có bóng đèn hay không
        return self.bulb

    def get_overlap(self):
        # Trả về True hay False biểu thị hình vuông có được chiếu sáng hay không"""
        return self.overlap

    def trans_bulb(self):
        """
        Trả về xem hình vuông có bóng đèn trên nó hay không. 
        Nếu không có thì thêm một bóng đèn vào hình vuông và chiếu sáng ô đó nếu hiện tại không có. 
        Ngược lại, tháo bóng đèn của hình vuông
        """
        if self.bulb is False:
            self.bulb = True
            self.illuminated = True
            self.symbol = 'L'
        else:
            self.bulb = False
        return self.bulb
