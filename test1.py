import json
import re
import os

# --- 路径配置 ---
json_path = '/Users/wuyongjie/PycharmProjects/mmdetection/YOLODataset/annotations/val.json'  # 你的原始 JSON 路径
output_json = '/Users/wuyongjie/PycharmProjects/mmdetection/YOLODataset/annotations/val.json'  # 处理后的 JSON 路径


def fix_json_filenames(path, save_path):
    # 1. 加载原始数据
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"开始处理: {len(data['images'])} 张图片的标注信息...")

    count = 0
    # 2. 遍历 images 数组
    for img_info in data['images']:
        old_name = img_info['file_name']

        # 3. 使用正则表达式提取 4 位数字序号 (例如从 satang_image_0122... 提取 0122)
        match = re.search(r'(\d{4})', old_name)

        if match:
            seq_num = match.group(1)
            # 统一修改为 序号.jpg
            new_name = f"{seq_num}.jpg"

            img_info['file_name'] = new_name
            count += 1
        else:
            print(f"警告：无法在文件名 '{old_name}' 中找到 4 位数字序号")

    # 4. 保存修改后的 JSON
    with open(save_path, 'w', encoding='utf-8') as f:
        # indent=4 让生成的 JSON 文件易于阅读检查
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"--- 处理完成 ---")
    print(f"共替换了 {count} 个文件名。")
    print(f"新 JSON 已保存至: {save_path}")


# 执行函数
fix_json_filenames(json_path, output_json)