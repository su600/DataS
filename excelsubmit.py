import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request

# import flask_excel as excel

app = Flask(__name__)
# excel.init_excel(app)


@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # aa=jsonify({"result": request.get_array(field_name='file')})
        file = request.files.get('file2')
        print(file.filename)
        data = pd.DataFrame(pd.read_excel(file))
        # 第一列 无表头 输出为DataFrame格式 带索引
        data2 = pd.read_excel(file, usecols=[0], header=None)
        data2=data2.dropna()
        data2 = data2.to_numpy().tolist()  # 转数组 转列表
        aa = sum(data2, [])  # 嵌套列表平铺
        # aa=data2.to_csv('111.csv',index=None) #写入文件 去除索引
        print(aa)
        # print(type(aa))
        # aa=str(aa)
        # return aa
        return render_template("ee.html", su=aa)
    return render_template("ee.html")


@app.route("/base", methods=['GET'])
def export_records():
    return render_template("exc.html")


if __name__ == "__main__":
    app.run()
