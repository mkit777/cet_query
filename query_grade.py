#!-*-coding:utf-8-*-
import requests

guesses = ({'zkzh': '3705511721{:0>3d}{:0>2d}'.format(a, b), 'xm': 'name'}
           for a in range(300, 330) for b in range(0, 5))
headers = {
    'Referer': 'http://www.chsi.com.cn/cet'
}
for param in guesses:
    rsp = requests.get('http://www.chsi.com.cn/cet/query',
                       params=param, headers=headers)
    if '无法找到对应的分数' not in rsp.text and '请输入验证码' not in rsp.text:
        with open(param['zkzh']+'.html', 'wb') as f:
            f.write(rsp.text.encode('utf-8'))
    else:
        print(param['zkzh'], '尝试失败')
