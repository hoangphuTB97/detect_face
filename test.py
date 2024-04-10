import cv2
import yaml

from libs.tracker.sort import Sort
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


while True:
    ret, frame = cap.read()
    if frame is None:
        break
    # Detect face
    faceobjects = face_detection.detect(frame)
    if len(faceobjects):
        # Convert dạng faceobjects thành bboxes và landmarks thuộc kiểu numpy array
        # bbox là : [x1, y1 , x2, y2, prob]
        # lanmark: gồm 5 điểm là 2 mắt, 1 mũi và 2 bên mép miệng của khuôn mặt
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

                cv2.rectangle(frame, (x1,y1), (x2, y2), (255,255,0), 2)
                cv2.putText(frame, str(int(track_bboxes[i][4])), (x1,y1),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0),2)
                for point in landmark:
                    cv2.circle(frame, (int(point[0]), int(point[1])), 2, (0, 255, 255), -1,)
            
    
    cv2.imshow("avatar",frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
