import pandas as pd
import re

def process_excel(input_file, output_file):
    # 读取Excel文件，指定没有表头
    df = pd.read_excel(input_file, header=None)

    # 创建一个新的DataFrame来存储结果
    new_df = pd.DataFrame(columns=['获奖单位', '姓名', '完成人序号', '', '', '综合奖励名称', '成果名称'])

    # 遍历原始数据
    for _, row in df.iterrows():
        # 分割获奖人列（第三列，索引为2），并只取前三个姓名
        winners = str(row[2]).split('，')[:3]

        # 组合奖项名称和奖励等级
        combined_award = f"{row[5]}{row[4]}"  # 请替换某列索引为奖项名称和奖励等级的实际列索引

        # 对每个获奖人创建一个新行
        for index, name in enumerate(winners):
            new_row = {'获奖单位': row[3],  # 获奖单位为第四列，索引为3
                       '姓名': name.strip(),
                       '完成人序号': index + 1,
                       '': '',
                       '': '',
                       '综合奖励名称': row[6],
                       '成果名称': row[1]}  # 成果名称为第二列，索引为1
            new_df = new_df.append(new_row, ignore_index=True)

    # 将处理后的数据保存到新的Excel文件
    new_df.to_excel(output_file, index=False)

# 输入和输出文件的路径
input_file = '广西2020.xlsx'
output_file = 'result_2020广西科学技术奖.xlsx'

process_excel(input_file, output_file)