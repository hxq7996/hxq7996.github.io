from flask_cors import CORS
import jwt
import time
import pymysql
from configparser import ConfigParser
from werkzeug.middleware.proxy_fix import ProxyFix
# 创建 ConfigParser 对象
config = ConfigParser()
# 读取配置文件
config.read('config.ini')
# 导入Flask类库
from flask import Flask,render_template,request,redirect,url_for,session,Response
# 创建应用实例
app = Flask(__name__)
app.jinja_env.variable_start_string = '<<'  # 解决与vue 标签的冲突
app.jinja_env.variable_end_string = '>>'

CORS(app, supports_credentials=True)

app.secret_key='any random string'

def token(username):
    # 生成一个字典，包含我们的具体信息
    d = {
        # 公共声明
        'exp':time.time()+3000, # (Expiration Time) 此token的过期时间的时间戳
        'iat':time.time(), # (Issued At) 指明此创建时间的时间戳
        'iss':'Issuer', # (Issuer) 指明此token的签发者
        
        # 私有声明
        'data':{
            'username':username,
            'timestamp':time.time()
        }
    }
    return jwt.encode(d,'gd',algorithm='HS256')

def connDB():               #连接数据库
    conn = pymysql.connect(host=config.get('database', 'HOST'), port=int(config.get('database', 'PORT')), user=config.get('database', 'USER'), password=config.get('database', 'PASSWORD'), charset='utf8',db=config.get('database', 'NAME'))
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return (conn,cursor)

def db_action_num(conn,cursor,sql, actionType=0):  # 进行相关业务操作
    try:
        cursor.execute(sql[0],sql[1])
        res = cursor.fetchall()
        conn.commit()
        if actionType == 1:  # 当操作类型为1时代表为查询业务，返回查询列表
            return res
        else:  # 当操作类型不为1时代表为新增、删除或更新业务，返回逻辑值
            return True
    except ValueError as e:
        print(e)

def connClose(conn,cur):          #关闭连接，释放资源
    cur.close()
    conn.close()

def db_action(sql, actionType=0):  # 进行相关业务操作
    try:
        conn = pymysql.connect(host=config.get('database', 'HOST'), port=int(config.get('database', 'PORT')), user=config.get('database', 'USER'), password=config.get('database', 'PASSWORD'), charset='utf8',db=config.get('database', 'NAME'))
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql[0],sql[1])
        res = cursor.fetchall()
        conn.commit()
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        if actionType == 1:  # 当操作类型为1时代表为查询业务，返回查询列表
            return res
        else:  # 当操作类型不为1时代表为新增、删除或更新业务，返回逻辑值
            return True
    except ValueError as e:
        print(e)

def login_flag(token):
    res = db_action(['select * from yonghu where token=%s',[token]],1)
    if type(res)==tuple:
        return "False"
    else:
        return res

# 视图函数（路由）
# {% python语句  %}
# {{ 变量 }}
@app.route("/")
def hello():
    #登录验证,页面初始化
    flag = login_flag(request.cookies.get('gdxt_token'))
    if flag =="False" :return render_template("lyear_pages_login_2.html",data='')
    else: return render_template("index.html",data='')
    

@app.route("/lyear_pages_doc")
def index():
    flag = login_flag(request.cookies.get('gdxt_token'))
    if flag =="False" :return render_template("lyear_pages_login_2.html",data='')
    else: 
        return render_template("lyear_pages_doc.html",data='')
    
@app.route("/lyear_pages_gd_doc")
def index_2():
    flag = login_flag(request.cookies.get('gdxt_token'))
    if flag =="False" :return render_template("lyear_pages_login_2.html",data='')
    else: 
        return render_template("lyear_pages_gd_doc.html",data='')

@app.route("/lyear_pages_user_doc")
def index_3():
    flag = login_flag(request.cookies.get('gdxt_token'))
    if flag =="False" :return render_template("lyear_pages_login_2.html",data='')
    else: 
        return render_template("lyear_pages_user_doc.html",data='')

@app.route("/lyear_pages_gdc_doc")
def index_4():
    flag = login_flag(request.cookies.get('gdxt_token'))
    if flag[0]['id']==1 :return render_template("lyear_pages_gdc_doc.html",data='')
    else: 
        return redirect("/")

