
# 获取telegram 群成员数据的程序入口


from configparser import ConfigParser
from src.TelegramChannelMemberExtractor import TGMemExtrator

cfg = ConfigParser()
cfg.read('./config/telegram_extractor.ini', encoding='utf-8')
config = {
    'TG_session_name': cfg.get('login_setting', 'TG_session_name'),
    'TG_api_id': int(cfg.get('login_setting', 'TG_api_id')),
    'TG_api_hash': cfg.get('login_setting', 'TG_api_hash'),
    'proxy_address': cfg.get('login_setting', 'proxy_address'),
    'proxy_port': int(cfg.get('login_setting', 'proxy_port')),
    'group_member': cfg.get('download_addr', 'group_member'),
    'group_avatar': cfg.get('download_addr', 'group_avatar')
}


def extractor_get_member(username):
    tgMemExtrator = TGMemExtrator(config)

    flag = False
    tgMemExtrator.set_channel(username)
    tgMemExtrator.dumpTojson(flag)


def main():
    username = 'Advancedchat'
    extractor_get_member(username)


if __name__ == '__main__':
    main()
