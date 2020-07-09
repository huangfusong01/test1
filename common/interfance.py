import requests
from common.logger import Logger
from json import dumps,loads

logger = Logger().logger

class interfance(requests.Session):

    def get_request(self,url,headers,params,cookies,description):
        '''

        :param ulr: 请求地址
        :param headers: 请求头
        :param pararms: 请求参数（请求体）
        :param cookie:
        :return:
        '''
        #print(description)
        try:
            result = self.request('GET',url=url,headers=headers,params=params,cookies=cookies)
            self.api_log(method='get',url=url,description=description, headers=headers, params=params, cookies=cookies,
                         code=result.status_code, res_text=result.text, res_header=result.headers)
            return result
        except Exception as e:
            raise e

    def post_request(self,description,url,headers,params,data,cookies):
        '''
        :param url 请求地址
        :param headers: 请求头
        :param data:请求体
        :param cookie:
        :return:
        '''
        #print(description)
        try:
            result = self.request('POST',url=url,headers=headers,params=params,data=data,cookies=cookies)
            self.api_log('post',url=url,description=description,headers=headers,params=params,cookies=cookies,
                     code=result.status_code,res_text=result.text,res_header=result.headers,data=data)
            return result
        except Exception as e:
            raise e

    def put_request(self,description,url,headers,params,data,cookies):
        '''
        :param ulr: 请求地址
        :param headers: 请求头
        :param pararms: 请求参数（请求体）
        :param cookie:
        :return:
        '''
        #print(description)

        try:
            result = self.request('PUT',url=url,headers=headers,params=params,data=data,cookies=cookies)
            self.api_log(method='put',url=url,description=description, headers=headers, params=params, cookies=cookies,
                         code=result.status_code, res_text=result.text, res_header=result.headers,data=data)

            return result
        except Exception as e:
            raise e

    def assertEquals(self,actual,expected):

        '''
        断言是否相等
        :param actual: 实际值
        :param expected: 期望值
        :return:
        '''
        try:
            assert actual == expected
            logger.info('断言成功,实际值:{} 等于预期值:{}'.format(actual,expected))

        except AssertionError as e:
            logger.info('断言失败,实际值:{} 不等于预期值:{}'.format(actual,expected))
            raise e

    def assertIn(self,content,target):

        '''
        断言目标文本是否包含文本
        :param content:包含文本
        :param target:目标文本
        :return:
        '''
        try:
            assert content in target
            logger.info('断言成功,目标文本:{} 包含 文本：{}'.format(target,content))

        except AssertionError as e:
            logger.info('断言失败,目标文本:{} 不包含 文本：{}'.format(target,content))
            raise e

    def assertTrue(self,actual):
        '''
        断言是否为真
        :param actual: 实际值
        :return:
        '''
        try:
            assert actual == True
            logger.info('断言成功，实际值 {} 为真'.format(actual))
        except Exception as e:
            logger.info('断言失败，实际值 {} 不为真'.format(actual))


    def api_log(self,method=None,url=None,description=None,headers=None,params=None,json=None,cookies=None,code=None,res_text=None,res_header=None,data=None):
        logger.info("请求描述====>{}".format(description))
        logger.info("请求方式====>{}".format(method))
        logger.info("请求地址====>{}".format(url))
        logger.info("请求报文====>{}".format(data))
        logger.info("请求头====>{}".format(dumps(headers,indent=4)))
        logger.info("请求参数====>{}".format(dumps(params,indent=4)))
        logger.info("请求体====>{}".format(dumps(json,indent=4)))
        logger.info("Cookies====>{}".format(dumps(cookies,indent=4)))
        logger.info("接口响应状态码====>{}".format(code))
        logger.info("接口响应头为====>{}".format(res_header))
        logger.info("接口响应体为====>{}".format(res_text))

