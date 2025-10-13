import numpy as np
import os
from PIL import Image

# 이미지 폴더 경로 (Windows 백슬래시 이스케이프 문제를 피하기 위해 raw string 사용)
im_folder = r'C:\Users\ichan\Desktop\project\images'

# 처리할 이미지 확장자 목록
valid_exts = {'.jpg'}

for filename in os.listdir(im_folder):
    file_lower = filename.lower()
    ext = os.path.splitext(file_lower)[1]
    if ext not in valid_exts:
        continue

    image_path = os.path.join(im_folder, filename)
    if not os.path.isfile(image_path):
        continue

    try:
        with Image.open(image_path) as im:
            im = im.convert('RGB')
            pix = np.array(im)
    except Exception as e:
        print(f"[스킵] '{filename}' 열기 실패: {e}")
        continue

    #pixel 값 부여 후, filtering pixel 제거
    height, width = pix.shape[0], pix.shape[1]

    filtered_pixels = []
    total_r, total_g, total_b = 0, 0, 0

    for y in range(height):
        for x in range(width):
            r, g, b = pix[y][x]
            if (r > 80 and g > 40 and b < 100) and (r > g + 20):
                filtered_pixels.append([x, y, r, g, b])
                total_r += r
                total_g += g
                total_b += b

    pixel_count = len(filtered_pixels)

    if pixel_count > 0:
        avg_r = total_r / pixel_count
        avg_g = total_g / pixel_count
        avg_b = total_b / pixel_count
        print(f"[{filename}] Average R: {avg_r:.2f}")
        print(f"[{filename}] Average G: {avg_g:.2f}")
        print(f"[{filename}] Average B: {avg_b:.2f}")
    else:
        print(f"[{filename}] 조건을 만족하는 픽셀 x.")
