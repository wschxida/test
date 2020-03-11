import re
import logging

# 添加关键词过滤，keywords_* = (a,b) a：分割符，b：关键词组合，以a分割
# 例: keywords_7 = (',', 'lpl,团战,一局,游戏') 包含 'lpl,团战,一局,游戏' 其中任意词视为无效数据，以','分割

keywords_1 = (',', '哪家医院,妇科,人流,白斑,包皮,除皱,肿瘤,勃起障碍,癫痫病,医院怎么样,医院好不好,医院在哪儿,有什么症状,微创,'
                   '治性病,怎样去除,肝癌,专业整容,美容专家,瘦脸针,主任医师,丰臀,不用开刀,肌肤恢复,整形医院,吸脂,双眼皮,'
                   '哪个正规,个人店铺,欢迎光临,欢迎阁下,吸引男人,养肾法,男士专用')
keywords_2 = (',', '彩票,bet,365,彩投注,现场投注,体验金,博彩,网上娱乐,赌博平台开户,娱乐平台,澳门娱乐,钻石娱乐,注册赔率,'
                   '体育投注,送现金,赌场,线上娱乐,国际娱乐,竞彩推荐,送彩金,免费试玩,不夜城,娱乐城,赌博网,欢迎您,百家乐,'
                   '老虎机,娱乐返水,娱乐')

keywords_3 = (',', '用户登录,输入密码,输入验证码,(.*\.com)')
keywords_4 = ('&', '吗\?&怎么样&多少&谁用过&用品|走势')
keywords_5 = (',', '二手房出售,装修设计,户型图,急售,效果图,样板间,宣传片,租房,南北通,装修图片,二居室,三居室,四居室,平米,精装,'
                   '房价走势,房源列表,均价约,户型结构,黄金楼层,万起送,豪装,有钥匙')

keywords_6 = (',', '彩投注,现场投注,体验金,博彩,网上娱乐,赌博平台开户,娱乐平台,澳门娱乐,钻石娱乐,注册赔率,体育投注,送现金,赌场,'
                   '线上娱乐,国际娱乐,竞彩推荐,送彩金,免费试玩,不夜城,娱乐城,赌博网,欢迎您,百家乐,老虎机,娱乐返水,娱乐')

keywords_7 = (',', 'lpl,团战,一局,游戏')

# url，keywords_* = (a,b) a：分割符，b：url组合，以a分割

urls_1 = (',', 'http://bbs.51credit.com/forum-83-277.html,forumdisplay.php.*?fid,mod=forumdisplay.*fid=')
urls_2 = (',', '\/forum-\d+-\d+\.html')

# seo，特征词组合过滤规则


#  参数，分割词自行自定和分割
#  specify_chars关键词合集，count：关键词在当前串出现的次数阈值，ratio 关键词在当前字符串的占比阈值
# 例：dict(specify_chars='-&>>'.split('&'), count=6, ratio=0.2) 过滤关键字'-'和'>>' ，当在当前字符串出现次数大于6时或字符占
#     比大于0.2时，判定是无效数据
rule_info_1 = [dict(specify_chars='_&|'.split('&'), count=4, ratio=0.2),
               dict(specify_chars='・'.split('&'), ratio=0.2),
               dict(specify_chars=',& &　'.split('&'), ratio=0.34),  # 空格：chr(32) and chr(12288)
               dict(specify_chars='-&>>'.split('&'), count=6, ratio=0.2)
               ]  # 过滤掉 SEO内容,针对标题

rule_info_2 = [dict(specify_chars='ICP备&地址：&邮编：'.split('&'), ratio=0.2),
               dict(specify_chars='第&页&上一页&下一页&首页&尾页'.split('&'), ratio=0.15),
               dict(specify_chars='设为首页&收藏本&站长统计&联系我们&关于我们&免责声明'.split('&'), ratio=0.15),
               dict(specify_chars='联系人&电话&QQ&手机&邮箱&Email'.split('&'), ratio=0.2),
               dict(specify_chars='回答&答案&题&解析&家教网&试题'.split('&'), ratio=0.2),
               dict(specify_chars='年&2015年&2014年&2013年&2012年&2011年'.split('&'), ratio=0.15),
               dict(specify_chars='违规贴吧举报反馈通道&批发&位置&404&失效页面&寻人计划'.split('&'), ratio=0.15),
               dict(specify_chars='―& - &...&会员中心&门户网站&网'.split('&'), ratio=0.25),
               ]  # 多种组合 垃圾特征词过滤,针对标题

rule_info_3 = [dict(specify_chars='_&|'.split('&'), count=4, ratio=0.2),
               dict(specify_chars='・'.split('&'), ratio=0.2),
               dict(specify_chars=',& &　'.split('&'), ratio=0.34),  # chr(32) and chr(12288)
               dict(specify_chars='-&>>'.split('&'), count=6, ratio=0.2)
               ]  # 过滤掉 SEO内容,针对摘要

