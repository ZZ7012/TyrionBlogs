---
title: DCM
---


• Diagnostic Event Manager (DEM): The DEM module provides function to retrieve all information related to fault memory such that the Dcm module is able to respond to tester requests by reading data from the fault memory. 
• Protocol Data Unit Router (PduR module): The PduR module provides functions to transmit and receive diagnostic data. Proper operation of the Dcm module presumes that the PduR interface supports all service primitives defined for the Service Access Point (SAP) between diagnostic application layer and underlying transport layer (see ISO14229-1 [1], chapter 5 Application layer services). 
• Communication Manager (ComM): The ComM module provides functions such that the Dcm module can indicate the states ”active” and ”inactive” for diagnostic communication. The Dcm module provides functionality to handle the communication requirements ”Full-/ Silent-/ No-Communication”. Additionally, the Dcm module provides the functionality to enable and disable Diagnostic Communication if requested by the ComM module.

SW-C and RTE: The Dcm module has the capability to analyze the received diagnostic request data stream and handles all functionalities related to diagnostic communication such as protocol handling and timing. Based on the analysis of the request data stream the Dcm module assembles the response data stream and delegates routines or IO-Control executions to SW-Cs .If any of the data elements or functional states cannot be provided by the Dcm module itself the Dcm requests data or functional states from SW-Cs via port-interfaces or from other BSW modules through direct function-calls. 
BswM: The Dcm notifies the BswM that the application was updated if the initialization of the Dcm is the consequence of a jump from the bootloader . The Dcm also indicates to the BswM a communication mode change. 
Crypto Service Manager (Csm): The crypto service module provides a wide range of  cryptographic algorithms. The Csm is used for authentication calculation. 
Key Manager (KeyM): The key manager module provides support for certificate handling and APIs to realize authenticated diagnostics via certificates.


##### 85——控制诊断故障码设置服务
让服务端停止或者恢复DTC状态位更新。

1.该服务可设置支持**功能寻址**，可控制单个服务端或者多个服务端的DTC状态位更新
2.该服务是改变ECU功能的服务，要设置在**非默认会话下**模式下执行，当ECU重新回到默认会话模式下时，该服务功能就会恢复到默认，即恢复DTC状态位更新。
3.如果之前已经让服务停止状态位更新，并且没有重新恢复更新，此时客户端再去请求停止，服务端仍应发送肯定响应；如果之前已经让服务端恢复状态位更新或者没有进行服务请求，此时客户端再去请求开启，服务端仍应发送肯定响应。
4.如果客户端发送清除诊断信息服务（14服务），此优先级比停止更新优先级更高，则控制DTC设置不应禁止重置服务端的DTC状态位，所以可以重置DTC状态位。
5.在停止DTC状态位更新之后，恢复DTC状态位更新的方式有：
	在非默认会话下超时，回到默认会话状态下
	 ECU复位，
	 使用85服务恢复DTC状态位的更新


85服务主要使用场景：
1.临时调整系统的某些部件状态，可能会造成服务端检测异常，导致服务端记录DTC，这时可以在调整之前让服务端停止DTC状态位的更新
2.当某个ECU更新程序时，此ECU会在有段时间内停止发送报文，等待程序更新完成才能继续发送报文，而在停止发送报文的这段时间里，与之相关的控制器就会报通信故障，这时我们在更新某个ECU程序之前，就需要事先停止相关控制器DTC状态位的更新。

85 01 
恢复DTC状态位的更新
85 02
停止DTC状态位的更新


否定响应码
0x12 子功能不支持
0x13消息长度错误或者格式无效
0x22条件错误
0x31请求超出范围



##### 22服务
请求一个或者多个两字节DID
服务器可限制oem或者tier1 可同时请求的DID数量。

否定响应码
0x13消息长度错误或者格式无效
0x22条件错误
0x31请求超出范围
	超出一次请求最大数量DID
	 请求的DID不支持
	

##### 2E——通过标识符写入数据

客户端使用2E服务将DataRecord写入服务器，数据由DID标识，可能受保护，也可能不受保护

否定响应码
0x13消息长度错误或者格式无效
0x22条件错误
0x31请求超出范围
	超出一次请求最大数量DID
	 请求的DID不支持
0x72一般编程故障
	服务器在写入内存错误时检测到故障