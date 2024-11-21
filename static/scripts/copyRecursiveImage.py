import os
import shutil

# 定义要查找的文件扩展名
valid_extensions = [".jpg", ".jpeg", ".png"]

# 遍历当前目录的所有子目录，跳过根目录
for root, dirs, files in os.walk("."):
    # 跳过当前目录（"."），只处理子目录
    if root == ".":
        continue

    # 遍历当前目录下的所有文件
    for file in files:
        # 检查文件是否是 featured.jpg 或 featured.jpeg
        if file.startswith("featured") and os.path.splitext(file)[1] in valid_extensions:
            # 构建文件的完整路径
            original_file = os.path.join(root, file)
            
            # 根据原文件的扩展名设置新的文件名
            extension = os.path.splitext(file)[1]
            new_file = os.path.join(root, f"featured.zh-cn{extension}")

            # 复制并重命名
            shutil.copy(original_file, new_file)
            print(f"'{original_file}' 已复制为 '{new_file}'")