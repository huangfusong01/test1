import re
import unittest
import ddt
import jsonpath
from common.interfance import *
from common.read_excles import *
import json

false = False
null = None
true = True


@ddt.ddt
class Test(unittest.TestCase):
    EXPR = '\$\{(.*?)\}'
    save = {}
    api_data = read_excles()

    def save_date(self,source,key,jexpr):
        values = jsonpath.jsonpath(source,jexpr)[0]
        self.save[key] = values
        logger.info("保存 {}=>{} 到全局变量池".format(key,values))
        print(self.save)


    #获取接口响应体的返回值，作为参数传到下一个请求中去
    def build_parms(self,string):
        keys = re.findall(self.EXPR,string)
        for key in keys:
            value = self.save.get(key)
            string = string.replace('${' + key + '}', str(value))
        return string

    def setUp(self):
        cookies = None
        print('{}测试开始')

    @classmethod
    def setUpClass(cls):
        # 实例化测试基类，自带cookie保持
        cls.request = interfance()


    @ddt.data(*api_data)
    @ddt.unpack
    def test_interfance(self, description, url, method, headers, cookies, params, data, verify,saves,code):

        data = self.build_parms(data)
       # url = self.build_parms(self)

        print(url)
        #print(data)

        if method.upper() == 'GET':
            result = self.request.get_request(url=url,description=description, headers=eval(headers), cookies=cookies, params=params)
            if code:
                print(description+':'+ str(result.status_code))

                self.assertEqual(result.status_code, 200, msg='接口请求状态码错误')
            # print(result.json())
        elif method.upper() == 'POST':
            dat = json.loads(data)
            print(type(dat))
            print(type(headers))
            result = self.request.post_request(url=url,description=description, headers=eval(headers), cookies=cookies, params=params,data=data.encode('utf-8'))
            if code:
                print(description + ':' + str(result.status_code))
                self.assertEqual(result.status_code, 200, msg='接口请求状态码错误')
            #print(type(result.json()))
        elif method.upper() == 'PUT':
            result = self.request.put_request(url=url, description=description, headers=eval(headers), cookies=cookies,
                                               params=params, data=data.encode('utf-8'))
            print(data)
            if code:
                print(description + ':' + str(result.status_code))
                self.assertEquals(result.status_code, 200, msg='接口请求状态码错误')
        else:
            pass

        if saves:

            for save in saves.split(";"):
                print(save)
                key = save.split("=")[0]
                jsp = save.split("=")[1]
                self.save_date(result.json(), key, jsp)

        if verify:
            # 遍历verify:
            list_ver = []
            list_valus = []
            for ver in verify.split(";"):
                #print(ver)
                dict_eval = eval(ver)
                #print(type(dict_eval))
                for ver_keys, ver_values in dict_eval.items():
                    list_ver.append(ver_keys)
                    list_valus.append(ver_values)
                actual = jsonpath.jsonpath(result.json(), list_ver[0])[0]
                #print(actual)
                expect = list_valus[0]
                #print(expect)
                self.request.assertEquals(expect, actual)



    @classmethod
    def tearDown(self):
        print('tearDown')


if __name__ == "__main__":
    unittest.main()
    print(save)