#include "smartHome.h"
#include "sapi.h"
#include "hal_led.h"
#include "hal_uart.h"

#define ID 0x01  // 本节点num

#define L P0_5  // 接的引脚

#define NUM  1  // 包含节点长度为1
uint8 IdList[NUM]={ID};

#define NUM_IN_CMD_SDEVICE 1
#define NUM_OUT_CMD_SDEVICE 3

void sendCon(uint8 s);
void IOInit(void);

const cId_t DeviceInputCommandList[NUM_IN_CMD_SDEVICE]=
                                {TOGGLE_CMD_ID};
const cId_t DeviceOutputCommandList[NUM_OUT_CMD_SDEVICE]=
                                {JOINNET_CMD_ID,HEART_BEAT_CMD_ID,MSG_CMD_ID};
const SimpleDescriptionFormat_t zb_SimpleDesc=
{
  ENDPOINT_ID_SMARTHOME,
  PROFILE_ID_SMARTHOME,
  DEVICE_ID_SDEVICE,
  DEVIDE_VERSION_ID,
  0,
  NUM_IN_CMD_SDEVICE,
  (cId_t*)DeviceInputCommandList,
  NUM_OUT_CMD_SDEVICE,
  (cId_t*)DeviceOutputCommandList  
};
/***********
执行时机：发送的数据包被接收方收到时被调用
handle:包的编号；
status:ZSUCCESS表示成功接收
************/
void zb_SendDataConfirm( uint8 handle, uint8 status )
{
  
}

/***********
执行时机：接收到的数据包被调用
************/
void zb_ReceiveDataIndication( uint16 source, uint16 command, 
                              uint16 len, uint8 *pData  )
{
  if(command==TOGGLE_CMD_ID) // 接受到协调器发来的信号
  {
    //zb_SendDataRequest(0X0,MSG_CMD_ID,6,pData,
    //                  0,FALSE,AF_DEFAULT_RADIUS);
    if(pData[0]==0xcf && pData[1]==0x03 && pData[2]==0x10 && pData[3]==ID && pData[5]==0xfc)  // 判断协议师傅符合要求
    {
     //TODO
      uint8 s = 0x00;
      if(pData[4]==0x01)
      {
        s = 0x01; //开门成功返回数据
        L = 1; // 开门
        osal_start_timerEx(sapi_TaskID,SEND_TIMER_EVT,1500);  //设置定时器1.5s后复位
      }
      sendCon(s); // 串口发送
    }
  }
}


void zb_AllowBindConfirm( uint16 source )
{
}

void zb_HandleKeys( uint8 shift, uint8 keys )
{
  
}

void zb_BindConfirm( uint16 commandId, uint8 status )
{
}


//void zb_SendDataRequest ( uint16 destination, uint16 commandId, uint8 len,
//                          uint8 *pData, uint8 handle, uint8 ack, uint8 radius );
void zb_StartConfirm( uint8 status )
{
  if(status==ZSUCCESS)
  {
    IOInit();
    //可把节点所包含的用电器的ID号发送过去
    zb_SendDataRequest(0X0,JOINNET_CMD_ID,NUM,
                      IdList,0,FALSE,AF_DEFAULT_RADIUS);
    osal_start_timerEx(sapi_TaskID,TIMER_TIMEOUT_EVT,2000); // 定时心跳包，2s
  }
}

void zb_HandleOsalEvent( uint16 event )
{
  if(event&TIMER_TIMEOUT_EVT) 
  {
    osal_start_timerEx(sapi_TaskID,TIMER_TIMEOUT_EVT,2000);  //重新定时心跳包
    zb_SendDataRequest(0X0,HEART_BEAT_CMD_ID,
                       0,NULL,0,FALSE,AF_DEFAULT_RADIUS);   // 发送心跳包
  }
  if(event&SEND_TIMER_EVT) //定时开启信号后复位信号
  {
    L = 0;
  }
}

void zb_FindDeviceConfirm( uint8 searchType, 
                          uint8 *searchKey, uint8 *result )
{
  
}

void sendCon(uint8 s)  // 发送数据
{ 
  uint8 tmpData[6];
  tmpData[0] = 0xcf;
  tmpData[1] = 0x03;
  tmpData[2] = 0x20;
  tmpData[3] = ID;
  tmpData[4] = s;
  tmpData[5] = 0xfc;
  zb_SendDataRequest(0X0,MSG_CMD_ID,6,tmpData,
                      0,FALSE,AF_DEFAULT_RADIUS);
}

void IOInit(void)  // 初始化引脚
{
  P0SEL &=~ 0x20;
  P0DIR |= 0x20;
  L = 0;
}