@app.route("/lyear_pages_rabc")
def index_4_1():
    flag = login_flag(request.cookies.get('gdxt_token'))
    if flag[0]['id']==1 :return render_template("lyear_pages_gdc_doc.html",data='')
    else: 
        return redirect("/")

@app.route("/lyear_pages_add_doc")
def index_4_2():
    flag = login_flag(request.cookies.get('gdxt_token'))
    if flag[0]['id']==1 :return render_template("lyear_pages_gdc_doc.html",data='')
    else: 
        return redirect("/")
    
@app.route("/lyear_pages_ip_doc")
def index_5():
    flag = login_flag(request.cookies.get('gdxt_token'))
    if flag =="False" :return render_template("lyear_pages_login_2.html",data='')
    else: 
        return render_template("lyear_pages_ip_doc.html",data='')

@app.route('/menuV',methods=['POST'])
def menuV():
    flag = login_flag(request.cookies.get('gdxt_token'))
    if flag[0]['id']==1 :return {'menuV':True}
    else: 
        return {'menuV':False}

@app.route('/loginProcess',methods=['POST','GET'])
def loginProcesspage():
    json_param = request.get_json()
    username=json_param['username']
    password=json_param['password']
    sql= ["select * from yonghu where username=%s and password=%s",[username,password]]
    res= db_action(sql,1)

    if type(res)==tuple:
        return "false"
    else: 
        token_add=token(res[0]["username"])
        sql_set_token=["update yonghu set token=%s where id=%s",[token_add,res[0]["id"],]]
        db_action(sql_set_token)
        res=db_action(sql,1)
        return res

@app.route('/GD/<a>/<b>',methods=['GET'])
def gd_k(a,b):
    conn,cur=connDB()
    sql=["SELECT * FROM blink  inner join alink on blink.alink_id=alink.id where url=%s and gd_flag=1 ORDER BY gd_lunxun asc,blink.id desc limit 1 ",[a+"/"+b]]
    res=db_action_num(conn,cur,sql,1)
    retstr="The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
    if type(res)==tuple:
        connClose(conn,cur)
        return retstr
    else:
        sql=["SELECT * FROM alink where url=%s",[a+"/"+b]]
        hlink_res1=db_action_num(conn,cur,sql,1)
        if type(hlink_res1)==list:
            user_ip = request.remote_addr
            if hlink_res1[0]['ipadd']==1:
                sql=["SELECT * FROM hlink where h_url=%s and shenf=%s",[user_ip,hlink_res1[0]['shenf']]]
                hlink_res2=db_action_num(conn,cur,sql,1)
                if type(hlink_res2)==list:
                    sql=["update hlink set h_click=h_click+1 where id=%s",[hlink_res2[0]['id']]]
                    hlink_res3=db_action_num(conn,cur,sql)
                else:
                    sql=["insert into hlink (h_url,h_click,alink_url,shenf,isflag) values (%s,%s,%s,%s,%s)",[user_ip,1,hlink_res1[0]['id'],hlink_res1[0]['shenf'],0]]
                    hlink_res3=db_action_num(conn,cur,sql)
            if hlink_res1[0]['hmd']==1:
                        sql=["SELECT * FROM hlink where h_url=%s and shenf=%s and isflag=1",[user_ip,hlink_res1[0]['shenf']]]
                        hlink_res5=db_action_num(conn,cur,sql,1)
                        if type(hlink_res5)==list:
                            sql=["update hlink set h_click=h_click+1,j_click=j_click+1 where id=%s",[hlink_res5[0]['id']]]
                            hlink_res4=db_action_num(conn,cur,sql)
                            connClose(conn,cur)
                            return retstr
        sql=["update blink set gd_click=gd_click+1,gd_lunxun = 1 where id=%s",[res[0]['id']]]
        res1=db_action_num(conn,cur,sql)
        sql=["SELECT * FROM blink  inner join alink on blink.alink_id=alink.id where url=%s and gd_flag=1 and gd_lunxun=0 limit 1 ",[a+"/"+b]]
        res2=db_action_num(conn,cur,sql,1)
        if type(res2)==tuple:
            sql=["update blink  inner join alink on blink.alink_id=alink.id set gd_lunxun = 0 where url=%s and gd_flag=1",[a+"/"+b]]
            res3=db_action_num(conn,cur,sql)
        # start_clink
        sql=["SELECT * FROM clink where alink_from=%s and gd_flag=1 limit 1 ",[a+"/"+b]]
        res4=db_action_num(conn,cur,sql,1)
        if type(res4)==list:
            if res4[0]['now']>0:
                sql=["update clink set now = now-1 where id=%s",[str(res4[0]['id'])]]
                res5=db_action_num(conn,cur,sql,1)
            else:
                sql=["update clink set now = pinlv,gd_click=gd_click+1 where id=%s",[str(res4[0]['id'])]]
                res5=db_action_num(conn,cur,sql,1)
                connClose(conn,cur)
                return redirect("/GD/"+res4[0]['alink_to'])
        # end_clink
        if res[0]['gd_num'].find("http")>-1:
            connClose(conn,cur)
            return redirect(res[0]['gd_num'])
        else:
            connClose(conn,cur)
            return redirect(res[0]['to_url'].replace('***',res[0]['gd_num']))

