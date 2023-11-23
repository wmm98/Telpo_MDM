"""
封装log方法

"""

import logging
import os
import time
import allure

"""
2.8 组件之间的关系
（1）日志器（logger）需要通过处理器（handler）将日志信息输出到目标位置，不同的处理器（handler）可以将日志输出到不同的位置。

（2）日志器（logger）可以设置多个处理器（handler）将同一条日志记录输出到不同的位置。

（3）每个处理器（handler）都可以设置自己的过滤器（filter）实现日志过滤，从而只保留感兴趣的日志。

（4）每个处理器（handler）都可以设置自己的格式器（formatter）实现同一条日志以不同的格式输出到不同的地方。

总结以上内容：Logger 可以包含一个或多个 Handler 和 Filter，即：LoggerFilter，即：Logger 与 Handler 
或 Fitler 是一对多的关系；一个 Logger 实例可以新增多个 Handler，一个 Handler 可以新增多个格式化器或多个过滤器，而且日志级别将会继承。

"""

log_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 设置日志级别为 INFO
logging.basicConfig(level=logging.INFO)


# 定义一个自定义过滤器，忽略系统级别 `warning` 和 `error` 信息
class CustomFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != logging.WARNING


# 创建一个名为 `allure` 的 Logger 对象
logger = logging.getLogger()


# 定义一个过滤器
# class WarningFilter(logging.Filter):
#     def filter(self, record):
#         return record.levelno > logging.WARNING
#
#
# # 创建一个新的日志处理器，将过滤器应用到该处理器上
# # filtered_handler = logging.StreamHandler()
# # filtered_handler.addFilter(WarningFilter())
#
# LEVELS = {
#     'debug': logging.DEBUG,
#     'info': logging.INFO,
#     'warning': logging.WARNING,
#     'error': logging.ERROR,
#     'critical': logging.CRITICAL
# }
# level = 'error'
#
# logger = logging.getLogger()
# logger.setLevel(LEVELS.get(level, logging.NOTSET))
#
# # logger.setLevel(logging.ERROR)
#
# # 设置所有日志记录器的最低级别为 DEBUG
# logging.basicConfig(level=logging.INFO)
# logger.addFilter(WarningFilter())

# logger = logging.getLogger()


# level = 'default'
# level = 'info'


# 获取默认的日志记录器，将新的处理器添加到记录器中
# root_logger = logging.getLogger()
# logger.addHandler(filtered_handler)


# r ：只读
# r+ : 读写
# w ： 新建（会对原有文件进行覆盖）
# a ： 追加
# b ： 二进制文件
def create_file(filename):
    # filename D:\GNP\GNP_StablilityTest/Log/log.log    D:\GNP\GNP_StablilityTest/Log/err.log
    # path D:\GNP\GNP_StablilityTest/Log
    path = filename[0:filename.rfind('/')]
    # 判断是否为文件夹
    if not os.path.isdir(path):
        os.makedirs(path)
    # 判读是否为文件
    elif not os.path.isfile(filename):
        fd = open(filename, mode='w', encoding='utf-8')
        fd.close()
    elif 'err.log' in filename:
        os.rename(filename, path + '/err' + time.strftime("%Y-%m-%d_%H_%M_%S") + '.log')
        fd = open(filename, mode='w', encoding='utf-8')
        fd.close()
    elif 'log.log' in filename:
        os.rename(filename, path + '/log' + time.strftime("%Y-%m-%d_%H_%M_%S") + '.log')
        fd = open(filename, mode='w', encoding='utf-8')
        fd.close()


"""orginal code"""


def set_handler(levels):
    if levels == 'error':
        logger.addHandler(MyLog.err_handler)
    logger.addHandler(MyLog.handler)


def remove_handler(levels):
    if levels == 'error':
        logger.removeHandler(MyLog.err_handler)
    logger.removeHandler(MyLog.handler)


def get_current_time():
    return time.strftime(MyLog.date, time.localtime(time.time()))


