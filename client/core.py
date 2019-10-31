import requests
import cv2
import os
import uuid
from enum import Enum, unique

HOST = os.getenv('YUNA_HOST')

@unique
class Code(Enum):
    EUPSTREAM = 502
    EUNCERTAIN = 721

def getExt(path):
    return path.split('.')[-1].lower()

def getFname(path):
    return path.split('/')[-1]

def reqDetection(url):
    try:
        req = requests.post(f'{HOST}/api/detect', json={'url': url})
    except requests.exceptions.RequestException as e:
        return None
    if (req.status_code != 200):
        return None
    return req.json()

def downloadFile(path):
    dst = f'cache/{getFname(path)}'
    try:
        req = requests.get(f'{HOST}/{path}')
    except requests.exceptions.RequestException as e:
        return None
    if (req.status_code != 200):
        return None
    with open(dst, 'wb') as f:
        f.write(req.content)
    return dst

def crop(path, bounds):
    dst = f'cache/{str(uuid.uuid4())}.{getExt(path)}'
    img = cv2.imread(path)
    bounds = [round(b) for b in bounds]
    cimg = img[bounds[1]:bounds[3], bounds[0]:bounds[2]].copy()
    cv2.imwrite(dst, cimg)
    return dst

def afd(url):
    faces = []
    res = reqDetection(url)
    if (res is None):
        return Code.EUPSTREAM

    for path in res:
        localPath = downloadFile(path)
        if (localPath is None):
            return Code.EUPSTREAM

        for face in res[path]:
            if (face['score'] < 0.85):
                faces.append(Code.EUNCERTAIN)
                continue
            faces.append(crop(localPath, face['bbox']))

    return faces
