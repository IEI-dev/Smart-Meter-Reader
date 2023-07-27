import numpy as np
import cv2
import openvino.runtime as ov



class dataprocess:
    def erode(seg_results, erode_kernel):
        kernel = np.ones((erode_kernel, erode_kernel), np.uint8)
        eroded_results = cv2.erode(seg_results.astype(np.uint8), kernel)
        return eroded_results

    def roi_process(img):
        resize_img = img.transpose(2, 0, 1) / 255
        img_mean = np.array([0.5, 0.5, 0.5]).reshape((3, 1, 1))
        img_std = np.array([0.5, 0.5, 0.5]).reshape((3, 1, 1))
        resize_img -= img_mean
        resize_img /= img_std
        return resize_img
    
    def segmentation_map_to_image(result: np.ndarray, colormap: np.ndarray, remove_holes: bool = False) -> np.ndarray:
        result = result.astype(np.uint8)

        contour_mode = cv2.RETR_EXTERNAL if remove_holes else cv2.RETR_TREE
        #np.zeros((512, 512, 3), dtype=np.uint8)
        mask = np.zeros((result.shape[0], result.shape[1], 3), dtype=np.uint8)

        for label_index, color in enumerate(colormap):
            label_index_map = result == label_index
            label_index_map = label_index_map.astype(np.uint8) * 255
            contours, hierarchies = cv2.findContours(
                label_index_map, contour_mode, cv2.CHAIN_APPROX_SIMPLE
            )
            cv2.drawContours(
                mask,
                contours,
                contourIdx=-1,
                color=color.tolist(),
                thickness=cv2.FILLED,
            )

        return mask




#load model
seg_model_path = "model/openvino/meter_seg_model/model.xml"
seg_model_shape = {'image': [ov.Dimension(1, 2), 3, 512, 512]}
ie_core = ov.Core()
model = ie_core.read_model(model=seg_model_path)
model.reshape(seg_model_shape)
compiled_model = ie_core.compile_model(model=model, device_name="CPU")

#inference
roi_imgs= cv2.imread("image/temp/test22.png")
roi_imgs = [dataprocess.roi_process(roi_imgs )]
output_layer = compiled_model.output(0)
seg_result = compiled_model(np.array(roi_imgs))[output_layer]

#image optimize erode(remove noise)
results = np.argmax(seg_result[0], axis=0)
seg_results = dataprocess.erode(results, erode_kernel = 4)

# draw back result  [black-background(#1C1C1C),red-pointer(#EE2C2C),white-scale(#FAFAFA)]
COLORMAP = np.array([[28, 28, 28], [238, 44, 44], [250, 250, 250]])
mask_list = dataprocess.segmentation_map_to_image(seg_results, COLORMAP)


#output
cv2.imwrite("./output.jpg", cv2.cvtColor(mask_list, cv2.COLOR_RGB2BGR))
print("The segmentation result image has been saved as \"segmentation_results.jpg\" in data")

