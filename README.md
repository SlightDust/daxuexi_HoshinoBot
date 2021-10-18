# daxuexi_HoshinoBot
一个适用于HoshinoBot的青年大学习答案获取插件

# 安装和使用方法：
和一般hoshino插件一样  

1. 在hoshino/modules下clone本仓库`git clone https://github.com/SlightDust/daxuexi_HoshinoBot.git`  
2. 在hoshino/config/\_\_bot\_\_.py中加入
```
MODULES_ON = {
...
'daxuexi_HoshinoBot',  # 青年大学习
}
```
3. 重启hoshino

群内发送`青年大学习`即可获取最新一期青年大学习答案。  
群内发送`启用 青年大学习推送`可开启自动推送功能，检测到青年大学习更新后将第一时间向群内推送通知。  

低调使用。

# Todo List
- [x] 基本功能（指发送`青年大学习`获取答案）
- [x] 异步
- [x] 检测到更新后自动推送


# 日志
2021/10/13  代码完成，大概能用了。  
2021/10/15  网络请求改为异步，防止阻塞bot主进程。  
2021/10/17  检测到更新时自动推送，推送功能默认关闭，需要群内发送`启用 青年大学习推送`来开启  
2021/10/18  修复不能获取答案的问题~~工作人员看到这个插件连夜修改了网页结构~~，现在的最新版可以获取答案了  