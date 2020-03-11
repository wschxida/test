#coding:utf-8

# P脚本分割字符串
def P(text, pattern, partNo=0):
    text_p = text
    pattern_list = pattern.split('*')
    # print(pattern_list)

    # 先把关键字替换成/
    for str in pattern_list:
        if str:
            if str in text:
                text_p = text_p.replace(str,'/')

    text_list = text_p.split('/')
    pattern_count = pattern.count('*')
    # print(text_p)
    # print(text_list)

    # partNo是整数时以及pattern需要有*才进行截取
    if isinstance(partNo,int) and pattern.find('*')>=0:
        if partNo == 0:
            result = text
        # pattern是否以*开头
        elif partNo > 0 and partNo <= pattern_count and len(text_list)>1 and pattern.startswith('*'):
            result = text_list[partNo - 1]
        elif partNo > 0 and partNo <= pattern_count and len(text_list)>1 and not pattern.startswith('*'):
            result = text_list[partNo]
        else:
            result = ''
    else:
        result = ''
    return result

s = '111c222f333g444'
p = '*cf'
d = 123



print(s)
print(p)
print('--------s_p = P(s, p, 0)--------')
s_p = P(s, p, 0)
print(s_p)
print('--------s_p = P(s, p, 1)--------')
s_p = P(s, p, 1)
print(s_p)
print('--------s_p = P(s, p, 2)--------')
s_p = P(s, p, 2)
print(s_p)
print('--------s_p = P(s, p, 10)--------')
s_p = P(s, p, 10)
print(s_p)
print('--------s_p = P(s, p, -1)--------')
s_p = P(s, p, -1)
print(s_p)
print("--------s_p = P(s, p, 'a')--------")
s_p = P(s, p, 'a')
print(s_p)
print("--------s_p = P(s, p, '1')--------")
s_p = P(s, p, '1')
print(s_p)
