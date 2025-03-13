import sys
import io
import requests
from bs4 import BeautifulSoup
import time
import pymysql
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. 修复其他数据库操作函数中的 open() 调用
def connect_db():
    """
    建立数据库连接
    :return: 数据库连接
    """
    db = pymysql.connect(host="localhost", port=3306, user="root", password="toor",
                         database="test", charset="utf8")
    return db

def insert(sql, values):
    """
    向数据库插入单条数据
    """
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(sql, values)
        db.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        db.close()
        return affected_rows
    except Exception as e:
        print(f"数据库插入错误：{str(e)}")
        return 0

def query1(sql):
    """
    不带参数查询
    """
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(sql)  # 移除 values 参数
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def query(sql, *keys):
    db = connect_db()  # 修改这里
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    cursor.execute(sql, keys)  # 执行查询sql 语句
    result = cursor.fetchall()  # 记录查询结果
    cursor.close()  # 关闭游标
    db.close()  # 关闭数据库连接
    return result  # 返回查询结果

def insert_p(sql, values):
    db = connect_db()  # 修改这里
    cursor = db.cursor()  # 使用cursor（）方法获取游标
    cursor.executemany(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return cursor.rowcount

def delete(sql, values):
    db = connect_db()  # 修改这里
    cursor = db.cursor()  # 使用cursor()方法获取游标
    cursor.execute(sql, values)
    db.commit()  # 执行修改
    cursor.close()
    db.close()
    return cursor.rowcount

def update(sql, values):
    db = connect_db()  # 修改这里
    cursor = db.cursor()  # 使用cursor()方法获取游标
    cursor.execute(sql, values)  # 执行sql数据修改语句
    db.commit()  # 提交数据
    cursor.close()  # 关闭游标
    db.close()  # 关闭数据库连接
    return cursor.rowcount



def read_url(url,headers):
    res = requests.get(url,headers=headers)
    time.sleep(0.2)  # 增加延时到2秒
    html = res.content.decode('utf-8')
    return html
def soup_html(html_str):
    # pip install lxml -i https://pypi.tuna.tsinghua.edu.cn/simple
    # 解析HTML文本数据 ，lxml库更实用与HTML
    soup = BeautifulSoup(html_str,"lxml")
    #逐步定位到目标标签
    div_lsit = soup.select("div.left>div.sons>div.cont")
    data_list = []
    data_url = []
    for div in div_lsit:
        # < div
        #
        # class ="cont" style=" margin-top:12px;border-bottom:1px dashed #DAD9D1; padding-bottom:7px;" >
        #
        # < a
        # href = "/mingju/juv_d898ba69839d.aspx"
        # style = " float:left;"
        # target = "_blank" > 东北看惊诸葛表，西南更草相如檄。 < / a >
        # < span
        # style = " color:#65645F; float:left; margin-left:5px; margin-right:10px;" >—— < / span > < a
        # href = "/shiwenv_6684e95c8744.aspx"
        # style = " float:left;"
        # target = "_blank" > 辛弃疾《满江红·送李正之提刑入蜀》 < / a >
        # < / div >   东北看惊诸葛表，西南更草相如檄。——辛弃疾《满江红·送李正之提刑入蜀》
        #数据清洗与标准化
        wen = div.get_text().replace("\n","")
        url = div.select("a")[0].get('href')
        url = "https://so.gushiwen.cn"+url
        data_list.append(wen)
        data_url.append(url)
    # print(data_list)
    # print(data_url)

    return data_list,data_url

def soup_zi_html(html_str):
    # pip install lxml
    soup = BeautifulSoup(html_str,"lxml")
    zi_wen = soup.select("div.contson")[0].get_text().replace("\n","")
    return zi_wen
def txt_def(info_list):
    import json
    with open(r'D:\03_教育\00_本科_海南师范大学\05_大三下_2025.3-2025.6\课程\网络信息内容安全\AI--\数据爬取\爬虫\sentence.txt', 'a', encoding='utf-8') as df:
        if isinstance(info_list, dict):
            for key, value in info_list.items():
                df.write(json.dumps({key: value}, ensure_ascii=False) + '\n\n')
        else:
            for one in info_list:
                df.write(json.dumps(one, ensure_ascii=False) + '\n\n')

if __name__ == '__main__':
    headers = {
        "Cookie": "Hm_lvt_9007fab6814e892d3020a64454da5a55=1741255364; Hm_lpvt_9007fab6814e892d3020a64454da5a55=1741255364; HMACCOUNT=FB757863880B2A52; login=flase",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
    }
    try:
        # 测试数据库连接
        db = connect_db()
        db.close()
        print("数据库连接测试成功")
        
        print("请输入要爬取的页数：")
        n = int(input())
        for i in range(1, n+1):
            try:
                html_str = read_url(f'https://so.gushiwen.cn/mingjus/default.aspx?page={i}&tstr=&astr=&cstr=&xstr=', headers=headers)
                print(f"开始读取第{i}主页面...")
                data_list, data_url = soup_html(html_str)
                print("主页面解析中...")
                
                data_zi_list = []
                for zi_url in data_url:
                    try:
                        print("开始读取子页面...")
                        html_zi_str = read_url(zi_url, headers=headers)
                        zi_wen = soup_zi_html(html_zi_str)
                        print("子页面解析中...")
                        data_zi_list.append(zi_wen)
                    except Exception as e:
                        print(f"子页面处理出错：{str(e)}")
                        continue
                
                print("数据入库中...")
                for j in range(len(data_list)):
                    try:
                        # 数据库插入
                        sql = "insert into train_ (content,summary) values (%s,%s)"
                        val = (data_list[j], data_zi_list[j])
                        insert(sql, val)
                        print(f"第{j + 1}条数据添加成功")
                        
                        # 写入文本文件
                        txt_def({data_list[j]: data_zi_list[j]})
                        print(f"第{j + 1}条数据写入文件成功")
                    except Exception as e:
                        print(f"数据处理失败：{str(e)}")
                        continue
                
            except Exception as e:
                print(f"处理第{i}页时出错：{str(e)}")
                continue
                
    except Exception as e:
        print(f"程序执行出错：{str(e)}")
