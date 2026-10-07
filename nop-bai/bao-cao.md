# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Trần Đại Nhân |
| MSSV | 2A202602642 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/hugebenevolence/K4-L3-DAY21-TranDaiNhan-2A202602642-CI-CD-for-AI-Systems |
| Ngày cập nhật | 08/10/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---:|---:|---:|---:|---:|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | **0.7149** | 0.8740 |

**Chọn bộ 3** vì F1 lớp dương cao nhất trên cùng holdout 500 mẫu và vượt ngưỡng 0.65. Bộ 1 có accuracy cao hơn nhưng F1 thấp hơn, nên không phù hợp làm mô hình cuối.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Chỉ 24,8% mẫu thuộc lớp thu nhập trên 50K. Mô hình luôn đoán thu nhập thấp vẫn đạt accuracy 0,752 nhưng F1 lớp dương bằng 0. F1 kết hợp precision và recall của lớp cần phát hiện, nên pipeline chặn triển khai khi `f1_score(y_eval, predictions) < 0.65`.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| MLflow lỗi phụ thuộc | `setuptools` và SQLAlchemy mới xung đột MLflow 2.13. | Giới hạn `setuptools<81`, `sqlalchemy<2.1`. |
| Dữ liệu lớn | CSV cần phiên bản riêng. | DVC đẩy dữ liệu lên S3; `dvc status -c` đồng bộ. |
| Release qua SSH | Khóa SSH đầu có mật khẩu, runner không thể dùng tự động. | Tạo khóa triển khai riêng, thêm public key vào EC2 và private key vào GitHub Secret; Release đã qua. |
| Thử Quality Gate | Cấu hình yếu đạt F1 0.6051. | Nhánh `quality-gate-proof` cho thấy Release bị bỏ qua. |

---

## 4. So Sánh Bước 2 và Bước 3

| | f1_score | accuracy |
|---|---:|---:|
| Bước 2 (chỉ `train_batch1`, chạy CI) | 0.7149 | 0.8740 |
| Bước 3 (thêm `train_batch2`, chạy CI) | 0.7354 | 0.8820 |

**Nhận xét:** Với 44.722 thay vì 22.361 mẫu, F1 tăng 0.0205 trên cùng holdout. Cả hai số đều từ CI; commit chỉ đổi con trỏ dữ liệu DVC đã tự kích hoạt đủ bốn job. Thêm dữ liệu không đảm bảo điểm luôn tăng.
