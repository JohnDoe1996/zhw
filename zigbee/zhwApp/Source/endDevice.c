#include "smartHome.h"
#include "sapi.h"
#include "hal_led.h"
#include "hal_uart.h"

#define ID 0x01  // ���ڵ�num

#define L P0_5  // �ӵ�����

#define NUM  1  // �����ڵ㳤��Ϊ1
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
ִ��ʱ�������͵����ݰ������շ��յ�ʱ������
handle:���ı�ţ�
status:ZSUCCESS��ʾ�ɹ�����
************/
void zb_SendDataConfirm( uint8 handle, uint8 status )
{
  
}

/***********
ִ��ʱ�������յ������ݰ�������
************/
void zb_ReceiveDataIndication( uint16 source, uint16 command, 
                              uint16 len, uint8 *pData  )
{
  if(command==TOGGLE_CMD_ID) // ���ܵ�Э�����������ź�
  {
    //zb_SendDataRequest(0X0,MSG_CMD_ID,6,pData,
    //                  0,FALSE,AF_DEFAULT_RADIUS);
    if(pData[0]==0xcf && pData[1]==0x03 && pData[2]==0x10 && pData[3]==ID && pData[5]==0xfc)  // �ж�Э��ʦ������Ҫ��
    {
     //TODO
      uint8 s = 0x00;
      if(pData[4]==0x01)
      {
        s = 0x01; //���ųɹ���������
        L = 1; // ����
        osal_start_timerEx(sapi_TaskID,SEND_TIMER_EVT,1500);  //���ö�ʱ��1.5s��λ
      }
      sendCon(s); // ���ڷ���
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
    //�ɰѽڵ����������õ�����ID�ŷ��͹�ȥ
    zb_SendDataRequest(0X0,JOINNET_CMD_ID,NUM,
                      IdList,0,FALSE,AF_DEFAULT_RADIUS);
    osal_start_timerEx(sapi_TaskID,TIMER_TIMEOUT_EVT,2000); // ��ʱ��������2s
  }
}

void zb_HandleOsalEvent( uint16 event )
{
  if(event&TIMER_TIMEOUT_EVT) 
  {
    osal_start_timerEx(sapi_TaskID,TIMER_TIMEOUT_EVT,2000);  //���¶�ʱ������
    zb_SendDataRequest(0X0,HEART_BEAT_CMD_ID,
                       0,NULL,0,FALSE,AF_DEFAULT_RADIUS);   // ����������
  }
  if(event&SEND_TIMER_EVT) //��ʱ�����źź�λ�ź�
  {
    L = 0;
  }
}

void zb_FindDeviceConfirm( uint8 searchType, 
                          uint8 *searchKey, uint8 *result )
{
  
}

void sendCon(uint8 s)  // ��������
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

void IOInit(void)  // ��ʼ������
{
  P0SEL &=~ 0x20;
  P0DIR |= 0x20;
  L = 0;
}