class MyLog:
    # 返回上级目录
    # path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print(path)
    # D:\GNP\GNP_StablilityTest

    # log的目录，日志目录
    log_file = log_path + '/Log/log.log'
    # print(log_file)
    err_file = log_path + '/Log/err.log'
    # ?
    # logger.setLevel(LEVELS.get(level, logging.NOTSET))

    # 将自定义的过滤器添加到日志记录器中

    create_file(log_file)
    create_file(err_file)
    date = '%Y-%m-%d %H:%M:%S'

    handler = logging.FileHandler(log_file, encoding='utf-8')
    err_handler = logging.FileHandler(err_file, encoding='utf-8')

    @staticmethod
    def debug(log_meg):
        set_handler('debug')
        logger.debug("[DEBUG " + get_current_time() + "]" + log_meg)
        remove_handler('debug')

    @staticmethod
    def info(log_meg):
        set_handler('info')
        logger.info("[INFO " + get_current_time() + "]" + log_meg)
        remove_handler('info')

    @staticmethod
    def warning(log_meg):
        set_handler('warning')
        logger.warning("[WARNING " + get_current_time() + "]" + log_meg)
        remove_handler('warning')

    @staticmethod
    def error(log_meg):
        set_handler('error')
        logger.error("[ERROR " + get_current_time() + "]" + log_meg)
        remove_handler('error')

    @staticmethod
    def critical(log_meg):
        set_handler('critical')
        logger.error("[CRITICAL " + get_current_time() + "]" + log_meg)
        remove_handler('critical')


# def create_textFile(filename):
#     # filename D:\GNP\GNP_StablilityTest/Log/log.log    D:\GNP\GNP_StablilityTest/Log/err.log
#     # path D:\GNP\GNP_StablilityTest/Log
#     path = filename[0:filename.rfind('/')]
#     # 判断是否为文件夹
#     if not os.path.isdir(path):
#         os.makedirs(path)
#     # 判读是否为文件
#     elif not os.path.isfile(filename):
#         fd = open(filename, mode='w', encoding='utf-8')
#         # fd.close()
#     elif 'output.txt' in filename:
#         os.rename(filename, path + '/output' + time.strftime("%Y-%m-%d_%H_%M_%S") + '.txt')
#         fd = open(filename, mode='w', encoding='utf-8')
#         # fd.close()


# class OutPutText():
#     # 返回上级目录
#     # path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     # log的目录，日志目录
#     filename = log_path + '/CatchLogs/output.txt'
#     # filename D:\GNP\GNP_StablilityTest/Log/log.log    D:\GNP\GNP_StablilityTest/Log/err.log
#     # path D:\GNP\GNP_StablilityTest/Log
#     path = filename[0:filename.rfind('/')]
#     # 判断是否为文件夹
#     if not os.path.isdir(path):
#         os.makedirs(path)
#     # 判读是否为文件
#     elif not os.path.isfile(filename):
#         fd = open(filename, mode='w', encoding='utf-8')
#         fd.close()
#     elif 'output.txt' in filename:
#         os.rename(filename, path + '/output' + time.strftime("%Y-%m-%d_%H_%M_%S") + '.txt')
#         fd = open(filename, mode='w', encoding='utf-8')
#         fd.close()
#
#     @staticmethod
#     def write_text(msg):
#         # ("[WARNING " + get_current_time() + "]" + log_meg)
#         date = '%Y-%m-%d %H:%M:%S'
#         filename = log_path + '/CatchLogs/output.txt'
#         f = open(filename, 'a+', encoding='utf-8')
#         f.write(msg + '\n')
#         f.close()


if __name__ == "__main__":
    MyLog.debug("This is debug message")
    MyLog.info("This is info message")
    MyLog.warning("This is warning message")
    MyLog.error("This is error")
    MyLog.critical("This is critical message")
    # MyLog()

    # output = OutPutText()
    # output.write_text("这是什么\n")
    # output.write_text("这是在调试11111")
