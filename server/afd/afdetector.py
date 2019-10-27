import numpy as np
import cv2
import tensorflow as tf
import os

import faster_rcnn_wrapper.FasterRCNNSlim
from nms_wrapper import NMSType, NMSWrapper

def detect(sess, rcnn_cls, image):
    # pre-processing image for Faster-RCNN
    img_origin = image.astype(np.float32, copy=True)
    img_origin -= np.array([[[102.9801, 115.9465, 112.7717]]])

    img_shape = img_origin.shape
    img_size_min = np.min(img_shape[:2])
    img_size_max = np.max(img_shape[:2])

    img_scale = 600 / img_size_min
    if np.round(img_scale * img_size_max) > 1000:
        img_scale = 1000 / img_size_max
    img = cv2.resize(img_origin, None, None, img_scale, img_scale, cv2.INTER_LINEAR)
    img_info = np.array([img.shape[0], img.shape[1], img_scale], dtype=np.float32)
    img = np.expand_dims(img, 0)

    # test image
    _, scores, bbox_pred, rois = rcnn_cls.test_image(sess, img, img_info)

    # bbox transform
    boxes = rois[:, 1:] / img_scale

    boxes = boxes.astype(bbox_pred.dtype, copy=False)
    widths = boxes[:, 2] - boxes[:, 0] + 1
    heights = boxes[:, 3] - boxes[:, 1] + 1
    ctr_x = boxes[:, 0] + 0.5 * widths
    ctr_y = boxes[:, 1] + 0.5 * heights
    dx = bbox_pred[:, 0::4]
    dy = bbox_pred[:, 1::4]
    dw = bbox_pred[:, 2::4]
    dh = bbox_pred[:, 3::4]
    pred_ctr_x = dx * widths[:, np.newaxis] + ctr_x[:, np.newaxis]
    pred_ctr_y = dy * heights[:, np.newaxis] + ctr_y[:, np.newaxis]
    pred_w = np.exp(dw) * widths[:, np.newaxis]
    pred_h = np.exp(dh) * heights[:, np.newaxis]
    pred_boxes = np.zeros_like(bbox_pred, dtype=bbox_pred.dtype)
    pred_boxes[:, 0::4] = pred_ctr_x - 0.5 * pred_w
    pred_boxes[:, 1::4] = pred_ctr_y - 0.5 * pred_h
    pred_boxes[:, 2::4] = pred_ctr_x + 0.5 * pred_w
    pred_boxes[:, 3::4] = pred_ctr_y + 0.5 * pred_h
    # clipping edge
    pred_boxes[:, 0::4] = np.maximum(pred_boxes[:, 0::4], 0)
    pred_boxes[:, 1::4] = np.maximum(pred_boxes[:, 1::4], 0)
    pred_boxes[:, 2::4] = np.minimum(pred_boxes[:, 2::4], img_shape[1] - 1)
    pred_boxes[:, 3::4] = np.minimum(pred_boxes[:, 3::4], img_shape[0] - 1)
    return scores, pred_boxes


def load_file_from_dir(dir_path):
    ret = []
    for file in os.listdir(dir_path):
        path_comb = os.path.join(dir_path, file)
        if os.path.isdir(path_comb):
            ret += load_file_from_dir(path_comb)
        else:
            ret.append(path_comb)
    return ret


def make_context(model='afdmodel/afdmodel.ckpt'):
    nms = NMSWrapper(NMSType.PY_NMS)
    cfg = tf.ConfigProto()
    cfg.gpu_options.allow_growth = True
    sess = tf.Session(config=cfg)
    net = FasterRCNNSlim()
    saver = tf.train.Saver()
    saver.restore(sess, model)
    return {
        'nms': nms,
        'session': sess,
        'net': net
    }


def recognize(context, input, nms_thresh=0.3, conf_thresh=0.8):
    assert os.path.exists(input), 'The input path does not exist'
    if os.path.isdir(input):
        files = load_file_from_dir(input)
    else:
        files = [input]
    file_len = len(files)

    result = {}
    for idx, file in enumerate(files):
        img = cv2.imread(file)
        scores, boxes = detect(context['session'], context['net'], img)
        boxes = boxes[:, 4:8]
        scores = scores[:, 1]
        keep = context['nms'](np.hstack([boxes, scores[:, np.newaxis]]).astype(np.float32), nms_thresh)
        boxes = boxes[keep, :]
        scores = scores[keep]
        inds = np.where(scores >= conf_thresh)[0]
        scores = scores[inds]
        boxes = boxes[inds, :]

        result[file] = []
        for i in range(scores.shape[0]):
            x1, y1, x2, y2 = boxes[i, :].tolist()
            new_result = {'score': float(scores[i]),
                          'bbox': [x1, y1, x2, y2]}
            result[file].append(new_result)

    return result
