# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import subprocess
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


adb = resource_path("adb")
autoAPK = resource_path("auto.apk")
dhu = resource_path("desktop-head-unit")


def auto_test():
    print("检查android手机是否连接...")
    output = subprocess.run(adb + " devices", shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
    devices = output.replace("List of devices attached", "").strip("\n").split("\n")
    first_device = devices[0].replace("device", "").strip()
    if len(devices) == 0 or first_device == "":
        print("没有android手机连接到电脑，请确保手机开发者选项开启，并连接手机开启调试，然后重试")
        return
    elif len(devices) > 1:
        print(output)
        print("多台android手机已连接，默认选择第一台 " + first_device)
    print("android 手机已连接")

    print("\n")
    print("检查auto apk是否安装...")
    cmd = adb + " -s " + first_device + " shell pm list packages com.google.android.projection.gearhead"
    print(cmd)
    installed = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True).stdout.decode("utf-8")
    print(installed)
    if "com.google.android.projection.gearhead" not in installed:
        print("auto apk 没有安装，现在安装 auto apk...")
        cmd = adb + " -s " + first_device + " install " + autoAPK
        res = subprocess.run(cmd, shell=True)
        if res.returncode != 0:
            print("安装 auto apk 失败，请手动安装后重试")
            return
    else:
        print("auto apk 已安装")
    cmd = adb + " -s " + first_device + " forward tcp:5277 tcp:5277"
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        print("手机和dhu连接失败，请检查 auto 是否启动音响服务器主机，确保启动后重试")
        return
    else:
        print("手机和dhu连接成功")

    print("\n")
    print("启动dhu...")
    print("如果dhu启动失败，请检查 auto 是否启动音响服务器主机，确保启动后重试")
    res = subprocess.run("chmod +x " + dhu, shell=True)
    if res.returncode != 0:
        print("./desktop-head-unit 不可运行，请手动修改属性后重试")
        return
    res = subprocess.run(dhu, shell=True, stdout=subprocess.PIPE)










if __name__ == '__main__':
    auto_test()

