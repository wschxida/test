
# -*- coding: UTF-8 -*-
__author__ = 'cedar'

card_list = []


def add_card():

    card_dict = {}
    card_dict["name"] = input("名字:")
    card_dict["phone"] = input("phone:")
    card_dict["qq"] = input("qq:")
    card_list.append(card_dict)


def show_all():

    print('{:10}\t\t{:10}\t\t{:10}'.format("name","phone","qq"))
    print('-' * 50)

    for card_dict in card_list:
        print('{:10}\t\t{:10}\t\t{:10}'.format(card_dict['name'],card_dict['phone'],card_dict['qq']))

    print('=' * 50)
    input('输入任意键返回：')


def search_card():
    search_name = input("请输入查询的名字:")
    for card_dict in card_list:
        if card_dict["name"] == search_name:
            print('{:10}\t\t{:10}\t\t{:10}'.format("name", "phone", "qq"))
            print('-' * 50)
            print('{:10}\t\t{:10}\t\t{:10}'.format(card_dict['name'], card_dict['phone'], card_dict['qq']))
            print('=' * 50)
            print('1：编辑')
            print('2：删除')
            print('0：返回')
            print('=' * 50)
            search_action = input('请输入需要的操作：')
            if search_action == '1':
                name_str = input("名字:")
                phone_str = input("phone:")
                qq_str = input("qq:")
                card_dict["name"] = edit_card(card_dict["name"],name_str)
                card_dict["phone"] = edit_card(card_dict["phone"], phone_str)
                card_dict["qq"] = edit_card(card_dict["qq"], qq_str)
                break
            if search_action == '2':
                card_list.remove(card_dict)
                break
            if search_action == '0':
                break

    else:
        print("查询不到结果")


def edit_card(card_value,input_str):
    card_value = card_value
    if len(input_str)>0:
        return input_str
    else:
        return card_value