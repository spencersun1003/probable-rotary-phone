import pandas as pd
import time

def searchMatch(award_winner, previous_unit, next_lower_unit):
    if
    # 这里是searchMatch函数的实现，返回匹配的单位
    # 根据需要实现具体的逻辑
    print(award_winner, previous_unit, next_lower_unit)
    time.sleep(5)  # 模拟网络请求

    return "清华大学"


def process_excel(file_path):
    df = pd.read_excel(file_path, header=None)  # 指定没有表头
    processed_data = []

    for index, row in df.iterrows():
        # 使用索引访问列
        winners = row[2].split('，')[:3]  # 第二列（索引1）存储获奖人
        units = row[3].split('，')  # 第三列（索引2）存储获奖单位

        for i, winner in enumerate(winners):
            if i == 0:
                # 第一个获奖人的单位是第一个获奖单位
                matched_unit = units[0] if units else None
            else:
                previous_unit = units[i - 1] if i - 1 < len(units) else None
                next_lower_unit = units[i] if i < len(units) else None
                matched_unit = searchMatch(winner, previous_unit, next_lower_unit)

            processed_data.append([winner, matched_unit])

    # 创建一个新的DataFrame，没有列名
    new_df = pd.DataFrame(processed_data)
    return new_df


file_path = '广西2021.xlsx'  # 替换为你的Excel文件路径
result_df = process_excel(file_path)
result_df.to_excel('processed_list.xlsx', index=False, header=False)