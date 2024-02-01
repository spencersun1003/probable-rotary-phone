import os
import pandas as pd
from flask import Flask, render_template, request, jsonify, session
from openpyxl.workbook import Workbook
from flask_session import Session
from pandas import ExcelWriter
from searchInfo import searchKeywords
app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"  # 或者使用 "redis"，如果你偏好使用Redis
Session(app)
app.secret_key = 'your_secret_key'

# 假设output.xlsx是输出文件，确保这个文件存在或者在写入之前创建它
output_file = 'output.xlsx'

def write_to_excel(row_index, winner_name, matched_unit):

    try:
        if not os.path.exists(output_file):
            # 如果文件不存在，创建一个新的Workbook，并保存
            wb = Workbook()
            ws = wb.active
            ws.title = "Sheet1"
            ws.append(['行号', '姓名', '匹配单位'])  # 添加标题行
            wb.save(filename=output_file)
        # 读取现有的Excel文件，如果不存在则创建一个新的DataFrame
        try:
            df_output = pd.read_excel(output_file)
        except FileNotFoundError:
            df_output = pd.DataFrame(columns=['行号', '姓名', '匹配单位'])

        # 添加新行
        new_row = {'行号': row_index, '姓名': winner_name, '匹配单位': matched_unit}
        df_output = df_output.append(new_row, ignore_index=True)

        # 写回Excel文件
        with ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df_output.to_excel(writer, index=False, sheet_name='Sheet1')
    except Exception as e:
        print(f"Error writing to Excel: {e}")


def initialize_session(data):
    session['data'] = data
    session['current_row'] = 0
    session['current_winner_index'] = 0  # 从第一个获奖人开始
    session['current_winner_name']=''
    session['current_unit_index'] = 0  # 从第一个获奖单位开始
    session['last_unit'] = None#data[0][3].split('，')[0]  # 第一个单位

def invokeSearch(winner,unitA,unitB):
    queryA=winner+" "+unitA
    info_left = searchKeywords(winner, unitA,queryA)
    queryB = winner + " " + unitB
    if unitB[0]!="*":
        info_right = searchKeywords(winner, unitB,queryB)
    else:
        info_right = {'keywordMatch:':'','results':'not searching'}
    return info_left,info_right

def get_current_data():
    data = session.get('data', [])
    current_row = session.get('current_row', 0)
    current_winner_index = session.get('current_winner_index', 0)
    current_unit_index = session.get('current_unit_index', 0)
    last_unit = session.get('last_unit', None)


    if current_row < len(data):
        winner_split= data[current_row][2].split('，')
        winners = winner_split[:3] if len(winner_split)>=3 else winner_split
        units = data[current_row][3].split('，')

        if current_winner_index < len(winners) and current_unit_index < len(units):
            if not last_unit:
                #if it's the first winner, the first unit is the only option
                unitA=units[current_unit_index]
                unitB='*first author must match first unit, click left to continue'
            else:
                unitA=last_unit
                if current_unit_index+1 < len(units):
                    unitB=units[current_unit_index+1]
                else:
                    unitB="*no more units, click left to continue"
            winner_name= winners[current_winner_index]
            session['current_winner_name']=winner_name
            unit_options = [unitA,unitB]
            info_left,info_right=invokeSearch(winner_name,unitA,unitB)

            return {'winner':winner_name,'winner_index':current_winner_index+1, 'row_index':current_row+1,'units': unit_options,'info_left':info_left,'info_right':info_right}

    return None

@app.route('/')
def index():
    file_path = '广西2020.xlsx'  # Excel文件路径
    df = pd.read_excel(file_path, header=None)
    initialize_session(df.values.tolist())
    return render_template('index.html', data=get_current_data())

@app.route('/update_unit', methods=['POST'])
def update_unit():
    content = request.json
    row_index = session.get('current_row', 0) + 1  # Excel行号通常从1开始
    winner_name = session.get('current_winner_name', '')
    data=session.get('data', [])
    matched_unit = content['unit']
    if not matched_unit==session['last_unit'] and session['last_unit']!=None:
        session['current_unit_index'] += 1
    session['last_unit'] = matched_unit
    # 写入Excel文件
    write_to_excel(row_index, winner_name, matched_unit)

    session['current_winner_index'] += 1

    current_winner_index = session.get('current_winner_index', 0)
    winner_split = data[row_index-1][2].split('，')
    print("current_winner_index",current_winner_index)
    if current_winner_index>=3 or current_winner_index>=len(winner_split):
        session['current_row'] += 1
        session['current_winner_index'] = 0
        session['current_unit_index']=0
        session['last_unit'] = None
    current_data = get_current_data()


    return jsonify(current_data)

if __name__ == '__main__':
    app.run(debug=True)