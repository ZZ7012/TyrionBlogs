---
title: EcuM
---




If a wakeup occurs on a communication channel, the corresponding bus transceiver driver must notify the ECU Manager module by invoking **EcuM_SetWakeupEvent**(see [SWS_EcuM_02826] ) function. Requirements for this notification are described in section 5.2 Peripherals with Wakeup Capability. 
[SWS_EcuM_02479] The ECU Manager module shall execute the Wakeup Validation Protocol upon the EcuM_SetWakeupEvent (see [SWS_EcuM_02826] ) function call according to Interaction of Wakeup Sources and the ECU Manager later in this chapter. (