# Đồ án cuối kì môn Lập trình hướng đối tượng (OOP)

## Đề tài: "LẬP TRÌNH GAME GIẢI ĐỐ TURN ON THE LIGHTS"

Đồ án này nhằm mục tiêu áp dụng những kiến thức đã học trong môn IT002.O21 tại trường Đại học Công nghệ Thông tin - Đại học Quốc gia Hồ Chí Minh vào việc xây dựng một trò chơi điện tử hoàn chỉnh. Trò chơi được phát triển bằng thư viện Pygame, một thư viện phổ biến dành cho lập trình game trong Python. Đồ án này không chỉ nhằm giúp sinh viên củng cố và nâng cao kỹ năng lập trình hướng đối tượng mà còn phát triển khả năng tư duy logic và sáng tạo.

## Mô tả trò chơi

“Bật tắt bóng đèn” là một trò chơi giải đố với mục tiêu là chiếu sáng toàn bộ bảng chơi. Dưới đây là mô tả chi tiết về luật chơi và cách chơi trò chơi này:

### Cấu trúc bảng chơi

- Bảng chơi là một lưới hình vuông, kích thước m x n ô.
- Mỗi ô trên bảng có thể là một ô trắng, ô đen hoặc ô có số.

### Mục tiêu

- Mục tiêu của trò chơi là đặt các bóng đèn vào các ô trắng sao cho mọi ô trắng trên bảng đều được chiếu sáng.

### Quy tắc đặt bóng đèn

- Bóng đèn chỉ có thể được đặt vào các ô trắng.
- Một bóng đèn sẽ chiếu sáng tất cả các ô trắng theo các hướng lên, xuống, trái, phải cho đến khi gặp phải một ô đen hoặc ranh giới của bảng.

### Quy tắc số trên các ô đen

- Một số ô đen có thể chứa một con số từ 0 đến 4.
- Con số này chỉ ra số lượng bóng đèn phải được đặt trong các ô kề (tối đa là 4 ô kề trong các hướng lên, xuống, trái, phải).
- Các ô đen không có số không có yêu cầu về số lượng bóng đèn kề.

### Quy tắc ánh sáng

- Tất cả các ô trắng phải được chiếu sáng.
- Không có hai bóng đèn nào được chiếu sáng lẫn nhau. Điều này có nghĩa là không có hai bóng đèn nào có thể được đặt sao cho chúng nằm trên cùng một hàng hoặc cột mà không có một ô đen nào ở giữa.

### Quy tắc kiểm tra

- Sau khi đặt xong các bóng đèn, người chơi có thể kiểm tra giải pháp của mình.
- Nếu tất cả các ô trắng được chiếu sáng và tất cả các ô đen chứa số có đúng số bóng đèn kề, giải pháp được coi là hợp lệ và người chơi thắng cuộc.

### Yêu cầu hệ thống

- Python 3.x
- Thư viện Pygame

### Hướng dẫn cài đặt

1. Clone kho lưu trữ về máy:

    ```sh
    git clone https://github.com/tentuoigia/turn-on-the-lights.git
    ```

2. Cài đặt các thư viện cần thiết:

    ```sh
    pip install pygame
    ```

### Chạy trò chơi

Chạy tệp `main.py` để bắt đầu trò chơi:

```sh
python main.py
