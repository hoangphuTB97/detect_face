import cv2
import yaml
import numpy as np
import datetime
import sqlite3

from unidecode import unidecode
from scipy.spatial import distance
from libs.tracker.sort import Sort
from database.new_database import DatabaseManager
from libs.face_detection.detect_face import FaceDetection
from libs.face_extract_feature.extract_feature import FaceExtractFeature
from libs.utils import convert_faceobject_to_numpy, align_face

 
configs_path = "./configs.yaml"
with open(configs_path) as f:
    configs = yaml.load(f, Loader=yaml.FullLoader)

cap = cv2.VideoCapture(0)
face_detection = FaceDetection(configs)
face_tracker = Sort()
face_extract_feature =  FaceExtractFeature(configs)

 
# Lấy tất cả các đặc trưng từ cơ sở dữ liệu
db_manager = DatabaseManager('C:/Users/Admin/Desktop/face_ncnn/database/database.db')
list_emps = db_manager.select_all_from_employees()
last_recognized_time = None
while True:
    ret, frame = cap.read()
    if frame is None:
        break
    # Detect face
    faceobjects = face_detection.detect(frame)

    if len(faceobjects):
        bboxes, landmarks = convert_faceobject_to_numpy(faceobjects)
        # Sử dụng tracker để gán id cho đối tượng face
        track_bboxes, track_landmarks = face_tracker.update(bboxes, landmarks)
        if len(track_bboxes):
            for i in range(len(track_bboxes)):
                x1, y1, x2, y2 = track_bboxes[i][:4].astype(int)
                landmark = track_landmarks[i]
                # Căn chỉnh face
                warped = align_face(frame, landmark)
                # extract feature face
                feature = face_extract_feature.extract(warped)
                # print(feature.shape)

                min_dst = None
                min_record = None
                threshold = 1.05

                # Khởi tạo một biến là None, cập nhật nó với khoảng cách nhỏ nhất tìm thấy trong mỗi lần lặp
                # Ngưỡng cần so sánh nếu lớn hơn 1.05 thì ta bỏ qua
                for record in list_emps:
                    dst = distance.euclidean(feature, record[-1])
                    if (min_dst is None or dst < min_dst) and dst <= threshold:
                        min_dst = dst
                        min_record = record

                if min_dst is not None:
                    # print("Khoảng cách nhỏ nhất:", min_dst)
                    # print("Bản ghi tương ứng:", min_record)
                    current_time = datetime.datetime.now()
                    # Kiểm tra xem đã có bản ghi check-in nào cho nhân viên này trong ngày hiện tại chưa
                    existing_records = db_manager.select_from_attendance(min_record[0], current_time.strftime("%Y-%m-%d"))
                    if len(existing_records) == 0:
                    # Nếu chưa có, thêm bản ghi check-in mới
                        db_manager.insert_into_attendance(min_record[0], current_time.strftime("%Y-%m-%d %H:%M:%S"), current_time.strftime("%Y-%m-%d %H:%M:%S"))
                        last_recognized_time = current_time
                    else:
                        if last_recognized_time is None or (current_time - last_recognized_time).total_seconds() > 60:
                            
                    # Nếu đã có, cập nhật thời gian check-out
                            db_manager.update_attendance_check_out(min_record[0], current_time.strftime("%Y-%m-%d %H:%M:%S"))
                            last_recognized_time = current_time
                    # print("OK babe:", min_record[1])
                    
                    # Hiển thị tên đã được điểm danh
                    cv2.putText(frame, "Nhan vien:" + unidecode(min_record[1]), (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

                cv2.rectangle(frame, (x1,y1), (x2, y2), (255,255,0), 2)
                cv2.putText(frame, str(int(track_bboxes[i][4])), (x1,y1),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0),2)
                for point in landmark:
                    cv2.circle(frame, (int(point[0]), int(point[1])), 2, (0, 255, 255), -1,)

    cv2.imshow("Avatar",frame)
    if cv2.waitKey(25) & 0xFF == ord('z'):
        break
cap.release()
cv2.destroyAllWindows()
db_manager.close_connection()
