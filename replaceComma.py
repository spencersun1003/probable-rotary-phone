import openpyxl

def replace_and_remove_characters_in_columns(file_path, old_char, new_char, columns):
    # 加载 Excel 文件
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # 遍历工作表中的行
    for row in sheet.iter_rows():
        for col_index in columns:
            cell = row[col_index]
            if cell.value:
                # 替换特定字符
                cell.value = cell.value.replace(old_char, new_char)
                # 移除换行符
                cell.value = cell.value.replace('\n', '').replace('\r', '')

    # 保存修改后的文件
    workbook.save(file_path)

# 调用函数
file_path = '广西2020.xlsx'  # 替换为你的文件路径
replace_and_remove_characters_in_columns(file_path, '、', '，', [2, 3])  # 第三列和第四列的索引分别是2和3