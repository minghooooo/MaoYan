import requests
import json
import re
import csv
import datetime

class movie:
    def __init__(self):
        # 网址变化的是时间，时间处理{}
        self.start_url = "https://piaofang.maoyan.com/dashboard-ajax/movie?showDate={}"
        #运用网址的headers
        self.headers = {
           
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}

    def parse_url(self,url):# 发送请求，返回响应
        # 运用get方法来对网址发送请求
        self.response = requests.get(url,headers=self.headers)
        #返回响应
       
        return self.response
        

    def save_content(self):#保存csv文件
        file = open("D:\Maoyan_data.csv","a",newline="",encoding='utf-8-sig')
        writer = csv.writer(file)
        #写表头
        writer.writerow(('时间','排名','名称','综合票房','票房占比','排片占比','场均人次','上座率','当日大盘数据'))
        r = json.loads(self.response.content.decode())
        rstr = str(r)
        # print(r)
        # print("end")
        # print(rstr)
        #只在疫情期间出现的特殊的json数据名
        pattern = re.compile(r"'operationMsg'")
        #判断是否为疫情期间，是的话跳过爬取
        if  pattern.findall(rstr) :
            writer.writerow('疫情期间，影院关闭')
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        else:
            #自定排序
            rank = 0
            #获取时间
            #  r = json.loads(self.response.content.decode())
            date = r['calendar']['selectDate']
            print(date) #检查
            # 获取当日大盘数据
            dpsj = r['movieList']['nationBoxInfo']['nationBoxSplitUnit']['num']+r['movieList']['nationBoxInfo']['nationBoxSplitUnit']['unit']
            # print(dpsj) #检查
            for movie in self.response.json()['movieList']['list']:  
                rank = rank + 1  
                name = movie['movieInfo']['movieName']  # 查找数据
                zhpf = movie['boxSplitUnit']['num']
                pfzb = movie['boxRate']
                ppzb = movie['showCountRate']
                cjrc = movie['avgShowView']
                szl =  movie['avgSeatView']
                # print(date,rank, name, zhpf, pfzb, ppzb, cjrc, szl,dpsj)  
                # #检查
                #写入数据
                writer.writerow((date,rank,name,zhpf,pfzb,ppzb,cjrc,szl,dpsj))
           

    def run(self):#主要逻辑，执行循环
        #定义时间
        #因为疫情原因或网站自身原因，现存数据起始时间与终止时间如下
        start = '2020-7-31'
        end = '2019-08-01'
        datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
        #运用时间的循环来获取每一个网页的数据
        while datestart > dateend:
            datestart -= datetime.timedelta(days=1)
            print(datestart.strftime('%Y%m%d'))
            #用{}，.format来表示时间
            url = self.start_url.format(datestart.strftime('%Y%m%d'))
            html_str = self.parse_url(url)
            self.save_content()

#执行爬虫
if __name__ == '__main__':
    m = movie()
    m.run()