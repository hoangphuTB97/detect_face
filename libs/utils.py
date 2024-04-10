import cv2
import numpy as np

from skimage import transform as trans

ARCFACE_DST = np.array([[38.2946, 51.6963], [73.5318, 51.5014], 
                        [56.0252, 71.7366],[41.5493, 92.3655], 
                        [70.7299, 92.2041]],dtype=np.float32)


def align_face(img, landmark, image_size=112):
    assert landmark.shape == (5, 2)
    assert image_size%112==0 or image_size%128==0
    if image_size%112==0:
        ratio = float(image_size)/112.0
        diff_x = 0
    else:
        ratio = float(image_size)/128.0
        diff_x = 8.0*ratio
    dst = ARCFACE_DST * ratio
    dst[:,0] += diff_x
    tform = trans.SimilarityTransform()
    tform.estimate(landmark, dst)
    M = tform.params[0:2, :]
    warped = cv2.warpAffine(img, M, (image_size, image_size), borderValue=0.0)
    return warped


def convert_faceobject_to_numpy(faceobjects):
    bboxes = []
    landmarks = []
    for faceobject in faceobjects:
        bbox = [faceobject.rect.x, faceobject.rect.y, 
                faceobject.rect.x + faceobject.rect.w, 
                faceobject.rect.y + faceobject.rect.h, 
                faceobject.prob]
        
        landmark = [[faceobject.landmark[0].x, faceobject.landmark[0].y], 
                    [faceobject.landmark[1].x, faceobject.landmark[1].y], 
                    [faceobject.landmark[2].x, faceobject.landmark[2].y],
                    [faceobject.landmark[3].x, faceobject.landmark[3].y],
                    [faceobject.landmark[4].x, faceobject.landmark[4].y]]

        bboxes.append(bbox)
        landmarks.append(landmark)
        
    return np.array(bboxes), np.array(landmarks)