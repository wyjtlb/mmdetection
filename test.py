import os
import shutil

def organize_labelme_jsons(img_train_dir, img_val_dir, json_source_dir, json_train_save_dir, json_val_save_dir):
    """
    根据图片文件夹中的文件名，将对应的 Labelme JSON 文件分发到不同文件夹。
    """
    # 确保保存 JSON 的目录存在
    os.makedirs(json_train_save_dir, exist_ok=True)
    os.makedirs(json_val_save_dir, exist_ok=True)

    # 1. 获取训练集和验证集的所有图片基本名称（不含后缀）
    # 例如：123.jpg -> 123
    train_img_names = {os.path.splitext(f)[0] for f in os.listdir(img_train_dir) if not f.startswith('.')}
    val_img_names = {os.path.splitext(f)[0] for f in os.listdir(img_val_dir) if not f.startswith('.')}
    tmp = []
    for img_name in train_img_names:
        tmp.append(img_name.split('_')[0] + '_' + img_name.split('_')[1] + '_' + img_name.split('_')[2])
    train_img_names = tmp[:]
    tmp = []
    for img_name in val_img_names:
        tmp.append(img_name.split('_')[0] + '_' + img_name.split('_')[1] + '_' + img_name.split('_')[2])
    val_img_names = tmp[:]
    print(f"训练集图片数: {len(train_img_names)}")
    print(f"验证集图片数: {len(val_img_names)}")

    count_train = 0
    count_val = 0
    count_missing = 0

    # 2. 遍历源 JSON 文件夹
    for json_file in os.listdir(json_source_dir):
        if json_file.endswith('.json'):
            # 获取 JSON 文件的基本名称（不含 .json）
            json_base_name = os.path.splitext(json_file)[0]
            source_path = os.path.join(json_source_dir, json_file)
            json_base_name = json_base_name.split('_')[0] + '_' + json_base_name.split('_')[1] + '_' + json_base_name.split('_')[2]
            # 3. 匹配并移动（或复制）
            if json_base_name in train_img_names:
                shutil.copy(source_path, os.path.join(json_train_save_dir, json_file))
                count_train += 1
            elif json_base_name in val_img_names:
                shutil.copy(source_path, os.path.join(json_val_save_dir, json_file))
                count_val += 1
            else:
                count_missing += 1

    print("-" * 30)
    print(f"处理完成！")
    print(f"移动到训练集 JSON 数: {count_train}")
    print(f"移动到验证集 JSON 数: {count_val}")
    print(f"未匹配到的 JSON 数: {count_missing}")

# --- 路径配置 (请根据你的实际路径修改) ---
organize_labelme_jsons(
    img_train_dir='/Users/wuyongjie/Desktop/砂糖橘标签/YOLODataset/images/train',  # 训练集图片所在文件夹
    img_val_dir='/Users/wuyongjie/Desktop/砂糖橘标签/YOLODataset/images/val',      # 验证集图片所在文件夹
    json_source_dir='/Users/wuyongjie/Desktop/砂糖橘标签',   # 你那194个JSON所在的原始文件夹
    json_train_save_dir='/Users/wuyongjie/Desktop/砂糖橘标签/train', # 训练集JSON存放处
    json_val_save_dir='/Users/wuyongjie/Desktop/砂糖橘标签/val'      # 验证集JSON存放处
)