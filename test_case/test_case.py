import re
import unittest
import ddt
import jsonpath
from common.interfance import *
from common.read_excles import *
import common.functions
import common.new_excle


false = False
null = None
true = True


@ddt.ddt
class Test(unittest.TestCase):
    api_data = common.new_excle.read_excles()

    # 全局变量池
    saves = {}
    # 识别${key}的正则表达式
    EXPR = '\$\{(.*?)\}'

    """
    source:响应值，目标字符串
    key：要匹配的key
    jexpr：匹配key的响应值的正则
    """
    def save_date(self, source, key, jexpr):
        values = jsonpath.jsonpath(source, jexpr)[0]
        self.saves[key] = values
        logger.info("保存 {}=>{} 到全局变量池".format(key, values))

    # 获取接口响应体的返回值，作为参数传到下一个请求中去
    def build_parms(self, string, id):
        keys = re.findall(self.EXPR, string)
        for key in keys:
            value = self.saves.get(key + '-' + id)
            string = string.replace('${' + key + '}', str(value))

            # 遍历所有函数助手并执行，结束后替换
        funcs = re.findall(self.EXPR, string)
        for func in funcs:
            fuc = func.split('__')[1]
            fuc_name = fuc.split("(")[0]
            fuc = fuc.replace(fuc_name, fuc_name.lower())
            value = eval(fuc)
            string = string.replace(func, str(value))
        return string

    def setUp(self):
        print('{}测试开始')


    @classmethod
    def setUpClass(cls):
        # 实例化测试基类，自带cookie保持
        cls.request =  interfance()

    for sheet_date in api_data:
        sheet = sheet_date.get('sheet')
        print(sheet)
        sdata = sheet_date.get('data')
        print(sdata)
        id1 = common.functions.uuid2()
        print(id1)
        exec(F'''
@ddt.data(*sdata)
@ddt.unpack
def test_{sheet}(self, description, url, method, headers, cookies, params, data, verify,saves,code):

        url = self.build_parms(url,"{id1}")
        method = self.build_parms(method,"{id1}")
        headers = self.build_parms(headers,"{id1}")
       
        data = self.build_parms(data,"{id1}")
        
        #print(type(data))
        
        #data = eval(data) if data else data
        
       # url = self.build_parms(self)

        print(url)
        #print(data)

        if method.upper() == 'GET':
            result = self.request.get_request(url=url,description=description, headers=eval(headers), cookies=cookies, params=params)
            if code:
                print(description+':'+ str(result.status_code))

                self.assertEquals(result.status_code, 200, msg='接口请求状态码错误')
            # print(result.json())
            
        elif method.upper() == 'POST':
            result = self.request.post_request(url=url,description=description, headers=eval(headers), cookies=cookies,params=params,data=data.encode('utf-8'))
            if code:
                print(description + ':' + str(result.status_code))
                self.assertEquals(result.status_code, 200, msg='接口请求状态码错误')
            #print(type(result.json()))
            
        elif method.upper() == 'PUT':
            result = self.request.post_request(url=url,description=description, headers=eval(headers), cookies=cookies,params=params,data=data.encode('utf-8'))
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
                self.save_date(result.json(), key+"-"+"{id1}", jsp)

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

                '''
             )

    @classmethod
    def tearDown(self):

        print('tearDown')


if __name__ == "__main__":
    unittest.main()