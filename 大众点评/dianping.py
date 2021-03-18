#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2021/3/10
# @Desc  :
# 参考：https://blog.csdn.net/m0_49077792/article/details/111369149
# 参考：https://segmentfault.com/a/1190000021880099
# font字体展示软件：https://www.high-logic.com/font-editor/fontcreator/download-confirmation


# encoding=utf-8
import os
import requests
import re
import random


from urllib.parse import quote
from fontTools.ttLib import TTFont
from lxml import etree

USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    ]


class DaZhong(object):
    def __init__(self):
        self.zitiUrl = "https://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/12fd772aee773d8a96ad5a354d8b595a.css"
        self.start_url = 'http://www.dianping.com/shenzhen/ch10'
        self.headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Referer': 'http://www.dianping.com/',
            'Cookie': '_lxsdk_cuid=1773e8d728cc8-09d44ed5ed080f-c791e37-1fa400-1773e8d728cc8; _lxsdk=1773e8d728cc8-09d44ed5ed080f-c791e37-1fa400-1773e8d728cc8; _hc.v=1b0f302f-f672-9b25-fb69-2a03acf06d04.1615360422; fspop=test; cy=7; cye=shenzhen; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1615360422,1615369303; s_ViewType=10; _lxsdk_s=1781ba8a48b-813-b51-1fb%7C%7C20; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1615371741'
        }

    def get_ziti(self):   # 根据字体的url把字体文件保存到本地
        res = requests.get(self.zitiUrl)
        font = re.findall(r'font-family: "(.*?)";src.*?(//s3plus\.meituan\.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/\w+.woff)', res.text, re.S)
        font_list = ['https:' + x[1] for x in font]
        font_name = [x[0] for x in font]
        for i in font_list:
            result = requests.get(i)
            file_name = i.split('/')[-1]
            with open(file_name, 'wb')as f:
                f.write(result.content)

    def parse_ziti(self, class_name, datas):

        if class_name == 'shopNum':   # 评论数， 人均消费， 口味环境服务分数
            woff_name = 'ebb40305.woff'
        elif class_name == 'tagName':   # 店铺分类，哪个商圈
            woff_name = '9b3f551f.woff'
        else:
            woff_name = '1d742900.woff'   # 店铺具体地址
        # 评分
        font_data = TTFont(woff_name)
        font_data.saveXML(woff_name)   # 保存xml便于做分析
        words = '1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下臬凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晚微周值费性桌拍跟块调糕'
        gly_list = font_data.getGlyphOrder()[2:]
        # print(gly_list)  # ['unie8a0', 'unie910', 'unif6a4', 'unif3d3', 'unie2f4', 'unie7a6', 'uniea32', 'unif0f9', 'unie2ac']
        new_dict = {}
        for index, value in enumerate(words):
            new_dict[gly_list[index]] = value
        print(new_dict)
        rel = ''
        for j in datas:
            if j.startswith('u'):
                rel += new_dict[j]
            else:
                rel += j
        return rel

    def get_page_info(self):  # 获取网页上需要的数据
        response = requests.get(self.start_url, headers=self.headers)
        print(response.status_code)
        with open('dazhong.html', 'w', encoding='utf-8')as f:   # 这里我把html保存到本地方便使用，不然超级容易被封ip
          f.write(response.text)
        with open('dazhong.html', 'r', encoding='utf-8') as f:
            html_ = f.read()
        html_ = re.sub(r"&#x(\w+?);", r"*\1", html_)   # 网页源码每个数字对应的内容，保留括号里的内容，把括号前面的内容替换为*
        html = etree.HTML(html_)
        # 所有数据的标签
        all_info = []
        li_list = html.xpath("//div[@class='content']/div/ul/li")
        for li in li_list:
            item = {}
            item['店铺名'] = li.xpath('./div[2]/div/a/h4/text()')[0]
            item['推荐菜'] = li.xpath('./div[2]/div[4]/a//text()')
            if item['推荐菜'] is not None:
                item['推荐菜'] = ','.join(li.xpath('./div[2]/div[4]/a//text()'))
            else:
                item['推荐菜'] = ''
            # 标签名称
            class_name = li.xpath("./div[2]/div[2]/a[1]/b/svgmtsi/@class")[0]
            tag_name = li.xpath('./div[2]/div[3]/a[2]/span/svgmtsi/@class')[0]
            addr_name = li.xpath('./div[2]/div[3]/span/svgmtsi/@class')[0]
            comment_num = li.xpath("./div[2]/div[2]/a[1]/b//text()")   # 拿评论的数据['1', '*e2ac', '*f0f9', '*e2ac', '*e8a0']
            # 遍历列表，把*号开头的去掉，并与uni拼接成新的，如果是1，则放在列表里，得到新的列表 ['1', 'unie2ac', 'unif0f9', 'unie2ac', 'unie8a0']
            comment_num_list = ['uni' + i.strip('*') if i.startswith('*') else i for i in comment_num]
            item['评价数'] = self.parse_ziti(class_name, comment_num_list)

            avg_price = li.xpath("./div[2]/div[2]/a[2]/b//text()")   # 人均消费
            avg_price_list = ['uni' + i.strip('*') if i.startswith('*') else i for i in avg_price]
            item['人均'] = self.parse_ziti(class_name, avg_price_list)

            shop_area = li.xpath('./div[2]/div[3]/a[2]/span//text()')   # 商圈
            shop_area_list = ['uni' + i.strip('*') if i.startswith('*') else i for i in shop_area]
            item['商圈'] = self.parse_ziti(tag_name, shop_area_list)

            shop_type = li.xpath('./div[2]/div[3]/a[1]/span//text()')  # 商铺类型
            shop_type_list = ['uni' + i.strip('*') if i.startswith('*') else i for i in shop_type]
            item['分类'] = self.parse_ziti(tag_name, shop_type_list)

            shop_address = li.xpath('./div[2]/div[3]/span//text()')   # 具体地址
            shop_address_list = ['uni' + i.strip('*') if i.startswith('*') else i for i in shop_address]
            item['地址'] = self.parse_ziti(addr_name, shop_address_list)

            zh_comment = li.xpath("./div[2]/span/span//text()")
            zh_comment_list = ['uni' + i.strip('*') if i.startswith('*') else i for i in zh_comment]
            item['综合评分'] = self.parse_ziti(class_name, zh_comment_list)

            all_info.append(item)
            print(all_info)


if __name__ == '__main__':
    dz = DaZhong()
    # dz.get_ziti()
    # dz.parse_ziti()
    dz.get_page_info()