@app.route('/alink',methods=['POST','GET'])
def alink():
    json_param = request.get_json()
    flag = login_flag(request.cookies.get('gdxt_token'))
    if "act" not in json_param:
        pnum=int(json_param["pnum"])
        psize=int(json_param["psize"])
        p_offset=(pnum-1)*psize
        pname=json_param["pname"]
        sql=["SELECT id FROM yonghu WHERE shenf1="+str(flag[0]['id'])+" or id="+str(flag[0]['id']),[]]
        if flag[0]['id']==1:
            sql=["SELECT id FROM yonghu",[]]
        res1= db_action(sql,1)
        idlist=''
        for item in res1:
            if idlist=='':idlist=str(item['id'])
            else:idlist+=','+str(item['id'])
        sql=["SELECT count(alink.id) as total FROM alink join yonghu on alink.shenf=yonghu.id WHERE alink.shenf in ("+idlist+") and (url LIKE %s or to_url LIKE %s)",[f"%{pname}%",f"%{pname}%"]]
        res1= db_action(sql,1)
        #print(res1,type(res1)) 打印
        sql=["SELECT * FROM alink join yonghu on alink.shenf=yonghu.id WHERE alink.shenf in ("+idlist+") and (url LIKE %s or to_url LIKE %s)  ORDER BY alink.id DESC LIMIT %s,%s",[f"%{pname}%",f"%{pname}%",p_offset,psize]]
        res= db_action(sql,1)
        if type(res)==tuple:
            return {}
        else:
            res1={'total':res1[0]['total']}
            res1['list']=res
            return res1
    else:
        if json_param["act"]=="add":
            sql=["SELECT * FROM alink WHERE url=%s",[json_param['row']['url1']+"/"+json_param['row']['url2']]]
            res= db_action(sql,1)
            if type(res)==tuple:
                sql=["insert into alink (url,to_url,shenf,ipadd,hmd) values (%s,%s,"+str(flag[0]['id'])+",%s,%s)",[json_param['row']['url1']+"/"+json_param['row']['url2'],json_param['row']['to_url'],json_param['row']['ipadd'],json_param['row']['hmd']]]
                res= db_action(sql)
                return "1"
            else:
                return "0"
        elif json_param["act"]=="edit":
            sql=["update alink set url=%s,to_url=%s,ipadd=%s,hmd=%s where id=%s",[json_param['row']['url1']+"/"+json_param['row']['url2'],json_param['row']['to_url'],json_param['row']['ipadd'],json_param['row']['hmd'],json_param['row']['id']]]
            res= db_action(sql)
            return "1"
        elif json_param["act"]=="del":
            sql=["delete from blink where alink_id in ("+str(json_param['row']['id'])+")",[]]
            res= db_action(sql)
            sql=["delete from hlink where alink_url in ("+str(json_param['row']['id'])+")",[]]
            res= db_action(sql)
            sql=["delete from alink where id in ("+str(json_param['row']['id'])+")",[]]
            res= db_action(sql)
            return "1"
        else:
            return {}
        
