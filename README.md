# AI Cờ Vây (Go Game with AI Agents)

Dự án này xây dựng trò chơi cờ vây (Go) với các agent AI sử dụng thuật toán Minimax và Alpha-Beta pruning, cùng với các hàm đánh giá khác nhau.

## Cài đặt

### Yêu cầu hệ thống
- Python 3.6 trở lên
- NumPy
- Pygame
- Matplotlib
- Psutil

### Cài đặt các thư viện cần thiết

```bash
pip install numpy pygame matplotlib psutil
```

## Cấu trúc dự án

- `main.py`: File chính để chạy trò chơi cờ vây với giao diện đồ họa
- `board.py`: Biểu diễn bàn cờ và các luật của trò chơi
- `agents.py`: Các agent AI sử dụng thuật toán Minimax và Alpha-Beta pruning
- `evaluators.py`: Các hàm đánh giá cho các agent AI
- `ui.py`: Giao diện người dùng sử dụng Pygame
- `game_analytics.py`: Thu thập và phân tích số liệu về hiệu suất của các agent
- `tournament.py`: Chạy giải đấu so sánh hiệu suất giữa các agent

## Cấu trúc thư mục kết quả (results)

Các file trong thư mục kết quả tuân theo quy ước đặt tên như sau:

```
depth{độ_sâu}_games{số_trận}_{loại_biểu_đồ}_{kích_thước_bàn}.png
```

Trong đó:
- `{độ_sâu}`: Độ sâu tìm kiếm được sử dụng trong giải đấu (ví dụ: depth2)
- `{số_trận}`: Số trận đấu đã chơi cho mỗi cấu hình (ví dụ: games10)
- `{loại_biểu_đồ}`: Loại biểu đồ, có thể là:
  - `win_rates`: Biểu đồ tỷ lệ thắng của các agent
  - `time`: Biểu đồ thời gian trung bình mỗi nước đi
  - `memory`: Biểu đồ sử dụng bộ nhớ và tổng bộ nhớ
- `{kích_thước_bàn}`: Kích thước bàn cờ được sử dụng (ví dụ: 9 cho bàn 9x9)

Ví dụ: `depth2_games10_memory_9.png` là biểu đồ sử dụng bộ nhớ cho giải đấu chạy với độ sâu 2, 10 trận đấu, trên bàn cờ 9x9.

Khi có nhiều kích thước bàn cờ được sử dụng, tên file sẽ liệt kê tất cả các kích thước, ví dụ: `depth2_games10_memory_9x13x19.png`.

## Hướng dẫn sử dụng

### Chạy trò chơi với giao diện đồ họa

Để chạy trò chơi với giao diện đồ họa mặc định (bàn cờ 9x9):

```bash
python main.py
```

Với các tùy chọn khác:

```bash
python main.py --board-size 19 --depth 3 --num-games 5
```

Các tham số có thể điều chỉnh:
- `--board-size`: Kích thước bàn cờ (9, 13, hoặc 19)
- `--num-games`: Số trận đấu sẽ chơi
- `--depth`: Độ sâu tìm kiếm của các agent
- `--no-ui`: Chạy trò chơi trong chế độ console (không có giao diện đồ họa)
- `--plot`: Vẽ biểu đồ phân tích sau khi chơi
- `--save-plots`: Đường dẫn để lưu biểu đồ
- `--fullscreen`: Chạy trò chơi ở chế độ toàn màn hình

### Chạy giải đấu

Để chạy giải đấu so sánh hiệu suất giữa các agent trên các kích thước bàn cờ khác nhau:

```bash
python tournament.py
```

Với các tùy chọn khác:

```bash
python tournament.py --board-sizes 9 13 19 --num-games 10 --depth 2 --save-dir results
```

Các tham số có thể điều chỉnh:
- `--board-sizes`: Các kích thước bàn cờ để thử nghiệm
- `--num-games`: Số trận đấu cho mỗi cấu hình
- `--depth`: Độ sâu tìm kiếm cho các agent
- `--save-dir`: Thư mục để lưu biểu đồ kết quả

## Cách chơi

Khi chạy trò chơi với giao diện đồ họa, bạn có thể:

1. Chọn kích thước bàn cờ (9x9, 13x13, hoặc 19x19) bằng các nút ở bảng điều khiển bên phải
2. Bật/tắt chế độ tự động chơi (Autoplay) để xem các agent tự chơi với nhau
3. Đặt quân cờ bằng cách nhấp chuột vào các giao điểm trên bàn cờ (khi chế độ tự động chơi tắt)
4. Bấm nút "Pass" để bỏ lượt
5. Bấm nút "Reset Game" để bắt đầu trò chơi mới
6. Bật/tắt chế độ toàn màn hình (Fullscreen)

Trong trò chơi, bạn có thể xem:
- Người chơi hiện tại (Black/White)
- Trạng thái trò chơi
- Thông tin về các agent (thời gian trung bình mỗi nước đi, mức sử dụng bộ nhớ)

## Các agent AI

Dự án này có các agent AI sau:

1. **StoneCountAgent**: Sử dụng hàm đánh giá dựa trên số lượng quân cờ trên bàn
2. **LibertyCountAgent**: Sử dụng hàm đánh giá dựa trên số lượng "liberties" (khả năng di chuyển) của các quân cờ
3. **RandomAgent**: Đi nước đi ngẫu nhiên, dùng để so sánh và thử nghiệm

## Phân tích hiệu suất

Sau khi chạy các trận đấu hoặc giải đấu, bạn có thể xem các biểu đồ phân tích:
- Tỷ lệ thắng của mỗi agent
- Thời gian trung bình mỗi nước đi
- Mức sử dụng bộ nhớ

Các biểu đồ này có thể được lưu vào thư mục được chỉ định với tham số `--save-plots` hoặc `--save-dir`.

## Lưu ý

- Trò chơi cờ vây sử dụng phương pháp tính điểm Area Scoring
- Luật Ko được áp dụng để ngăn cản việc lặp lại các nước đi
- Trò chơi kết thúc khi có hai lượt bỏ qua liên tiếp, hoặc khi một bên có lợi thế áp đảo