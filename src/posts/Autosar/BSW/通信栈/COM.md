---
title: COM
---

signal gateway 

ipdu callout  

UB

signal group


### TxMode Direct and Periodic

事件报文需要配置为Direct
周期型报文需要配置为Periodic

周期型报文每个周期就会固定发送报文

事件型报文是当有com_sendsignal()触发时才会发送报文


