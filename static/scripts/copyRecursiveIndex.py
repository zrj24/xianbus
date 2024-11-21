import os
import shutil

# 定义要查找的文件名
file_to_find = "index.md"
file_to_copy = "index.zh-cn.md"

# 遍历当前目录的所有子目录，跳过根目录
for root, dirs, files in os.walk("."):
    # 跳过当前目录（"."），只处理子目录
    if root == ".":
        continue

    # 遍历当前目录下的所有文件
    for file in files:
        # 检查文件是否是 index.md
        if file == file_to_find:
            # 构建文件的完整路径
            original_file = os.path.join(root, file)

            # 设置新的文件名为 index.zh-cn.md
            new_file = os.path.join(root, file_to_copy)

            # 复制并重命名
            shutil.copy(original_file, new_file)
            print(f"'{original_file}' 已复制为 '{new_file}'")