# daxuexi_HoshinoBot
一个适用于HoshinoBot的青年大学习答案获取插件

# 安装方法：
和一般hoshino插件一样  

1. 在hoshino/modules下clone本仓库`clone https://github.com/SlightDust/daxuexi_HoshinoBot.git`  
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

# 已知问题
没有使用异步，网络较差时可能阻塞其他进程。  
人比较菜，等我研究一下异步……