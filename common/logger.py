import logging
from logging import handlers
import os

curPath = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))

class Logger():
    leval_relation = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    def __init__(self,fileName = '{}/logs/all.log'.format(curPath),when = 'D',leval = 'info',backCount = 3,fmt = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s' ):
        self.logger = logging.getLogger(fileName)#实例化一个logger的filename对象
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.leval_relation.get(leval))#设置日志等级
        stream_handler = logging.StreamHandler()#往屏幕上输出日志
        stream_handler.setFormatter(format_str)#设置屏幕上显示的格式
        file_handler = handlers.TimedRotatingFileHandler(filename=fileName,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        file_handler.setFormatter(format_str)#设置文件上显示的格式
        self.logger.addHandler(stream_handler)#把对象添加到logger上
        self.logger.addHandler(file_handler)
if __name__ == '__main__':
    txt = 'test'
    log = Logger()
    log.logger.info(txt)





