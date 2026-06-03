# Hướng dẫn Cài đặt & Chạy Mô hình tạo Video Wan 2.1 trên ComfyUI

Tài liệu này hướng dẫn chi tiết cách thiết lập môi trường và khởi chạy mô hình tạo video **Wan 2.1 (phiên bản 1.3B)** tối ưu cho card đồ họa NVIDIA RTX 4050 6GB VRAM và 16GB RAM trên Windows.

---

## 📋 Yêu cầu hệ thống trước khi cài đặt
* **Hệ điều hành:** Windows 10/11.
* **Python:** Khuyến nghị dùng **Python 3.12** (Tránh dùng Python 3.14 vì PyTorch CUDA chưa hỗ trợ chính thức).
* **Card đồ họa (GPU):** NVIDIA GPU (đã cài đặt Driver mới nhất hỗ trợ CUDA).

---

## 🛠️ Các bước thực hiện

### Bước 1: Khởi tạo và kích hoạt môi trường ảo (Virtual Environment)
Mở Terminal/PowerShell tại thư mục `d:\ComfyUI` và chạy các lệnh sau:
```powershell
# 1. Tạo môi trường ảo với Python 3.12
py -3.12 -m venv venv

# 2. Kích hoạt môi trường ảo
.\venv\Scripts\activate
```
*(Nếu kích hoạt thành công, bạn sẽ thấy chữ `(venv)` xuất hiện ở đầu dòng lệnh).*

### Bước 2: Cài đặt PyTorch hỗ trợ tăng tốc GPU (CUDA 12.4)
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```
*Lưu ý: File cài đặt nặng khoảng 2.5 GB, thời gian tải phụ thuộc vào tốc độ mạng của bạn.*

### Bước 3: Cài đặt các thư viện phụ thuộc (Dependencies)
```powershell
# Cài đặt thư viện chính của ComfyUI
pip install -r requirements.txt

# Cài đặt thư viện cho ComfyUI Manager
pip install -r manager_requirements.txt
```

### Bước 4: Tải tự động các file Mô hình (Models)
Chạy script Python được viết sẵn để tự động tải các file mô hình Wan 2.1 phù hợp nhất về đúng thư mục:
```powershell
python download_wan_models.py
```
* Các file mô hình được tải bao gồm:
  1. **Text Encoder (6.4 GB):** `umt5_xxl_fp8_e4m3fn_scaled.safetensors` lưu tại `models/text_encoders/`
  2. **VAE (242 MB):** `wan_2.1_vae.safetensors` lưu tại `models/vae/`
  3. **Video Model 1.3B (2.7 GB):** `wan2.1_t2v_1.3B_fp16.safetensors` lưu tại `models/diffusion_models/`

---

## 🚀 Khởi chạy dự án ComfyUI

Để chạy dự án ổn định và tránh lỗi tràn bộ nhớ (Access Violation/Out of Memory) trên card đồ họa 6GB VRAM, hãy dùng lệnh khởi động kèm tham số tối ưu sau:
```powershell
python main.py --enable-manager --lowvram
```
* **`--enable-manager`**: Bật tính năng quản lý Custom Nodes (ComfyUI Manager).
* **`--lowvram`**: Cơ chế thông minh tự động chia nhỏ và phân bổ mô hình giữa VRAM và RAM hệ thống, giúp chạy mượt mà trên card 6GB.

Sau khi chạy lệnh, truy cập giao diện web qua địa chỉ: **[http://127.0.0.1:8188](http://127.0.0.1:8188)**

---

## 🎬 Hướng dẫn tạo Video MP4

### 1. Load Workflow mẫu
* Tại giao diện web ComfyUI, kéo và thả file **`text_to_video_wan.json`** trực tiếp vào màn hình vẽ node (hoặc click nút **Load** ở menu bên trái $\rightarrow$ chọn file này).
* Nhấn nút **Refresh** ở menu bên phải để ComfyUI nhận diện các file mô hình vừa tải ở Bước 4.

### 2. Cài đặt xuất định dạng MP4
* Mở **Manager** (biểu tượng chữ C ở góc trái hoặc phím tắt `M`) $\rightarrow$ **Install Custom Nodes**.
* Tìm kiếm từ khóa: `Video Helper Suite` và nhấn **Install**.
* Khởi động lại ComfyUI trên Terminal để áp dụng thư viện mới.
* Trên giao diện web, double-click tìm kiếm node **`Video Combine`** để thay thế cho node `SaveAnimatedWEBP` cũ. 
* Cấu hình trong node `Video Combine`: chọn **`format = video/h264-mp4`** để xuất trực tiếp ra video `.mp4`.

### 3. Điều chỉnh thời lượng video (Số giây)
Thời lượng video được tính bằng công thức:
$$\text{Số giây} = \frac{\text{length (Tổng số frames)}}{\text{frame_rate (Tốc độ FPS)}}$$

* Chỉnh tổng số khung hình ở Node **`Empty HunyuanVideo 1.0 Latent`** (ô tham số **`length`**).
* Chỉnh tốc độ ở Node **`Video Combine`** (ô tham số **`frame_rate`**).
* *Ví dụ:* Chỉnh `length = 80` và `frame_rate = 16` $\rightarrow$ Bạn sẽ có video dài đúng **5 giây** chuyển động mượt mà.

---

## 🔒 Nguyên tắc bảo mật khi sử dụng API & Git
* Kho lưu trữ (Repository) của bạn hiện đang ở chế độ công khai (Public).
* **Tuyệt đối không lưu trực tiếp** API Key, mật khẩu vào các file code Python khi push lên GitHub.
* Hãy lưu các thông tin bảo mật vào file **`.env`** ở thư mục gốc (file này đã được ẩn tự động trong `.gitignore` không bị đẩy lên GitHub) và gọi chúng ra bằng thư viện `python-dotenv`:
  ```python
  import os
  from dotenv import load_dotenv
  load_dotenv()
  api_key = os.getenv("API_KEY_NAME")
  ```
