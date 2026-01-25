
CAN state manager  

管理的为总线通信状态，包括能不能发送报文 能不能接受报文 总线上有没有错

由上而下，CanSM接收其他模块的总线状态切换请求并通知CanIf模块去执行
由下而上，CanSM接收CanIf模块的总线状态切换反馈并汇报给其他模块


CanSM功能介绍
	CanSM提供的主要功能主要有：  
	1. 总线模式切换  
	2. Busoff 恢复管理  
	3. 切换波特率  
	4. 唤醒确认管理


2.2 Busoff 恢复机制
  除了上面所说的总线状态机，CanSM模块还有另外一个小型状态机，那就是用来实现的Busoff 恢复机制。

  当CanSM模块从CanIf模块收到 Busoff 通知时，将会进入 Busoff 恢复的状态，恢复机制如下：
		快恢复，产生 Busoff 后，延时 CanSMBorTimeL1 时间尝试恢复；
		快恢复次数达到 CanSMBorCounterL1ToL2 后，进行慢恢复；
		慢恢复，产生 Busoff 后，延时 CanSMBorTimeL2 时间尝试恢复；
		慢恢复次数为无限次。


2.3 切换波特率
   CanSM模块提供接口CanSM_ChangeBaudrate可以切换CAN总线通信波特率，但是只有在FULLCOM状态且没有Busoff 时才能调用CanSM_ChangeBaudrate，其他状态调用 CanSM_ChangeBaudrate 会被拒绝。


2.4 唤醒确认功能
   当系统进入休眠后，CAN 控制器也进入休眠状态。当发生 CAN 通道唤醒事件时，EcuM 会 调 用 CanSM模块的CanSM_StartWakeupSource() 函 数 ，CanSM状态机会由NOCOM状态进入CANSM_BSM_WUVALIDATION状态，将硬件状态设置为正常工作态。此时硬件可以接收到网络上的报文，CanIf 模块会判断该唤醒帧是否合法。若判断结果为合法， ComM 会 调 用 CanSM 模 块 的CanSM_RequestComMode()接口请求 CanSM 进入 FULLCOM 模式， 若结果为非法，则 EcuM 会调用 CanSM 模块的CanSM_StopWakeupSource()函数，由CanSM将硬件重新设置为休眠状态。


参考链接：
https://blog.csdn.net/Oushuwen/article/details/128922097