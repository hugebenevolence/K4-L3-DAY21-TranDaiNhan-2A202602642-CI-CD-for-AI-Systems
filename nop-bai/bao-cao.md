# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Trần Đại Nhân |
| MSSV | 2A202602642 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/hugebenevolence/K4-L3-DAY21-TranDaiNhan-2A202602642-CI-CD-for-AI-Systems |
| Ngày nộp | 07/10/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---:|---:|---:|---:|---:|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | **0.7149** | 0.8740 |

**Bộ siêu tham số đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.

**Lý do:** Bộ thứ ba có F1 lớp dương cao nhất trên cùng holdout 500 mẫu và vượt ngưỡng 0.65. Bộ thứ nhất có accuracy cao hơn (0.8780) nhưng F1 thấp hơn, cho thấy accuracy chưa đủ để chọn mô hình cho lớp thiểu số. Tổ hợp 50 cây và learning rate 0.05 cho F1 thấp nhất; thí nghiệm chưa tách riêng tác động từng tham số.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Khoảng 24,8% mẫu thuộc lớp thu nhập trên 50K. Mô hình luôn đoán thu nhập thấp vẫn đạt accuracy 0,752 nhưng F1 lớp dương bằng 0. F1 kết hợp precision và recall của lớp cần phát hiện, nên phát hiện cả dự đoán nhầm lẫn bỏ sót. Pipeline yêu cầu `f1_score(y_eval, predictions) >= 0.65`. Không dùng `average="weighted"` vì lớp đa số kéo điểm lên; `average="macro"` cũng không đo trực tiếp F1 của lớp dương.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| MLflow không khởi động | `setuptools` mới và SQLAlchemy 2.1 xung đột với MLflow 2.13. | Giới hạn `setuptools<81`, `sqlalchemy<2.1`; test và train đã qua. |
| CSV không đưa trực tiếp vào Git | Dữ liệu cần phiên bản riêng. | Dùng DVC với S3; `dvc push` và `dvc status -c` thành công. |
| Chưa có Release trên VM | AWS từ chối quyền EC2; fork chưa chạy Actions. | Chờ quyền EC2 và bật Actions/Secrets để chạy pipeline. |

---

## 4. So Sánh Bước 2 và Bước 3

| | f1_score | accuracy |
|---|---:|---:|
| Bước 2 (chỉ `train_batch1`, chạy local) | 0.7149 | 0.8740 |
| Bước 3 (thêm `train_batch2`, chạy local) | 0.7354 | 0.8820 |

**Nhận xét:** Tăng tập huấn luyện từ 22.361 lên 44.722 mẫu giúp F1 tăng 0.0205 và accuracy tăng 0.0080 trên cùng holdout. Đây là quan sát của lần chạy local, chưa chứng minh thêm dữ liệu luôn cải thiện mô hình. Cần đối chiếu với artifact CI sau khi Actions được bật.