@app.route('/blink',methods=['POST','GET'])
def blink():
    json_param = request.get_json()
    flag = login_flag(request.cookies.get('gdxt_token'))
    if "act" not in json_param:
        pnum=int(json_param["pnum"])
        psize=int(json_param["psize"])
        p_offset=(pnum-1)*psize
        pname=json_param["pname"]
        sql=["SELECT id FROM yonghu WHERE shenf1="+str(flag[0]['id'])+" or id="+str(flag[0]['id']),[]]
        if flag[0]['id']==1:
            sql=["SELECT id FROM yonghu",[]]
        res1= db_action(sql,1)
        idlist=''
        for item in res1:
            if idlist=='':idlist=str(item['id'])
            else:idlist+=','+str(item['id'])
        sql=["SELECT count(blink.id) as total FROM blink  inner join alink on blink.alink_id=alink.id join yonghu on alink.shenf=yonghu.id  WHERE blink.shenf in ("+idlist+") and (name LIKE %s or gd_num LIKE %s or url LIKE %s)  ",[f"%{pname}%",f"%{pname}%",f"%{pname}%"]]
        res1= db_action(sql,1)
        #print(res1,type(res1)) 打印
        sql=["SELECT * FROM blink  inner join alink on blink.alink_id=alink.id join yonghu on alink.shenf=yonghu.id  WHERE blink.shenf in ("+idlist+") and (name LIKE %s or gd_num LIKE %s or url LIKE %s)  ORDER BY blink.id desc LIMIT %s,%s",[f"%{pname}%",f"%{pname}%",f"%{pname}%",p_offset,psize]]
        res= db_action(sql,1)
        if type(res)==tuple:
            return {}
        else:
            res1={'total':res1[0]['total']}
            res1['list']=res
            # print(res1,type(res1))
            # res=res1[0].update({'list':res})
            #print(res1,type(res1))
            return res1
    else:
        if json_param["act"]=="add":
            # {'row': {'url1': '', 'url2': '', 'to_url': '1'}, 'act': 'add'}
            # delete from user_info where userName = %s
            gd_num=json_param['row']['gd_num'].split("\n")
            gd_num_sql=''
            sql=["SELECT * FROM alink where id="+str(json_param['row']['alink_id']),[]]
            res= db_action(sql,1)
            for item in gd_num:
                if len(item)>0:
                    if gd_num_sql=='':
                        gd_num_sql='('+ str(res[0]['shenf'])+',1,'+str(json_param['row']['alink_id'])+',\''+str(json_param['row']['name'])+'\',\''+item+'\')'
                    else:
                        gd_num_sql+=',('+ str(res[0]['shenf'])+',1,'+str(json_param['row']['alink_id'])+',\''+str(json_param['row']['name'])+'\',\''+item+'\')'
            print(gd_num_sql)       
            sql=["insert into blink (shenf,gd_flag,alink_id,name,gd_num) values "+gd_num_sql,[]]
            res= db_action(sql)
            print(flag[0]['id'])
            return "1"
        elif json_param["act"]=="edit":
            sql=["update blink set alink_id=%s,name=%s,gd_num=%s where id=%s",[json_param['row']['alink_id'],json_param['row']['name'],json_param['row']['gd_num'],json_param['row']['id']]]
            res= db_action(sql)
            return "1"
        elif json_param["act"]=="del":
            # 参数化in???
            sql=["delete from blink where id in ("+str(json_param['row']['id'])+")",[]]
            res= db_action(sql)
            return "1"
        elif json_param["act"]=="flag":
            # 参数化in???
            # UPDATE blink SET gd_flag = IF(gd_flag=0,1,0) where id in (55,56)
            sql=["UPDATE blink SET gd_flag = IF(gd_flag=0,1,0) where id in ("+ str(json_param['row']['id']) +")",[]]
            res= db_action(sql)
            return "1"
        else:
            return {}

