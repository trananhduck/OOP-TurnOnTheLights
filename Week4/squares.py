class Squares:
    """
    Đại diện cho những ô vuông trong bảng.
    Attributes:
        __neighbors (list): Danh sách các ô vuông là hàng xóm của ô vuông hiện tại.
        symbol (str): Ký hiệu của ô vuông (B, W, L).
        __visited (bool): Trạng thái ô vuông đã được duyệt qua hay chưa.
        __location (tuple): Tọa độ của ô vuông.
    """

    def __init__(self, x, y):
        """
        Khởi tạo đối tượng Squares.
        Args:
            x (int): Tọa độ x của ô vuông.
            y (int): Tọa độ y của ô vuông.
        """
        self.__neighbors = []
        self.symbol = ''
        self.__visited = False
        self.__location = (x, y)

    def add_neighbors(self, square):
        """
        Thêm các ô vuông là hàng xóm của ô vuông hiện tại.
        Args:
            square (Squares): Ô vuông hàng xóm.
        """
        self.__neighbors.append(square)

    def set_symbol(self, symbol):
        """
        Tạo loại ký hiệu cho ô vuông.
        Args:
            symbol (str): Ký hiệu của ô vuông (B, W, L).
        """
        self.symbol = symbol

    def set_visited(self, status):
        """
        Tạo trạng thái ô vuông được duyệt qua hay chưa.
        Args:
            status (bool): Trạng thái đã duyệt qua (True) hoặc chưa (False).
        """
        self.__visited = status

    def get_symbol(self):
        """
        Trả về loại ký hiệu của ô vuông.
        Returns:
            str: Ký hiệu của ô vuông (B, W, L).
        """
        return self.symbol

    def get_neighbors(self):
        """
        Trả về các ô vuông hàng xóm.
        Returns:
            list: Danh sách các ô vuông hàng xóm.
        """
        return self.__neighbors

    def get_location(self):
        """
        Trả về tọa độ của ô vuông dạng tuple.
        Returns:
            tuple: Tọa độ của ô vuông.
        """
        return self.__location

    def get_visited(self):
        """
        Trả về giá trị boolean thể hiện ô vuông đã được duyệt qua hay chưa.
        Returns:
            bool: Trạng thái đã duyệt qua (True) hoặc chưa (False).
        """
        return self.__visited


class Black(Squares):
    """
    Đại diện cho ô vuông màu đen trong bảng.
    Attributes:
        __number (str): Số được in trên ô vuông màu đen.
    """

    def __init__(self, x, y):
        """
        Khởi tạo các đặc điểm của hình vuông màu đen
        """
        super().__init__(x, y)
        self.symbol = ''
        self.__number = ''

    def __str__(self):
        """
        Trả về số được in (kiểu string) trên ô vuông màu đen.
        Returns:
            str: Số được in trên ô vuông màu đen.
        """
        return '{self.__number}'.format(self=self)

    def set_number(self, num):
        """
        Tạo thuộc tính số của ô vuông.
        Args:
            num (str): Số được in trên ô vuông (các giá trị "", 0, 1, 2, 3 hoặc 4).
        """
        self.__number = num

    def get_number(self):
        """
        Trả về thuộc tính số của ô vuông.
        Returns:
            str: Số được in trên ô vuông (các giá trị "", 0, 1, 2, 3 hoặc 4).
        """
        return self.__number


class White(Squares):
    """
    Đại diện cho những ô vuông màu trắng.
    Attributes:
        __illuminated (bool): Trạng thái được chiếu sáng của ô vuông.
        __bulb (bool): Trạng thái có bóng đèn của ô vuông.
        __overlap (bool): Trạng thái có bóng đèn chiếu sáng chồng lên nhau.
    """

    def __init__(self, x, y):
        """
        Khởi tạo các đặc điểm mặc định của ô vuông màu trắng.
        Args:
            x (int): Tọa độ x của ô vuông.
            y (int): Tọa độ y của ô vuông.
        """
        super().__init__(x, y)
        self.__illuminated = False
        self.__bulb = False
        self.__overlap = False
        self.symbol = 'W'

    def __str__(self):
        """
        Trả về ký hiệu của ô vuông thay vì đối tượng khi nó được in.
        Returns:
            str: Ký hiệu của ô vuông.
        """
        return '{self.symbol}'.format(self=self)

    def set_illuminated(self, trans):
        """
        Đặt trạng thái được chiếu sáng của ô vuông.
        Args:
            trans (bool): Trạng thái chiếu sáng của ô vuông (True hoặc False).
        """
        # Lấy giá trị boolean làm tham số, nếu True thì đặt thuộc tính được chiếu sáng là True
        # và thẻ thành '*', màn hình hiển thị nó được chiếu sáng hay không, (nó có màu vàng hay trắng)
        # nếu không được chiếu sáng được đặt thành False và thẻ được chuyển đổi thành 'W'
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
        """
        Đặt trạng thái overlap của ô vuông.
        Args:
            overlap (bool): Trạng thái có hai bóng đèn chiếu sáng chồng lên nhau (True hoặc False).
        """
        self.__overlap = overlap

    def get_illuminated(self):
        """
        Trả về trạng thái được chiếu sáng của ô vuông.
        Returns:
            bool: Trạng thái chiếu sáng (True hoặc False).
        """
        return self.__illuminated

    def get_bulb(self):
        """
        Trả về trạng thái có bóng đèn của ô vuông.
        Returns:
            bool: Trạng thái có bóng đèn (True hoặc False).
        """
        return self.__bulb

    def get_overlap(self):
        """
        Trả về trạng thái có bóng đèn chiếu sáng chồng lên nhau.
        Returns:
            bool: Trạng thái có bóng đèn chiếu sáng chồng lên nhau (True hoặc False).
        """
        return self.__overlap

    def trans_bulb(self):
        """
        Đổi trạng thái bóng đèn của ô vuông.
        Nếu ô vuông không có bóng đèn, thêm bóng đèn vào ô vuông và chiếu sáng nó.
        Nếu ô vuông đã có bóng đèn, gỡ bóng đèn ra.
        Returns:
            bool: Trạng thái có bóng đèn sau khi chuyển đổi (True hoặc False).
        """
        if self.__bulb is False:
            self.__bulb = True
            self.__illuminated = True
            self.symbol = 'L'
        else:
            self.__bulb = False
        return self.__bulb