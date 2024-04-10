import cv2
import ncnn
import numpy as np


class FaceExtractFeature:
    def __init__(self, configs):
        self.configs = configs

        self.bin_path = self.configs["face_extract_feature"]["model"]["bin_path"]
        self.param_path = self.configs["face_extract_feature"]["model"]["param_path"]
        self.use_vulkan_compute = self.configs["face_extract_feature"]["model"]["use_vulkan_compute"]

        self.mean_vals =  self.configs["face_extract_feature"]["preprocess"]["mean_vals"]
        self.norm_vals = self.configs["face_extract_feature"]["preprocess"]["norm_vals"]

        self.net = ncnn.Net()
        self.net.opt.use_vulkan_compute = self.use_vulkan_compute
        self.net.opt.num_threads = ncnn.get_big_cpu_count()

        self.net.load_param(self.param_path)
        self.net.load_model(self.bin_path)

    def extract(self, aimg):
        img_h = aimg.shape[0]
        img_w = aimg.shape[1]
        mat_in = ncnn.Mat.from_pixels(aimg, ncnn.Mat.PixelType.PIXEL_BGR2RGB, img_w, img_h)
        mat_in.substract_mean_normalize(self.mean_vals, self.norm_vals)

        ex = self.net.create_extractor()
        ex.input("in0", mat_in)
        ret, mat_out = ex.extract("out0")
        feature = np.array(mat_out, np.float32)
        feature_norm = np.linalg.norm(feature)
        feature = feature/feature_norm
        return feature