@app.route('/clink',methods=['POST','GET'])
def clink():
    json_param = request.get_json()
    flag = login_flag(request.cookies.get('gdxt_token'))
    if "act" not in json_param:
        pnum=int(json_param["pnum"])
        psize=int(json_param["psize"])
        p_offset=(pnum-1)*psize
        pname=json_param["pname"]
        sql=["SELECT id FROM yonghu WHERE shenf1="+str(flag[0]['id'])+" or id="+str(flag[0]['id']),[]]
        if flag[0]['id']==1:
            sql=["SELECT id FROM yonghu",[]]
        res1= db_action(sql,1)
        idlist=''
        for item in res1:
            if idlist=='':idlist=str(item['id'])
            else:idlist+=','+str(item['id'])
        sql=["SELECT count(clink.id) as total FROM clink   WHERE  (alink_from LIKE %s or alink_to LIKE %s)  ",[f"%{pname}%",f"%{pname}%"]]
        res1= db_action(sql,1)
        #print(res1,type(res1)) 打印
        sql=["SELECT * FROM clink   WHERE (alink_from LIKE %s or alink_to LIKE %s)  ORDER BY clink.id desc LIMIT %s,%s",[f"%{pname}%",f"%{pname}%",p_offset,psize]]
        res= db_action(sql,1)
        if type(res)==tuple:
            return {}
        else:
            res1={'total':res1[0]['total']}
            res1['list']=res
            # print(res1,type(res1))
            # res=res1[0].update({'list':res})
            #print(res1,type(res1))
            return res1
    else:
        if json_param["act"]=="add":
            # {'row': {'url1': '', 'url2': '', 'to_url': '1'}, 'act': 'add'}
            # delete from user_info where userName = %s
            
            sql=["insert into clink (alink_from,alink_to,pinlv,now,gd_click,gd_flag) values (%s,%s,%s,%s,0,1)",[json_param['row']['alink_from'],json_param['row']['alink_to'],json_param['row']['pinlv'],json_param['row']['pinlv']]]
            res= db_action(sql)
            return "1"
        elif json_param["act"]=="edit":
            sql=["update clink set alink_from=%s,alink_to=%s,pinlv=%s where id=%s",[json_param['row']['alink_from'],json_param['row']['alink_to'],json_param['row']['pinlv'],json_param['row']['id']]]
            res= db_action(sql)
            return "1"
        elif json_param["act"]=="del":
            # 参数化in???
            sql=["delete from clink where id in ("+str(json_param['row']['id'])+")",[]]
            res= db_action(sql)
            return "1"
        elif json_param["act"]=="flag":
            # 参数化in???
            # UPDATE clink SET gd_flag = IF(gd_flag=0,1,0) where id in (55,56)
            sql=["UPDATE clink SET gd_flag = IF(gd_flag=0,1,0) where id in ("+ str(json_param['row']['id']) +")",[]]
            res= db_action(sql)
            return "1"
        else:
            return {}

@app.route('/hlink',methods=['POST','GET'])
def hlink():
    json_param = request.get_json()
    flag = login_flag(request.cookies.get('gdxt_token'))
    if "act" not in json_param:
        pnum=int(json_param["pnum"])
        psize=int(json_param["psize"])
        p_offset=(pnum-1)*psize
        pname=json_param["pname"]
        sql=["SELECT id FROM yonghu WHERE shenf1="+str(flag[0]['id'])+" or id="+str(flag[0]['id']),[]]
        if flag[0]['id']==1:
            sql=["SELECT id FROM yonghu",[]]
        res1= db_action(sql,1)
        idlist=''
        for item in res1:
            if idlist=='':idlist=str(item['id'])
            else:idlist+=','+str(item['id'])
        sql=["SELECT count(hlink.id) as total FROM hlink inner join alink on hlink.alink_url=alink.id join yonghu on hlink.shenf=yonghu.id WHERE hlink.shenf in ("+idlist+") and (alink_url LIKE %s or h_url LIKE %s)",[f"%{pname}%",f"%{pname}%"]]
        res1= db_action(sql,1)
        #print(res1,type(res1)) 打印
        sql=["SELECT * FROM hlink inner join alink on hlink.alink_url=alink.id join yonghu on hlink.shenf=yonghu.id WHERE hlink.shenf in ("+idlist+") and (alink_url LIKE %s or h_url LIKE %s)  ORDER BY hlink.id DESC LIMIT %s,%s",[f"%{pname}%",f"%{pname}%",p_offset,psize]]
        res= db_action(sql,1)
        if type(res)==tuple:
            return {}
        else:
            res1={'total':res1[0]['total']}
            res1['list']=res
            return res1
    else:
        if json_param["act"]=="del":
            # 参数化in???
            sql=["delete from hlink where id in ("+str(json_param['row']['id'])+")",[]]
            res= db_action(sql)
            return "1"
        elif json_param["act"]=="delall":
            sql=["SELECT id FROM yonghu WHERE shenf1="+str(flag[0]['id'])+" or id="+str(flag[0]['id']),[]]
            if flag[0]['id']==1:
                sql=["SELECT id FROM yonghu",[]]
            res1= db_action(sql,1)
            idlist=''
            for item in res1:
                if idlist=='':idlist=str(item['id'])
                else:idlist+=','+str(item['id'])
            sql=["delete from hlink where shenf in ("+idlist+") and isflag=0",[]]
            res= db_action(sql)
            return "1"
        elif json_param["act"]=="flag":
            # 参数化in???
            # UPDATE clink SET gd_flag = IF(gd_flag=0,1,0) where id in (55,56)
            sql=["UPDATE hlink SET isflag = IF(isflag=0,1,0) where id in ("+ str(json_param['row']['id']) +")",[]]
            res= db_action(sql)
            return "1"
        else:
            return {}

