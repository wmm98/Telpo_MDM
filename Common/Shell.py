"""
封装执行shell语句方法
"""

import subprocess
import time
from Common.Log import MyLog

log = MyLog()


class Shell:
    @staticmethod
    def invoke(cmd, runtime=120):
        try:
            output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE).communicate(
                timeout=runtime)
            o = output.decode("utf-8")
            return o
        except subprocess.TimeoutExpired as e:
            print(str(e))
            err = str(e) + "\n" + "@@@@@@@@@@@@@@@@@@@@@@@@请检查命令！！！"
            log.error(str(err))
            assert False, err

    @staticmethod
    def kill():
        subprocess.Popen(shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).kill()


if __name__ == '__main__':
    send = Shell()
    # proc = send.popen("adb shell \"su\"")
    # proc = send.popen("adb shell \"dmesg\"")
    # proc = send.popen("adb shell \"ls\"")

    send.invoke("adb devices")
    print("这是在调试")
