from flask import render_template
from blueprints.influxdb import *

siemens_ = Blueprint("siemens_",__name__)

'''
西门子库文件 python-snap7
'''
# import s7read
import snap7.client as client
from snap7.util import *
from snap7.snap7types import *
from blueprints.login import is_login

###################### 西门子 #######################################

@siemens_.route("/siemens",methods=("GET","POST"))
@is_login
def siemens():
    ## 反馈系统运行状态
    def s7connect(ip, rack, slot):
        try:
            plc = client.Client()
            # print(ip,rack,slot)
            plc.connect(ip, rack, slot)
        except Exception as e:
            flash("连接失败，请确认IP或网络连通性", "connect0")
        else:
            state = plc.get_cpu_state()
            flash(ip + " 连接成功", "connect1")
            return plc

    if request.method =="POST":
        # flash("run", "run")
        # print("222222222")
        forminfo = request.form.to_dict()
        # print(forminfo)

        # 该页面的表单信息，只要submit都传到这里，其中包括plc的连接信息 ip[str] rack[int] slot[int]
        # 还包括变量地址信息以及influxdb配置信息，通过字典长度区分各个表单
        global plc
        if (forminfo)=={}: #上传变量表
            try:
                f = request.files.get('file') ## 获取文件
                print(f.filename)
                f.save('D:/' + secure_filename(f.filename))  ## C盘写入权限受限Permission denied
            except Exception as e:
                print(e)
                flash(e,"uploadstatus")
            else:
                ## 保存测试
                flash("变量表上传成功", "uploadstatus")
                # try:
                #     f.save('D:/' + secure_filename(f.filename))  ## C盘写入权限受限Permission denied
                # except Exception as e:
                #     print(e)
                #     flash(e, "uploadstatus")
                # else:
                #     flash("变量表上传成功","uploadstatus")

        if len(forminfo)==3: #PLC 连接信息
            print(forminfo)
            plc=s7connect(str(forminfo["ipaddress"]),int(forminfo["rack"]),int(forminfo["slot"])) #数据类型转换
            # ip=forminfo["ipaddress"]
        if len(forminfo)==2: #变量地址
            print(forminfo)
            data=s7read(plc,forminfo["iqm"],forminfo["address"])
            print(data)
                # return data

        elif len(forminfo)==4: # influxdb连接信息
            print(forminfo)
            influxdbip = forminfo["influxdb"]
            token = forminfo["token"]
            measurement = forminfo["measurement"]
            cycle=forminfo["cycle"]
            influxDB(influxdbip,token,measurement,cycle)
        # flash(forminfo,"connect1")
        return redirect("#")
        # return render_template("siemens.html")
    return render_template("siemens.html")
    # return render_template("rockwell.html")

@siemens_.route("/siemensdisconnect",methods=("POST","GET"))
@is_login
def s7disconnect():
    try:
        print("disconnect")
        # plc = client.Client()
        plc.disconnect()
    except Exception:
        flash("断开失败","connect0") ##connect0 失败提醒
    else:
        flash("已断开连接","connect1") ## connect1 操作成功提示
    return redirect("/siemens#connection")

@siemens_.route("/s7read",methods=("POST","GET"))
@is_login
def s7read(plc,iqm,address):

    ss=""  # 标识I/Q/M
    t=areas[iqm]
    # print(address)
    if address=='':
        address2=0.0
    else:
        address2=(float(address))
    if t ==129:
        ss = "I "
    if t == 130:
        ss = "Q "
    if t == 131:
        ss = "M "

    b = (int(address2))
    c = (int((address2-b)*10))

    print(t,b,c)
    try:
        variable = ss + address
        print(variable)
        timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        result=plc.read_area(t,0,b,8)  ## 变量类型，0，地址起始，固定8位
        data = get_bool(result, 0, c)  ## 地址偏移值
        ttt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    except Exception as e:
        print(e)
    else:
        # flash(data, "value")
        # flash(timenow, "time")
        # flash(variable,"variable")
        siemensdata = dict(zip(variable, data))
        print(siemensdata)
    return render_template("siemens.html", siemensdata=siemensdata, ttt=ttt)

