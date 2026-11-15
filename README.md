# 🏡 My Home - Fullhouse 3D Villa Project

> **Dự án thiết kế kiến trúc 3D nhà phố 2 tầng hiện đại (5m × 18m trên khu đất 7m × 22m)**  
> *Nơi bình an, ấm áp, lưu giữ yêu thương và tiếng cười của ba chị em và gia đình.*

---

## 📌 Tổng Quan Công Trình

- **Địa điểm & Mặt tiền:** Hướng Tây, mặt tiền quốc lộ, ngang 7m × dài 22m.
- **Kích thước nhà xây:** Ngang 5m × Dài 18m (2 tầng).
- **Hành lang đường luồng:** 2m xuyên suốt chiều dài (cho xe máy/xe đạp ra sân sau, mở toàn bộ cửa sổ đón gió tươi).
- **Quy mô:** 5 phòng ngủ (Ba Mẹ, Phòng đọc sách/khách tầng 1; Phòng Master, Chị Hai, Em Út tầng 2).
- **Tiện ích nổi bật:**
  - Phòng Master có đàn Piano upright, góc tập Yoga & Thiền định, WC riêng khép kín và ban công ngắm sao, tắm trăng.
  - Phòng khách kết hợp Gian thờ Phật Quan Âm trang nghiêm với vách ngăn gỗ CNC ấm cúng.
  - Bếp mở với quầy đảo mặt đá làm bánh, thông thoáng với vườn sau.
  - Sân trước có hiên trà/nhậu ngoài trời riêng cho Ba & các chú có mái che, không ảnh hưởng sinh hoạt trong nhà.
  - Sân sau có khu giặt phơi mái kính lấy sáng, chống mưa hắt và vườn rau hữu cơ sạch sẽ.
  - Tường đôi 220mm và cửa kính cách âm chống ồn quốc lộ; sàn gạch nhám chống trơn chuẩn R11.

---

## 📂 Danh Mục Tập Tin Trong Repository

| Tên File | Mô Tả | Cách Sử Dụng |
| :--- | :--- | :--- |
| **`Fullhouse_3D_Viewer.html`** | Trình xem 3D trực quan tương tác cao | Nhấp đúp chuột để mở bằng trình duyệt (Chrome, Edge) - Không cần cài đặt phần mềm |
| **`build_fullhouse_blender.py`** | Script Python tự động dựng mô hình trong Blender | Mở Blender ➔ Thẻ Scripting ➔ Open file ➔ Run Script |
| **`Fullhouse_Model.obj`** & **`.mtl`** | Mô hình 3D định dạng Wavefront tiêu chuẩn | Import trực tiếp vào Blender, SketchUp, 3ds Max, Rhino |
| **`README.md`** | Tài liệu hướng dẫn và thông tin dự án | Đọc trên GitHub |

---

## 🚀 Hướng Dẫn Sử Dụng

### 1. Xem Ngay Mô Hình 3D (Không Cần Cài Đặt)
- Mở tệp **`Fullhouse_3D_Viewer.html`** trên trình duyệt Web (Google Chrome, Microsoft Edge, Firefox, Safari).
- Sử dụng chuột:
  - **Chuột trái:** Xoay 360°.
  - **Chuột phải:** Di chuyển / Pan góc nhìn.
  - **Cuộn chuột:** Phóng to / Thu nhỏ.
- Thanh công cụ phía dưới & bên phải:
  - Bóc tách từng tầng (Tầng 1, Tầng 2, Tầng Mái, Tách tầng thẳng đứng).
  - Khám phá nhanh từng phòng (Phòng Master, Đàn Piano, Gian Thờ, Quầy Bánh, Vườn Rau...).
  - Chuyển đổi ánh sáng **Ban Ngày ☀️ / Ban Đêm 🌓**.

### 2. Mở Trong Blender
1. Khởi động **Blender** (khuyên dùng bản 3.0 trở lên hoặc 4.x).
2. Chuyển sang thẻ tab **Scripting** trên thanh menu trên cùng.
3. Bấm **Open** và chọn file **`build_fullhouse_blender.py`**.
4. Bấm nút **Run Script** (hoặc nhấn `Alt + P`).
5. Bấm phím **Z** ➔ Chọn **Material Preview** để xem đầy đủ vật liệu, ánh sáng và cây xanh.