rule_info_4 = [dict(specify_chars='ICP备&地址：&邮编：'.split('&'), ratio=0.2),
               dict(specify_chars='第&页&上一页&下一页&首页&尾页'.split('&'), ratio=0.15),
               dict(specify_chars='设为首页&收藏本&站长统计&联系我们&关于我们&免责声明'.split('&'), ratio=0.15),
               dict(specify_chars='联系人&电话&QQ&手机&邮箱&Email'.split('&'), ratio=0.2),
               dict(specify_chars='回答&答案&题&解析&家教网&试题'.split('&'), ratio=0.2),
               dict(specify_chars='年&2015年&2014年&2013年&2012年&2011年'.split('&'), ratio=0.15),
               dict(specify_chars='违规贴吧举报反馈通道&批发&位置&404&失效页面&寻人计划'.split('&'), ratio=0.15),
               dict(specify_chars='―& - &会员中心&门户网站&网'.split('&'), ratio=0.25)
               ]  # 多种组合 垃圾特征词过滤,针对摘要

keyword_list = []
url_list = []
for i, j in dict(globals().items()).items():
    if 'keywords_' in i:
        keyword_list += j[1].split(j[0])
    if 'urls_' in i:
        url_list += j[1].split(j[0])

is_junk_urls = lambda content: True if re.search('|'.join(url_list), (content if content else ''), re.I) else False
is_junk_words = lambda content: True if re.search('|'.join(keyword_list), (content if content else ''), re.I) else False


# 以下为上面两个函数的测试，实际运行用上面的函数即可
def is_junk_urls_test(content: str):
    '''测试用',过滤链接'''
    data = re.search('|'.join(url_list), content)
    if data:
        logging.warning(data.group())
        return True
    else:
        return False


def is_junk_words_test(content: str):
    '''测试用,过滤垃圾词'''
    data = re.search('|'.join(keyword_list), content)
    if data:
        logging.warning(data.group())
        return True
    else:
        return False


as_establish_1 = lambda value, _content, info: specify_char_ratio(_content, value) > info.get('ratio') \
                                               and _content.count(value) > info.get('count')
as_establish_2 = lambda value, _content, info: specify_char_ratio(_content, value) > info.get('ratio')
as_establish_3 = lambda value, _content, info: _content.count(value) > info.get('count')


def is_junk_content_seo(_content, info_list):
    '''
    过滤掉 SEO内容
    列表值可以是一下情况
    长度和比例自定义，
    1,判断字符占长及字符出现次数比例
    2，只判断字符占长
    3,只判断字符出现次数比例

    retuen 只返回布尔值
    #######
    '''
    for info in info_list:
        if info.get('count') and info.get('ratio'):
            as_establish = as_establish_1
        elif info.get('ratio'):
            as_establish = as_establish_2
        else:
            as_establish = as_establish_3
        for value in info.get('specify_chars'):
            if as_establish(value, _content, info):
                logging.warning('%s，%s' % (info.get('specify_chars'), value))
                return True
    else:
        return False


def is_junk_content_feature_word(_content, info_list):
    '''
    多种组合 垃圾特征词过滤
    :param _content:
    :param info_list:
    :return:
    '''
    for info in info_list:
        _ratio = 0
        for specify_chars in info.get('specify_chars'):
            _ratio += specify_char_ratio(_content, specify_chars)
            if _ratio > info.get('ratio'):
                logging.warning('%s，%s' % (info.get('specify_chars'), specify_chars))
                return True
    else:
        return False


def specify_char_ratio(all_strings, specify_char):
    '''
    返回给定字符占总字符长度的比例
    :param all_strings:
    :param specify_char:
    :return:
    '''

    _temp_str = all_strings.replace(specify_char, '')
    _length_all_strings, _length_temp_str = len(all_strings), len(_temp_str)
    return (_length_all_strings - _length_temp_str) / _length_all_strings


def py_isjunk(title=None, abstract=None, url=None):
    is_junk = False

    if title and not is_junk:
        is_junk = is_junk_content_seo(title, rule_info_1) or is_junk_content_feature_word(title, rule_info_2) or \
                  is_junk_words_test(title)
    if abstract and not is_junk:
        is_junk = is_junk_content_seo(abstract, rule_info_3) or is_junk_content_feature_word(abstract, rule_info_4) or \
                  is_junk_words_test(abstract)
    if url and not is_junk:
        is_junk = is_junk_urls_test(url)
    return is_junk


if __name__ == '__main__':
    title = '拓木者家居企业店家具怎么样?茶几电视柜质量好吗(图)'
    abstract = '红苹果家具- 床|餐台|茶几|沙发|床垫|电视柜|全屋定制|定制家具|定制... 深..'
    url = 'https://m.sogou.com/ntcnews?clk=10&url=http%3A%2F%2Fwww.hbdushi.cn%2F2017%2F0920%2F65431.html&g_ut=2&ct=' \
          '180425142102&sz=0-0&key=%E7%BA%A2%E8%8B%B9%E6%9E%9C+%E5%BA%8A%E5%9E%AB&uID=8nqyDOshmxZGwI1L&pno=2&v=2&type=1'

    junk = py_isjunk(title, abstract, url)
    logging.warning(' junk:%s\n%s\n%s\n%s' % (junk, title, abstract, url))
