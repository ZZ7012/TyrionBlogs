常见的网络管理是不带PNC的，只是做整个NM的休眠唤醒作用

CanNm 报文中的byte0 和byte1 由CanIF给到CanNM

User data部分信息通过 PduR 路由到 Com；如果携带PNC信息 则有Com层调用com_sendsignal接口给到ComM层；ComM 拿到PNC信息之后进行状态机的切换；


[SWS_CanNm_00107] If CanNmNodeDetectionEnabled is set to TRUE CanNm shall clear the Repeat Message Bit when leaving the Repeat Message State.

何时会CanNm报文会快发？

**CanNmNodeDetectionEnabled** = TRUE时，节点在NOS（Normal Operation State）或者RSS（Ready Sleep State）状态下，内部请求进入RMS（Repeat Message State）状态时，节点外发网络管理报文会置位**RMR Bit**，请求网段内的其他节点也进入RMS状态，协调节点网络状态。

标准文档原文：
If CanNmNodeDetectionEnabled is set to TRUE and Repeat Message Request Bit is received in the Normal Operation State, the CanNm module shall enter the Repeat Message State.c(RS_Nm_00153, RS_Nm_02549)

If CanNmNodeDetectionEnabled is set to TRUE and function CanNm_RepeatMessageRequest is called in the Normal Operation State, the CanNm module shall enter the Repeat Message State.

If CanNmNodeDetectionEnabled is set to TRUE and function CanNm_RepeatMessageRequest is called in the Normal Operation State the CanNm module shall set the Repeat Message Bit.

**被动唤醒时会快发嘛？**
答：不会快发 

被动唤醒调用的接口是CanNm_PassiveStartup()
主动唤醒调用的接口是CanNm_NetworkRequest()
标准文档原文
When entering the Repeat Message State from Bus Sleep Mode or Prepare Bus Sleep Mode because of CanNm_NetworkRequest() (active wakeup) and if ***CanNmImmediateNmTransmissions*** is greater zero, the NM PDUs shall be transmitted using CanNmImmediateNmCycleTime as cycle time. The transmission of the first NM PDU shall be triggered as soon as possible. 

什么是被动唤醒？收到网络报文 或者应用报文才能被唤醒？

**如果是被动唤醒，且收到了 Repeat Message Bit 置位 会不会快发？**

会快发!!!
SWS_CanNm_00014] dIf CanNmRepeatMsgIndEnabled is set to TRUE and the Repeat Message Request bit is received CanNm module shall call the callout function Nm_RepeatMessageIndication only the first time until Repeat Message State has been left again. In case the Partial Network Learning Bit is also received with value 1 and CanNmDynamicPncToChannelMappingEnabled is set to TRUE the parameter pnLearningBitSet shall be set to TRUE in this function call, otherwise to FALSE.c (RS_Nm_00153) Note: When Repeat Message Bit is received NM will enter or restart Repeat Message State, but the bits will still be received as requestor will send until he leaves Repeat Message State to be fault-tolerant regarding possible loss of messages. State Change and callout are only needed once the first time the node received it.

**主动唤醒时会快发嘛？**
答：会快发 

标准文档原文
When entering the Repeat Message State from Bus Sleep Mode or Prepare Bus Sleep Mode because of CanNm_NetworkRequest() (active wakeup) and if ***CanNmImmediateNmTransmissions*** is greater zero, the NM PDUs shall be transmitted using CanNmImmediateNmCycleTime as cycle time. The transmission of the first NM PDU shall be triggered as soon as possible. 


**是否快发总结！！！**

是否为主动唤醒？
是主动唤醒，承担唤醒网络的角色 需要快速唤醒同网段的其他节点

是被动唤醒，是否收到repeat message bit 置位  置位需要进快发模式

其他情况下 调用回到repeat message state 的接口，进入快发。



什么是主动唤醒？ KL15 点火信号 上电 或者定时器到了 自己唤醒自己。

当节点被动唤醒，由BSM（Bus-Sleep Mode）/PBSM（Prepare Bus-Sleep Mode）进入RMS状态时，发送的网络管理报文，RMR Bit不置位。

For nodes that are not in passive mode (refer to subsection 7.9.3) the Repeat Message State ensures, that any transition from Bus-Sleep or Prepare Bus-Sleep to the Network Mode becomes visible to the other nodes on the network. Additionally, it ensures that any node stays active for a minimum amount of time. It can be used for detection of present nodes.



如果设置的NM Variant为Full，ComM 在请求full communication时 ComM还会调用CanNm_NetworkRequest接口，CanNm状态将由Bus Sleep状态迁移到Network Mode。再然后，CanNm调用ComM_Nm_NetworkMode()接口，通知ComM网络管理状态已经进入Network Mode