from datetime import datetime, timedelta
from app.db.database import engine, SessionLocal, Base
from app.db.models import User, Owner, Vehicle, Inspection, UserRole, VehicleStatus, InspectionResult
from app.core.security import get_password_hash

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(User).first():
        db.close()
        return

    # Tạo Người dùng
    admin = User(username="admin", full_name="Quản trị hệ thống", hashed_password=get_password_hash("admin123"), role=UserRole.ADMIN)
    staff = User(username="staff1", full_name="Nhân viên Tiếp nhận", hashed_password=get_password_hash("staff123"), role=UserRole.STAFF)
    inspector = User(username="inspector1", full_name="Đăng kiểm viên A", hashed_password=get_password_hash("123456"), role=UserRole.INSPECTOR)
    db.add_all([admin, staff, inspector])
    db.commit()

    # Tạo Chủ xe
    owner1 = Owner(full_name="Nguyễn Văn Hưng", phone="0912345678", address="Thành phố Hà Nội")
    owner2 = Owner(full_name="Công ty Vận tải An Bình", phone="0243888999", address="Thành phố Hồ Chí Minh")
    db.add_all([owner1, owner2])
    db.commit()

    now = datetime.now()
    # Tạo Phương tiện
    v1 = Vehicle(plate_number="29A-888.66", brand="Toyota Camry", manufacture_year=2020, expiration_date=now - timedelta(days=5), status=VehicleStatus.EXPIRED, owner_id=owner1.id)
    v2 = Vehicle(plate_number="51G-339.81", brand="Ford Ranger", manufacture_year=2021, expiration_date=now + timedelta(days=10), status=VehicleStatus.WARNING, owner_id=owner1.id)
    v3 = Vehicle(plate_number="30H-123.45", brand="Hyundai SantaFe", manufacture_year=2022, expiration_date=now + timedelta(days=180), status=VehicleStatus.SAFE, owner_id=owner2.id)
    db.add_all([v1, v2, v3])
    db.commit()

    # Tạo Lịch sử kiểm định
    insp1 = Inspection(vehicle_id=v3.id, inspection_date=now - timedelta(days=180), next_inspection_date=now + timedelta(days=180), result=InspectionResult.PASSED, notes="Đạt yêu cầu kỹ thuật và khí thải")
    db.add(insp1)
    db.commit()

    db.close()
    print("Khởi tạo dữ liệu mẫu thành công!")

if __name__ == "__main__":
    seed_data()