# @app.errorhandler(404)  # 传入错误码作为参数状态
# def error_date(error):  # 接受错误作为参数
#     return '1'
    #return render_template("404.html"), 404  # 返回对应的http状态码，和返回404错误的h

@app.route('/yonghu',methods=['POST','GET'])
def yonghu():
    json_param = request.get_json()
    flag = login_flag(request.cookies.get('gdxt_token'))
    if "act" not in json_param:
        pnum=int(json_param["pnum"])
        psize=int(json_param["psize"])
        p_offset=(pnum-1)*psize
        pname=json_param["pname"]
        sql=["SELECT count(id) as total FROM yonghu WHERE shenf1="+str(flag[0]['id'])+" or id="+str(flag[0]['id']),[]]
        if flag[0]['id']==1:
            sql=["SELECT count(id) as total FROM yonghu  where LENGTH(shenf)>0 or id=1",[]]
        res1= db_action(sql,1)
        #print(res1,type(res1)) 打印
        sql=["SELECT * FROM yonghu WHERE shenf1="+str(flag[0]['id'])+" or id="+str(flag[0]['id'])+"   LIMIT %s,%s",[p_offset,psize]]
        if flag[0]['id']==1:
            sql=["SELECT * FROM yonghu where LENGTH(shenf)>0 or id=1 LIMIT %s,%s",[p_offset,psize]]
        res= db_action(sql,1)
        if type(res)==tuple:
            return {}
        else:
            res1={'total':res1[0]['total']}
            res1['list']=res
            if len(flag[0]['shenf'])==0 and  len(flag[0]['shenf1'])>0:
                res1['shenflag']=False
            else:
                res1['shenflag']=True
            return res1
    else:
        if json_param["act"]=="add":
            # {'row': {'url1': '', 'url2': '', 'to_url': '1'}, 'act': 'add'}
            # delete from user_info where userName = %s
            sql=["SELECT * FROM yonghu WHERE username=%s",[json_param['row']['username']]]
            res= db_action(sql,1)
            if type(res)==tuple:
                sql=["insert into yonghu (username,password,shenf1) values (%s,%s,%s)",[json_param['row']['username'],json_param['row']['password'],str(flag[0]['id'])]]
                if flag[0]['id']==1:
                    sql=["insert into yonghu (username,password,shenf) values (%s,%s,%s)",[json_param['row']['username'],json_param['row']['password'],'1']]
                res= db_action(sql)
                return "1"
            else:
                return "0"
        elif json_param["act"]=="edit":
            sql=["SELECT * FROM yonghu WHERE username=%s",[json_param['row']['username']]]
            res= db_action(sql,1)
            # if type(res)==tuple:
            #     sql=["update yonghu set username=%s,password=%s where id=%s",[json_param['row']['username'],json_param['row']['password'],json_param['row']['id']]]
            #     res= db_action(sql)
            #     return "1"
            # else:
            #     return "0"
            sql=["update yonghu set username=%s,password=%s where id=%s",[json_param['row']['username'],json_param['row']['password'],json_param['row']['id']]]
            res= db_action(sql)
            return "1"
        elif json_param["act"]=="del":
            # 参数化in???
            sql=["delete from alink where shenf in ("+str(json_param['row']['id'])+")",[]]
            res= db_action(sql)
            sql=["delete from blink where shenf in ("+str(json_param['row']['id'])+")",[]]
            res= db_action(sql)
            sql=["delete from hlink where shenf in ("+str(json_param['row']['id'])+")",[]]
            res= db_action(sql)
            sql=["delete from yonghu where id in ("+str(json_param['row']['id'])+")",[]]
            res= db_action(sql)
            return "1"
        else:
            return {}

@app.route('/test')
def test():
    return render_template("test.html",data='res')

# 启动服务
# 打开 debug 模式,默认是没有开启的。直接保存然后就有效果,浏览器上就可以看到报错信息
# 在同一个网络下的其他设备可以访问的话，需要修改为0.0.0.0
if __name__ == '__main__':
   app.run(port=80,host="0.0.0.0",debug=True)

