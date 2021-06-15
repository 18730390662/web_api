# coding=utf-8
import sys
import os
import configparser
base_path = os.getcwd()

sys.path.append(base_path)
import requests


import json
from Utils.handle_init import handle_ini
from Utils.handle_cookie import write_cookiess_value



class BaseRequest():
    def send_post(self, url, param, header,cookie=None,get_cookie=None):
        response = requests.post(url, data=json.dumps(param),headers=header,cookies=cookie)
        if get_cookie != None:
            cookie_value_jar = response.cookies
            cookie_value = requests.utils.dict_from_cookiejar(cookie_value_jar)
            write_cookiess_value(cookie_value, get_cookie['is_cookie'])

        res = response.text
        return res

    def send_get(self, url, data, header=None,cookie=None, get_cookie=None):
        '''
        发视get请求
        '''
        response = requests.get(url=url, params=data, cookies=cookie, headers=header)
        if get_cookie != None:
            cookie_value_jar = response.cookies
            cookie_value = requests.utils.dict_from_cookiejar(cookie_value_jar)



            write_cookiess_value(cookie_value, get_cookie['is_cookie'])


        res = response.text
        return res




    def run_main(self, method, url, data,header=None,cookie=None,get_cookie=None):
        base_url = handle_ini.get_value('host')
        if 'http' not in url:
            url = base_url + url
            print("这是URL",url)
        if method=="post":
            res=self.send_post(url,data,header,cookie,get_cookie)
        else:
            res=self.send_get(url,data,header,cookie,get_cookie)
        try:
            res = json.loads(res)
        except:
            print("这个结果是一个text")
        print("--->", res)
        return res
request = BaseRequest()

if __name__ == '__main__':
    url = 'http://127.0.0.1:8000/login1'
    data = {"key": "zhangdy0", "password": "123456"}

    get_cookie = {"is_cookie": "app"}
    res = request.run_main(method='get', url=url, data=data, get_cookie="write")






# 代码思路
# 首先导入模块不说了
# 封装一个get接口和一个post接口
# 大家可能看不懂的是get_cooke这个参数，这个参数在下边的main中没有调用，是用于后期操作cookie回写的参数，后边会阐明，
# 在写一个run_main方法，用于调用时判断是调用封装好的哪一个接口，以及一个url的处理，url是传入的参数，如果没有传入host，就将host与url做一个拼接，如果传入一个完整的url，就不需要进行处理，直接使用即可，最后直接实例化一个对象request，一个简单的单例模式，用于其他模块的调用
#
# 总体分两步
# 1、封装requests接口
# 2、写一个调用接口的主函数
#
# 这些代码咱们还要改进，例如host这里就要写活，所以，需要写一些配置文件
