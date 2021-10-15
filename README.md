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

低调使用。

# Todo List
- [x] 基本功能（指发送`青年大学习`获取答案）
- [x] 异步
- [ ] 检测到更新后自动推送


# 日志
2021/10/13  代码完成，大概能用了。  
2021/10/15  网络请求改为异步，防止阻塞bot主进程。  
