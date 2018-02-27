# -*- coding: utf-8 -*-
import requests
import os
HEADERS = {
    'Referer': 'http://www.chsi.com.cn/cet'
}


def query(kh_list):
    path = os.path.dirname(os.path.abspath(__file__))
    for param in kh_list:
        rsp = requests.get('http://www.chsi.com.cn/cet/query',
                           params=param, headers=HEADERS)
        if '无法找到对应的分数' not in rsp.text and '请输入验证码' not in rsp.text:
            with open(os.path.join(path, param['zkzh']+'.html'), 'wb', encoding='utf-8') as f:
                f.write(rsp.text.encode('utf-8'))
                print(param['zkzh'], '查询成功')
                print('结果保存在:', os.path.join(path, param['zkzh']+'.html'))
            break
        else:
            print(param['zkzh'], '尝试失败')

    else:
        print('查询失败')


def check_input(msg, df, check_size=True):
    print(msg)
    tip = '请输入>>> '
    while True:
        user_in = input(tip).strip()
        if check_size and user_in and len(user_in) != len(df):
            tip = '您的输入有误，请重新输入>>> '
        else:
            return user_in if user_in else df


def gen_zkzh():
    fixed = []
    flex = []
    print('***任何输入直接回车即为默认值***')
    TIP_XX = '''
    --------------------------------
    学校id,长度为5位
    默认值为山科大，其它学校请自主查询
    --------------------------------
    '''
    fixed.append(check_input(TIP_XX, '37055'))

    TIP_XQ = '''
    --------------------------------
    校区id,长度为1
    默认值为山科大青岛，其它校区请自主查询
    --------------------------------
    '''
    fixed.append(check_input(TIP_XQ, '1'))

    TIP_NF = '''
    --------------------------------
    年份id,长度为2
    默认值为17年
    --------------------------------
    '''
    fixed.append(check_input(TIP_NF, '17'))
    TIP_KJ = '''
    --------------------------------
    考季id,长度为1
    1为上半年，2为下半年
    默认值为下半年
    --------------------------------
    '''
    fixed.append(check_input(TIP_KJ, '2'))

    TIP_CET = '''
    --------------------------------
    四六级id,长度为1
    1为四级,2为6级
    默认值为4级
    --------------------------------
    '''
    fixed.append(check_input(TIP_CET, '1', False))

    TIP_KC = '''
    --------------------------------
    考场号id，长度为3
    该值为一个范围,挨个进行查询，直到正确为止
    格式： start end
    如，我要查300到310考场
    输入 300 310
    若想为定值，则end与start相同即可
    默认值为： 000 000
    不足3位，用0补齐
    --------------------------------
    '''
    flex.extend(map(int, check_input(TIP_KC, '000 000').split()))

    TIP_ZH = '''
    --------------------------------
    座号id,长度为2
    该值为一个范围,挨个进行查询，直到正确为止
    格式： start end
    如，我要查20到25号
    输入 20 25
    若想为定值，则end与start相同即可
    默认值为： 00 00
    不足2位，用0补齐
    --------------------------------
    '''
    flex.extend(map(int, check_input(TIP_ZH, '00 00').split()))

    TIP_XM = '''
    --------------------------------
    输入自己的大名即可
    默认值为 小脑斧
    --------------------------------
    '''
    name = check_input(TIP_XM, '小脑斧', False)

    fix_str = ''.join(fixed) + '{:0>3d}{:0>2d}'

    return ({'zkzh': fix_str.format(a, b), 'xm': name} for a in range(flex[0], flex[1]+1) for b in range(flex[2], flex[3]+1))


if __name__ == '__main__':
    kh_list = gen_zkzh()
    query(kh_list)
    while True:
        input("\n任意键退出")
        break
