import pandas as pd
import numpy as np
import os
from autogluon.tabular import TabularPredictor
import urllib
import urllib.request
import requests
import re
import random
import time
import predfit

user_agent = ["Mozilla/5.0 (Windows NT 10.0; WOW64)", 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
              'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
              'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
              'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
              'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
              'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

def spider_done( id ):
    root = os.getcwd()
    print("done")
    path_done = root + '\\' + 'Bdone' + '.xlsx'
    if (os.path.isfile(path_done)):
        done_sp = pd.read_excel(path_done)
        done_sp_list = done_sp[0].tolist()
    else:
        done_sp_list = ["0"]
    # done_sp = pd.read_excel(path_done)
    # done_sp_list = done_sp[0].tolist()
    done_sp_list.append(id)
    new_done_sp_df = pd.DataFrame(done_sp_list)
    new_done_sp_df.to_excel(path_done, header=True, index=None)  # , startrow=len(old))
    return

def spider(  ):
    stock_total = [] #stock_total：所有页面的数据
    url = 'http://guess2.win007.com/basket/'
    request=urllib.request.Request(url=url,headers={"User-Agent":random.choice(user_agent)})#随机从user_agent列表中抽取一个元素
    response=urllib.request.urlopen(request)
    content=response.read().decode('UTF-8')       #读取网页内容
    time.sleep(random.randrange(1, 2))
    #print(content)
    pattern = re.compile('(?<=zt_)(\d*)')
    #print(body)
    #data_page = re.findall(pattern, str(content))  # 正则匹配
    #pattern = re.compile('(?<=home_)([0-9]*)')
    game_id = re.findall(pattern, str(content))  # 正则匹配
    print(game_id)
    return game_id

def gamespider(gameid):
    root = os.getcwd() # 获取当前路径
    stock_total=[]   #stock_total：所有页面的数据
    #gameid = 1910700
    #for page in range(1,2):
    url = 'http://nba.win007.com/odds/AsianOdds_n.aspx?id=' + str(gameid)
    request = urllib.request.Request(url=url,headers={"User-Agent": random.choice(user_agent)})  # 随机从user_agent列表中抽取一个元素
    response = urllib.request.urlopen(request)
    content = response.read().decode('UTF-8')  # 读取网页内容
    time.sleep(random.randrange(1, 2))
    #print(content)

    pattern = re.compile('(?<= alt=")([\s\S].*?)\" t')
    team_name = re.findall(pattern, str(content))
    print(team_name)

    content1 = str(content).replace(" ", "").replace("\r", "").replace("\n", "")
    #print(content1)
    pattern = re.compile('(?<=id="headVs">)[\u4E00-\u9FA5A-Za-z+\/(\-|\+)?\d+(\.\d+)?]+(?=<)')
    VS = re.findall(pattern, str(content1))
    if(len(VS) == 0):
        pattern = re.compile('(?<=="rowredb">)[\u4E00-\u9FA5A-Za-z+\/(\-|\+)?\d+(\.\d+)?]+(?=<)')
        VS = re.findall(pattern, str(content1))
        if(len(VS) == 0):
            pattern = re.compile('(?<=class=\'vs\'>)[\u4E00-\u9FA5A-Za-z+\/(\-|\+)?\d+(\.\d+)?]+(?=<)')
            VS = re.findall(pattern, str(content1))
    print(VS)

    pattern = re.compile('(?<=class="LName">)\S+(?=<)')
    LName = re.findall(pattern, str(content))
    print(LName)
    Lname = str(LName[0])
    print(Lname)
    if((Lname != 'NBA') & (Lname != 'CBA')):
        spider_done(gameid)
        return

    pattern = re.compile('(?<=\t)[0-9]*|\d{4}-\d{2}-\d{2} \d{2}:\d{2}(?=\&)')
    playtime = re.findall(pattern, str(content))
    print(playtime)

    for i in playtime:
        if i == '':
            playtime.remove(i)
    time_now = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    time_diff = time.mktime(time.strptime(str(playtime[0]), "%Y-%m-%d %H:%M")) - time.mktime(
        time.strptime(str(time_now), "%Y-%m-%d %H:%M"))
    # print(playtime[0])
    # print(time_now)
    # print(time_diff)

    if ((time_diff < 2400)):#(time_diff >- 2400)&
        print('1 hours in')
    else:
        print('1 hours out')
        return

    pattern = re.compile('(?<=<div class="score">)(\d*)')
    score = re.findall(pattern, str(content))
    if(len(score) == 0):
        score = ['0', '0']
    print(score)

    pattern = re.compile('(?<=id="odds")[\s\S]+<div id="MiddleAd"')
    tbody = re.findall(pattern, str(content))
    #print(tbody)

    tbody = str(tbody).replace(" ", "").replace("\\r", "").replace("\\n", "")
    #tbody = str(tbody).replace("\\r", "")
    #tbody = str(tbody).replace("\\n", "")
    #print(tbody)
    pattern = re.compile('(?<=>)[\u4E00-\u9FA5A-Za-z+\/(\-|\+)?\d+(\.\d+)?]+(?=<)|(?<=home_)[0-9]*|\d{4}-\d{2}-\d{2} \d{2}:\d{2}')
    state = re.findall(pattern, str(tbody))
    #print(state)
    a = ['初', '多盘口', '即', '终', '历史资料', '详', '主', '客', '同', '公司', '主队', '盘口', '客队']
    company = ['澳门', '易胜博', 'Crown', '365', '韦德', '威廉', 'Interwetten', '立博', '12B', '利记']
    black_list = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
    for i in a:
        while i in state:
            state.remove(i)
    #print(state)
    for i in range(len(state)-1,-1,-1):
        if state[i] in company:
            # print('ture')
            if (i == (len(state) - 1)):
                for j in black_list:
                    state.insert(i + 1, j)
            elif (state[i + 1] in company):
                for j in black_list:
                    state.insert(i+1, j)

    #print(state)
    result = []  # result：最终数据
    Hang = (int)(len(state)/10)
    # 转换成多维列表
    for y in range(0, Hang):
        for x in range(0, 10):
            if x == 0:
                result.append([])
            result[y].append(state[x + y * 10])
    #print(result)
    result_df = pd.DataFrame(result)
    result_df = result_df.drop([4, 5, 6], axis=1)
    result_df = result_df[result_df[0] != '盘口2']
    result_df = result_df[result_df[0] != '盘口3']
    result_df = result_df[result_df[0] != '盘口4']
    result_df = result_df[result_df[0] != '盘口5']
    #print(result_df)
    result1 = np.array(result_df)
    #print(result1)
    result1 = result1.flatten()
    result1 = result1.tolist()
    # Hang = (int)(len(result1) / 7)
    # for i in range(len(result1)+Hang*2):
    #     if result1[i] in company:
    #         if (float(score[0]) - float(score[1]) > float(result1[i + 2])):
    #             result1.insert(i + 1, '1')
    #         elif (float(score[0]) - float(score[1]) == float(result1[i + 2])):
    #             result1.insert(i + 1, '0')
    #         elif (float(score[0]) - float(score[1]) < float(result1[i + 2])):
    #             result1.insert(i + 1, '-1')
    #
    #         if (float(score[0]) - float(score[1]) > float(result1[i + 6])):
    #             result1.insert(i + 2, '1')
    #         elif (float(score[0]) - float(score[1]) == float(result1[i + 6])):
    #             result1.insert(i + 2, '0')
    #         elif (float(score[0]) - float(score[1]) < float(result1[i + 6])):
    #             result1.insert(i + 2, '-1')
    # print(result1)

    url = 'https://nba.win007.com/odds/OverDown_n.aspx?id=' + str(gameid) + '&l=0'
    request = urllib.request.Request(url=url,headers={"User-Agent": random.choice(user_agent)})  # 随机从user_agent列表中抽取一个元素
    response = urllib.request.urlopen(request)
    content = response.read().decode('UTF-8')  # 读取网页内容
    time.sleep(random.randrange(1, 2))

    #pattern = re.compile('(?<= alt=")([\s\S].*?)\" t')
    #team_name = re.findall(pattern, str(content))
    #print(team_name)

    pattern = re.compile('(?<=id="odds")[\s\S]+<div id="MiddleAd"')
    tbody = re.findall(pattern, str(content))
    #print(tbody)

    tbody = str(tbody).replace(" ", "")
    tbody = str(tbody).replace("\\r", "")
    tbody = str(tbody).replace("\\n", "")
    #print(tbody)
    pattern = re.compile(
        '(?<=>)[\u4E00-\u9FA5A-Za-z+\/(\-|\+)?\d+(\.\d+)?]+(?=<)|(?<=home_)[0-9]*|\d{4}-\d{2}-\d{2} \d{2}:\d{2}')
    state = re.findall(pattern, str(tbody))
    #print(state)
    a = ['初', '多盘口', '即', '终', '变化时间', '详', '主', '客', '同', '公司', '大分', '盘口', '小分']
    for i in a:
        while i in state:
            state.remove(i)
    #print(state)
    for i in range(len(state)-1,-1,-1):
        if state[i] in company:
            # print('ture')
            if (i == (len(state) - 1)):
                for j in black_list:
                    state.insert(i + 1, j)
            elif (state[i + 1] in company):
                for j in black_list:
                    state.insert(i+1, j)

    result = []  # result：最终数据
    Hang = (int)(len(state)/10)
    # 转换成多维列表
    for y in range(0, Hang):
        for x in range(0, 10):
            if x == 0:
                result.append([])
            result[y].append(state[x + y * 10])
    #print(result)
    result_df = pd.DataFrame(result)
    result_df = result_df.drop([4, 5, 6], axis=1)
    result_df = result_df[result_df[0] != '盘口2']
    result_df = result_df[result_df[0] != '盘口3']
    result_df = result_df[result_df[0] != '盘口4']
    result_df = result_df[result_df[0] != '盘口5']
    #result_df = result_df.drop(result_df[result_df[0]=='盘口2'],axis=0)
    #print(result_df)
    result2 = np.array(result_df)
    result2 = result2.flatten()
    result2 = result2.tolist()
    #print(result2)
    # Hang = (int)(len(result2) / 7)
    # for i in range(len(result2)+Hang*2):
    #     if result2[i] in company:
    #         if (float(score[0]) + float(score[1]) > float(result2[i + 2])):
    #             result2.insert(i + 1, '1')
    #         elif (float(score[0]) + float(score[1]) == float(result2[i + 2])):
    #             result2.insert(i + 1, '0')
    #         elif (float(score[0]) + float(score[1]) < float(result2[i + 2])):
    #             result2.insert(i + 1, '-1')
    #
    #         if (float(score[0]) + float(score[1]) > float(result2[i + 6])):
    #             result2.insert(i + 2, '1')
    #         elif (float(score[0]) + float(score[1]) == float(result2[i + 6])):
    #             result2.insert(i + 2, '0')
    #         elif (float(score[0]) + float(score[1]) < float(result2[i + 6])):
    #             result2.insert(i + 2, '-1')
    # print(result2)
    url = 'http://nba.win007.com/analysis/'+str(gameid)+'.htm'
    request = urllib.request.Request(url=url,headers={"User-Agent": random.choice(user_agent)})  # 随机从user_agent列表中抽取一个元素
    response = urllib.request.urlopen(request)
    content = response.read().decode('UTF-8')  # 读取网页内容
    time.sleep(random.randrange(1, 2))

    #print(content)
    pattern = re.compile(
        '(?<=var e_data=)[\S\s]+(?=var f_data)')
    state = re.findall(pattern, str(content))
    state = str(state)
    state = state.replace('\'', '').replace('[', '').replace(']', '').replace(';', '').replace(' ', '').replace('\\r', '').replace('\\n', '')
    state = state.split(',')
    e_data = []  # result：最终数据
    Hang = (int)(len(state) / 27)
    # 转换成多维列表
    for y in range(0, Hang):
        for x in range(0, 27):
            if x == 0:
                e_data.append([])
            e_data[y].append(state[x + y * 27])
    #print(e_data)

    data = e_data
    Get = 0
    Lose = 0
    Hcount = 0
    Gcount = 0
    H_Get = 0
    H_Lose = 0
    G_Get = 0
    G_Lose = 0
    Get_5 = 0
    Lose_5 = 0
    Get_10 = 0
    Lose_10 = 0
    for i in range(Hang):
        Get += int(data[i][3])
        Lose += int(data[i][4])
        if i < 5 :
            Get_5 += int(data[i][3])
            Lose_5 += int(data[i][4])
        if i<10:
            Get_10 += int(data[i][3])
            Lose_10 += int(data[i][4])
        if(int(data[i][5]) == 1):
            Hcount += 1
            H_Get += int(data[i][3])
            H_Lose += int(data[i][4])
        elif(int(data[i][5]) == 0):
            Gcount += 1
            G_Get += int(data[i][3])
            G_Lose += int(data[i][4])

    e_AveG = round(float(Get / Hang),2)
    e_AveL = round(float(Lose / Hang),2)
    e_AveHG = round(float(H_Get / Hcount),2)
    e_AveHL = round(float(H_Lose / Hcount),2)
    e_AveGG = round(float(G_Get / Gcount),2)
    e_AveGL = round(float(G_Lose / Gcount),2)
    e_AveG5 = round(float(Get_5 / 5), 2)
    e_AveL5 = round(float(Lose_5 / 5), 2)
    e_AveG10 = round(float(Get_10 / 10), 2)
    e_AveL10 = round(float(Lose_10 / 10), 2)

    pattern = re.compile(
        '(?<=var h_data=)[\S\s]+(?=var a_data)')
    state = re.findall(pattern, str(content))
    state = str(state)
    state = state.replace('\'', '').replace('[', '').replace(']', '').replace(';', '').replace(' ', '').replace('\\r',
                                                                                                                '').replace(
        '\\n', '')
    state = state.split(',')
    v_data = []  # result：最终数据
    Hang = (int)(len(state) / 36)
    # 转换成多维列表
    for y in range(0, Hang):
        for x in range(0, 36):
            if x == 0:
                v_data.append([])
            v_data[y].append(state[x + y * 36])
    # v_data_df = pd.DataFrame(v_data)
    # pd.set_option('display.max_columns', None)
    # print(v_data_df)
    data = v_data
    Win_5 = 0
    Win_10 = 0
    Handicap_5 = 0
    Handicap_10 = 0
    Big_5 = 0
    Big_10 = 0

    for i in range(Hang):
        if i < 5:
            if ((data[i][9]) == '1'):
                Win_5 += 1
            if ((data[i][12]) == '1'):
                Handicap_5 += 1
            if ((data[i][15]) == '1'):
                Big_5 += 1
        if i < 10:
            if ((data[i][9]) == '1'):
                Win_10 += 1
            if ((data[i][12]) == '1'):
                Handicap_10 += 1
            if ((data[i][15]) == '1'):
                Big_10 += 1

    e_Win_5 = round(float(Win_5 / 5), 2)
    e_Handicap_5 = round(float(Handicap_5 / 5), 2)
    e_Big_5 = round(float(Big_5 / 5), 2)
    e_Win_10 = round(float(Win_10 / 10), 2)
    e_Handicap_10 = round(float(Handicap_10 / 10), 2)
    e_Big_10 = round(float(Big_10 / 10), 2)

    pattern = re.compile(
        '(?<=var f_data=)[\S\s]+(?=var h_ranking)')
    state = re.findall(pattern, str(content))
    state = str(state)
    state = state.replace('\'', '').replace('[', '').replace(']', '').replace(';', '').replace(' ', '').replace('\\r', '').replace('\\n', '')
    state = state.split(',')
    f_data = []  # result：最终数据
    Hang = (int)(len(state) / 27)
    # 转换成多维列表
    for y in range(0, Hang):
        for x in range(0, 27):
            if x == 0:
                f_data.append([])
            f_data[y].append(state[x + y * 27])
    # print(f_data)

    data = f_data
    Get = 0
    Lose = 0
    Hcount = 0
    Gcount = 0
    H_Get = 0
    H_Lose = 0
    G_Get = 0
    G_Lose = 0
    Get_5 = 0
    Lose_5 = 0
    Get_10 = 0
    Lose_10 = 0

    for i in range(Hang):
        Get += int(data[i][3])
        Lose += int(data[i][4])
        if i < 5 :
            Get_5 += int(data[i][3])
            Lose_5 += int(data[i][4])
        if i < 10:
            Get_10 += int(data[i][3])
            Lose_10 += int(data[i][4])
        if (int(data[i][5]) == 1):
            Hcount += 1
            H_Get += int(data[i][3])
            H_Lose += int(data[i][4])
        elif (int(data[i][5]) == 0):
            Gcount += 1
            G_Get += int(data[i][3])
            G_Lose += int(data[i][4])

    f_AveG = round(float(Get / Hang),2)
    f_AveL = round(float(Lose / Hang),2)
    f_AveHG = round(float(H_Get / Hcount),2)
    f_AveHL = round(float(H_Lose / Hcount),2)
    f_AveGG = round(float(G_Get / Gcount),2)
    f_AveGL = round(float(G_Lose / Gcount),2)
    f_AveG5 = round(float(Get_5 / 5), 2)
    f_AveL5 = round(float(Lose_5 / 5), 2)
    f_AveG10 = round(float(Get_10 / 10), 2)
    f_AveL10 = round(float(Lose_10 / 10), 2)

    pattern = re.compile(
        '(?<=var a_data=)[\S\s]+(?=var ma_data)')
    state = re.findall(pattern, str(content))
    state = str(state)
    state = state.replace('\'', '').replace('[', '').replace(']', '').replace(';', '').replace(' ', '').replace('\\r',
                                                                                                                '').replace(
        '\\n', '')
    state = state.split(',')
    a_data = []  # result：最终数据
    Hang = (int)(len(state) / 36)
    # 转换成多维列表
    for y in range(0, Hang):
        for x in range(0, 36):
            if x == 0:
                a_data.append([])
            a_data[y].append(state[x + y * 36])
    # a_data_df = pd.DataFrame(a_data)
    # pd.set_option('display.max_columns', None)
    # print(a_data_df)
    data = a_data
    Win_5 = 0
    Win_10 = 0
    Handicap_5 = 0
    Handicap_10 = 0
    Big_5 = 0
    Big_10 = 0

    for i in range(Hang):
        if i < 5:
            if ((data[i][9]) == '1'):
                Win_5 += 1
            if ((data[i][12]) == '1'):
                Handicap_5 += 1
            if ((data[i][15]) == '1'):
                Big_5 += 1
        if i < 10:
            if ((data[i][9]) == '1'):
                Win_10 += 1
            if ((data[i][12]) == '1'):
                Handicap_10 += 1
            if ((data[i][15]) == '1'):
                Big_10 += 1

    f_Win_5 = round(float(Win_5 / 5), 2)
    f_Handicap_5 = round(float(Handicap_5 / 5), 2)
    f_Big_5 = round(float(Big_5 / 5), 2)
    f_Win_10 = round(float(Win_10 / 10), 2)
    f_Handicap_10 = round(float(Handicap_10 / 10), 2)
    f_Big_10 = round(float(Big_10 / 10), 2)

    pattern = re.compile(
        '(?<=var h_ranking=)[\S\s]+(?=var g_ranking)')
    state = re.findall(pattern, str(content))
    state = str(state)
    state = state.replace('\'', '').replace('[', '').replace(']', '').replace(';', '').replace(' ', '').replace('\\r', '').replace('\\n', '').replace('\"', '')
    Hrank = state.split(',')
    #print(state)
    pattern = re.compile(
        '(?<=var g_ranking=)[\S\s]+(?=var v_data)')
    state = re.findall(pattern, str(content))
    state = str(state)
    state = state.replace('\'', '').replace('[', '').replace(']', '').replace(';', '').replace(' ', '').replace('\\r', '').replace('\\n', '').replace('\"', '')
    Grank = state.split(',')
    #print(state)

    ranking = [e_AveG, e_AveL, e_AveHG, e_AveHL, e_AveGG, e_AveGL, e_AveG5, e_AveL5, e_AveG10, e_AveL10, e_Win_5,
               e_Handicap_5, e_Big_5, e_Win_10, e_Handicap_10, e_Big_10, ] + Hrank + [f_AveG, f_AveL, f_AveHG, f_AveHL,
                                                                                      f_AveGG, f_AveGL, f_AveG5,
                                                                                      f_AveL5, f_AveG10, f_AveL10,
                                                                                      f_Win_5, f_Handicap_5, f_Big_5,
                                                                                      f_Win_10,
                                                                                      f_Handicap_10, f_Big_10] + Grank
    #print(ranking)

    gameid_list = [gameid]

    result =  gameid_list + playtime + LName + team_name + VS + score + ranking + result1 + result2

    if (float(score[0]) - float(score[1]) > float(result[50])):
        result.insert(8, '1')
    elif (float(score[0]) - float(score[1]) == float(result[50])):
        result.insert(8, '0')
    elif (float(score[0]) - float(score[1]) < float(result[50])):
        result.insert(8, '-1')

    if (float(score[0]) - float(score[1]) > float(result[54])):
        result.insert(9, '1')
    elif (float(score[0]) - float(score[1]) == float(result[54])):
        result.insert(9, '0')
    elif (float(score[0]) - float(score[1]) < float(result[54])):
        result.insert(9, '-1')

    if (float(score[0]) + float(score[1]) > float(result[122])):
        result.insert(10, '1')
    elif (float(score[0]) + float(score[1]) == float(result[122])):
        result.insert(10, '0')
    elif (float(score[0]) + float(score[1]) < float(result[122])):
        result.insert(10, '-1')

    if (float(score[0]) + float(score[1]) > float(result[126])):
        result.insert(11, '1')
    elif (float(score[0]) + float(score[1]) == float(result[126])):
        result.insert(11, '0')
    elif (float(score[0]) + float(score[1]) < float(result[126])):
        result.insert(11, '-1')

    # result = np.array(result)
    # result = result.transpose()
    print(result)

    result_df = pd.DataFrame(result)#, columns=['编号', '时间', '联赛', '主队', '客队', '联赛', '公司1', '初主', '初盘', '初客', '终主', '终盘', '终客', '公司2', '初主', '初盘', '初客', '终主', '终盘', '终客', '公司3', '初主', '初盘', '初客', '终主', '终盘', '终客', '公司4', '初主', '初盘', '初客', '终主', '终盘', '终客', '公司5', '初主', '初盘', '初客', '终主', '终盘', '终客', '公司6', '初主', '初盘', '初客', '终主', '终盘', '终客'])
    result_df = result_df.transpose()

    if (Lname == 'NBA'):
        path = root + '\\' + 'NBAdata' + '.xlsx'
    elif(Lname == 'CBA'):
        path = root + '\\' + 'CBAdata' + '.xlsx'


    if (os.path.isfile(path)):
        Bdata = pd.read_excel(path)
        result_df = Bdata.append(result_df, ignore_index=True)
    result_df[0] = result_df[0].astype('str')

    result_df = result_df.drop_duplicates(subset=[0], keep='last')
    result_df.sort_values(1, inplace=True)
    result_df.to_excel(path, index=None)

    if (VS[0] == '完'):
        spider_done(gameid)
        return

def arrange( newid ):
    newid_t = []
    for i in newid:
        newid_t.append(int(i))
    # newid = newid_t
    root = os.getcwd()
    path_wait = root + '\\' + 'Bwait' + '.xlsx'
    path_done = root + '\\' + 'Bdone' + '.xlsx'
    if(os.path.isfile(path_wait)):
        wait_sp = pd.read_excel(path_wait)
        wait_sp_list = wait_sp[0].tolist()
    else:
        wait_sp_list = []
    if (os.path.isfile(path_done)):
        done_sp = pd.read_excel(path_done)
        done_sp_list = done_sp[0].tolist()
    else:
        done_sp_list = []
    wait_sp_list.extend(newid_t)
    new_wait_sp = ["0"]
    for i in wait_sp_list:
        if i not in done_sp_list:
            if i not in new_wait_sp:
                new_wait_sp.append(i)
    print(new_wait_sp)
    new_wait_sp_df = pd.DataFrame(new_wait_sp)
    new_wait_sp_df = new_wait_sp_df.drop(labels=0)
    del new_wait_sp[0]
    new_wait_sp_df.to_excel(path_wait, header=True, index=None)#, startrow=len(old))
    return new_wait_sp


def pred_pred(Lname):
    root = os.getcwd()  # 获取当前路径
    if Lname == 'NBA':
        path = root + '\\' + 'NBAdata' + '.xlsx'
    elif Lname == 'CBA':
        path = root + '\\' + 'CBAdata' + '.xlsx'

    train_data_all = pd.read_excel(path)
    train_data_all.fillna(0)

    label_n = ['6', '7', '8', '10']
    label_zk = 9
    label_dx = 11
    for i in label_n:
        train_data_all = train_data_all.drop(columns=int(i))

    test_data = []
    test_data = pd.DataFrame(train_data_all)
    test_data.drop(index=(test_data.loc[(test_data[5] == "完")].index), inplace=True)
    print(test_data)
    if ((len(test_data)) == 0):
        return

    if Lname == 'NBA':
        save_path_zk_D = ['agModels-predictClassNBAzk_D', 'agModels-predictClassNBAdx_D']
        save_path_zk_3D = ['agModels-predictClassNBAzk_3D', 'agModels-predictClassNBAdx_3D']
        save_path_zk_W = ['agModels-predictClassNBAzk_W', 'agModels-predictClassNBAdx_W']
        save_path_zk_M = ['agModels-predictClassNBAzk_M', 'agModels-predictClassNBAdx_M']
        save_path_zk_A = ['agModels-predictClassNBAzk_A', 'agModels-predictClassNBAdx_A']
    elif Lname == 'CBA':
        save_path_zk_D = ['agModels-predictClassCBAzk_D', 'agModels-predictClassCBAdx_D']
        save_path_zk_3D = ['agModels-predictClassCBAzk_3D', 'agModels-predictClassCBAdx_3D']
        save_path_zk_W = ['agModels-predictClassCBAzk_W', 'agModels-predictClassCBAdx_W']
        save_path_zk_M = ['agModels-predictClassCBAzk_M', 'agModels-predictClassCBAdx_M']
        save_path_zk_A = ['agModels-predictClassCBAzk_A', 'agModels-predictClassCBAdx_A']

    save_path_list = [save_path_zk_D, save_path_zk_3D, save_path_zk_W, save_path_zk_M, save_path_zk_A]

    out_pred = []
    out_pred = pd.DataFrame()
    out_pred['编号'] = test_data[0]
    out_pred['时间'] = test_data[1]
    out_pred['联赛'] = test_data[2]
    out_pred['主队'] = test_data[3]
    out_pred['客队'] = test_data[4]

    for i in range(len(save_path_list)):
        save_path_zk = save_path_list[i][0]
        save_path_dx = save_path_list[i][1]


        test_data_nolab = test_data.drop(columns=[label_zk])
        test_data_nolab = test_data_nolab.drop(columns=[label_dx])

        predictor = TabularPredictor.load(save_path_zk)
        y_pred = predictor.predict(test_data_nolab)
        # print(y_pred)
        out_pred[save_path_zk] = y_pred
        # print(out_pred)
        predictor = TabularPredictor.load(save_path_dx)
        y_pred = predictor.predict(test_data_nolab)
        #print(y_pred)
        out_pred[save_path_dx] = y_pred
    print(out_pred)
    out_pred['sum_zk'] = out_pred[
        [save_path_list[1][0], save_path_list[2][0], save_path_list[3][0],
         save_path_list[4][0]]].sum(axis=1)#save_path_list[0][0],
    out_pred['sum_dx'] = out_pred[
        [save_path_list[1][1], save_path_list[2][1], save_path_list[3][1],
         save_path_list[4][1]]].sum(axis=1)#save_path_list[0][1],

    out_pred['zk'] = out_pred.apply(lambda x: '主' if x['sum_zk'] == 4 else '客' if x['sum_zk'] == -4 else 0,
                                    axis=1)
    out_pred['dx'] = out_pred.apply(lambda x: '大' if x['sum_dx'] == 4 else '小' if x['sum_dx'] == -4 else 0,
                                    axis=1)

    if Lname == 'NBA':
        path_out_pred = root + '\\' + 'NBAout_pred' + '.xlsx'
    elif Lname == 'CBA':
        path_out_pred = root + '\\' + 'CBAout_pred' + '.xlsx'

    if (os.path.isfile(path_out_pred)):
        Odata = pd.read_excel(path_out_pred)
        out_pred = Odata.append(out_pred, ignore_index=True)
    out_pred['编号'] = out_pred['编号'].astype('str')

    out_pred = out_pred.drop_duplicates(subset=['编号'], keep='last')
    out_pred.sort_values(by='时间', inplace=True)
    # result_df = result_df.sort_values(by='时间', ascending=True)
    # result_df = result_df.reset_index(drop=True)
    out_pred.to_excel(path_out_pred, index=None)

    time_now = time.strftime("%Y-%m-%d %H:%M", time.localtime())


    out_pred['diff'] = out_pred.apply(
        lambda x: time.mktime(time.strptime(str(x['时间']), "%Y-%m-%d %H:%M")) - time.mktime(
            time.strptime(str(time_now), "%Y-%m-%d %H:%M")),
        axis=1)
    out_pred_1 = out_pred[(out_pred['diff']>-2400)&(out_pred['diff']<2400)]
    print(out_pred_1)

    return


if __name__ == '__main__':
    time_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gameid = spider()
    new_waitid = arrange(gameid)
    for i in new_waitid:
        gamespider(i)
    pred_pred('CBA')
    pred_pred('NBA')
    time_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(time_start)
    print(time_end)
    hour = time.localtime().tm_hour
    min = time.localtime().tm_min
    if((hour == 0) &(min<=29)):
        predfit.pred_fit('NBA')
        predfit.pred_fit('CBA')

