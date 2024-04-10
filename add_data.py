import cv2
import yaml
import sqlite3
import numpy as np

from libs.tracker.sort import Sort
from database.create_data import DatabaseManager
from libs.face_detection.detect_face import FaceDetection
from libs.face_extract_feature.extract_feature import FaceExtractFeature
from libs.utils import convert_faceobject_to_numpy, align_face


configs_path = "./configs.yaml"
with open(configs_path) as f:
    configs = yaml.load(f, Loader=yaml.FullLoader)

face_detection = FaceDetection(configs)
face_extract_feature =  FaceExtractFeature(configs)

#Kết nối với cơ sở dữ liệu
db_manager = DatabaseManager('database/databases.db')

#Đọc dữ liệu đầu vào
image = cv2.imread('Facebase/trandieulinh.jpg')

faces = face_detection.detect(image)
if faces:
    bboxes, landmarks = convert_faceobject_to_numpy(faces)
    aligned_face = align_face(image, landmarks[0])
    feature = face_extract_feature.extract(aligned_face)

    # Thêm thông tin vào cơ sở dữ liệu
    db_manager.insert_into_employees('Trần Diệu Linh','Nữ','2002', 'Nhân Viên', 'HCNS', feature)
    print("Thêm thông tin thành công!")
db_manager.close_connection()
