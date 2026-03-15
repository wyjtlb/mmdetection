import os
import json
import mmcv
from mmengine.utils import track_iter_progress


def convert_labelme_to_coco(json_dir, out_file):
    """
    将 Labelme 的多个 JSON 文件转换为一个标准的 COCO 格式 JSON
    """
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json') and f != out_file]

    # 基础结构
    coco_format_json = {
        "images": [],
        "annotations": [],
        "categories": [{"id": 0, "name": "orange"}]  # 根据你的项目修改类别名
    }

    obj_count = 0

    print(f"开始转换，共找到 {len(json_files)} 个标注文件...")

    for idx, json_file in enumerate(track_iter_progress(json_files)):
        json_path = os.path.join(json_dir, json_file)

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 1. 处理图片信息
        img_name = data['imagePath'].split('/')[-1]  # 获取文件名
        # 如果 Labelme 没存宽高，用 mmcv 读取
        height = data.get('imageHeight')
        width = data.get('imageWidth')

        coco_format_json["images"].append({
            "id": idx,
            "file_name": img_name,
            "height": height,
            "width": width
        })

        # 2. 处理标注信息 (Shapes)
        for shape in data['shapes']:
            if shape['shape_type'] != 'rectangle':
                continue  # 如果不是矩形框则跳过

            points = shape['points']
            # Labelme 矩形框通常存两个点: [[x1, y1], [x2, y2]]
            x1, y1 = points[0]
            x2, y2 = points[1]

            # 计算 bbox: [x, y, width, height]
            xmin, xmax = min(x1, x2), max(x1, x2)
            ymin, ymax = min(y1, y2), max(y1, y2)
            w = xmax - xmin
            h = ymax - ymin

            coco_format_json["annotations"].append({
                "id": obj_count,
                "image_id": idx,
                "category_id": 0,  # 这里对应上面 categories 的 id
                "bbox": [xmin, ymin, w, h],
                "area": w * h,
                "segmentation": [],  # 目标检测通常不需要分割点，留空即可
                "iscrowd": 0
            })
            obj_count += 1

    # 保存结果
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(coco_format_json, f, indent=4)
    print(f"\n转换完成！结果已保存至: {out_file}")


if __name__ == '__main__':
    # 填入你 JSON 文件所在的文件夹路径
    train_dir = '/Users/wuyongjie/Desktop/砂糖橘标签/train'
    val_dir = '/Users/wuyongjie/Desktop/砂糖橘标签/val'

    convert_labelme_to_coco(train_dir, os.path.join(train_dir, 'annotation_coco.json'))
    convert_labelme_to_coco(val_dir, os.path.join(val_dir, 'annotation_coco.json'))