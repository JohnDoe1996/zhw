#include "smartHome.h"
#include "sapi.h"

#include "osal.h"
#include "hal_uart.h"
#include "stdio.h"
#define NUM_IN_CMD_COORINATOR 3
#define NUM_OUT_CMD_COORINATOR 1
void *alloceDeviceNode(uint8 num);
void uart_receive(uint8 port,uint8 event);
const cId_t coordinatorInputCommandList[NUM_IN_CMD_COORINATOR]=
                                {JOINNET_CMD_ID,HEART_BEAT_CMD_ID,MSG_CMD_ID};
const cId_t coordinatorOutputCommandList[NUM_OUT_CMD_COORINATOR]=
                                {TOGGLE_CMD_ID};
struct device_node
{
  struct device_node *next;
  uint8 shortAddr[2];
  uint8 lostHeartCount;
  uint8 Num; 
  uint8 Id[1];
};

static struct device_node DeviceHeader={NULL};

void *alloceDeviceNode(uint8 num)
{
  return osal_mem_alloc(sizeof(struct device_node)-1+num);
}

const SimpleDescriptionFormat_t zb_SimpleDesc=
{
  ENDPOINT_ID_SMARTHOME,
  PROFILE_ID_SMARTHOME,
  DEVICE_ID_COORDINATOR,
  DEVIDE_VERSION_ID,
  0,
  NUM_IN_CMD_COORINATOR,
  (cId_t*)coordinatorInputCommandList,
  NUM_OUT_CMD_COORINATOR,
  (cId_t*)coordinatorOutputCommandList  
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
ִ��ʱ�������յ����ݰ�ʱ������
************/
void zb_ReceiveDataIndication( uint16 source, uint16 command, 
                              uint16 len, uint8 *pData  )
{

  if(command==MSG_CMD_ID) // ���յ��ն˽ڵ㴫��������
  {
    HalUARTWrite(0,pData,len); // ����ֱ�Ӵ�������
  }
  if(command==JOINNET_CMD_ID)   // �ڵ����
  {
    //int i;
    struct device_node *p=DeviceHeader.next;  //�½�һ���ڵ�ṹ��
    while(p!=NULL)
    {
      if( osal_memcmp(pData,p->Id,len)==TRUE)
        break;
      else
      {
        p=p->next;
      }
    }
    if(p==NULL)//�½ڵ����
    {
      struct device_node *np=(struct device_node *)alloceDeviceNode(len);
      osal_memcpy(np->shortAddr,&source,2);
      np->Num=len;
      osal_memcpy(np->Id,pData,len); 
      np->next=DeviceHeader.next;//ͷ��
      DeviceHeader.next=np;
      p=np;
    } 
    else
    {
      osal_memcpy(p->shortAddr,&source,2);
    }
    uint8 buf[6]={0xcf,0x03,0x00,0x00,0x00,0x00};
    // sprintf(buf,"Led device come on!,shortAddr=%u,ledId:",(uint16)p->shortAddr);
    buf[2] = 0x11;
    buf[3] = p->Id[0];
    buf[5] = 0xfc;
    HalUARTWrite(0,buf,6);  // �ڵ������Ϣ���͵�����

  }
  else if(command==HEART_BEAT_CMD_ID)  // ��������Ϣ
  {
    struct device_node *p=DeviceHeader.next;
    while(p!=NULL)
    {
      if( osal_memcmp(&source,p->shortAddr,2)==TRUE)
        break;
      else
      {
        p=p->next;
      }
    } 
    if(p!=NULL)
    {
      p->lostHeartCount=HEART_BEAT_MAX_COUNT;
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


void zb_StartConfirm( uint8 status )
{
  halUARTCfg_t uartcfg;
  uartcfg.baudRate=HAL_UART_BR_115200;
  uartcfg.flowControl=FALSE;
  uartcfg.callBackFunc=uart_receive;
  HalUARTOpen(0,&uartcfg);
  if(status==ZSUCCESS)  // �����ɹ�
  {
    uint8 buf[6]={0xcf,0x03,0x00,0x00,0x00,0xfc};
    HalUARTWrite(0,buf,6);  // �����ɹ���Ϣ���͵�����
    osal_start_timerEx(sapi_TaskID,TIMER_TIMEOUT_EVT,2000);  //���ö�ʱ2�룬����һ������������ 
  }  
}

void zb_HandleOsalEvent( uint16 event )
{
  if(event&TIMER_TIMEOUT_EVT)
  {
    struct device_node *p=DeviceHeader.next;
    struct device_node *pre=DeviceHeader.next;
    osal_start_timerEx(sapi_TaskID,TIMER_TIMEOUT_EVT,2000); // �������ö�ʱ��
    while(p!=NULL)
    {
      p->lostHeartCount--;
      if(p->lostHeartCount<=0) // ����нڵ�����
      {
        uint8 buf[6] = {0xcf,0x03,0x00,0x00,0x00,0x00};
        struct device_node *pTmp=p;
        pre->next=p->next;  
        p=p->next;
        // sprintf(buf,"endpoint:shortAddr=%u is off-line\r\n",(uint16)pTmp->shortAddr);
        buf[2] = 0x21;
        buf[3] = p->Id[0];
        buf[5] = 0xfc;
        HalUARTWrite(0,buf,6); // �򴮿ڷ��ͽڵ���������
        continue;
      } 
      pre=p;
      p=p->next;
    }    
  }
}

void zb_FindDeviceConfirm( uint8 searchType, 
                          uint8 *searchKey, uint8 *result )
{
  
}

void uart_receive(uint8 port,uint8 event)
{
  uint16 dstAddr;
  if(event& (HAL_UART_RX_FULL|HAL_UART_RX_ABOUT_FULL|HAL_UART_RX_TIMEOUT))  //���ڽ��ܵ�����
  {
    uint8 buf[6];
    struct device_node *p=DeviceHeader.next;
    HalUARTRead(0,buf,6);  // ���ڶ�ȡ6���ַ����浽buf
    // HalUARTWrite(0,buf,6);
    if(buf[0]==0xcf && buf[5]==0xfc)  //�ж��Ƿ����Э��
    {
      while(p!=NULL)
      { 
        int i;
        for(i=0;i<p->Num;i++)//���ҽڵ�������ַ
        {
          if(p->Id[i]==buf[3])
            break;
        }
        if(i<p->Num)
          break;
        p=p->next;
      }
      // HalUARTWrite(0,p->shortAddr,2);
      if(p!=NULL)
      {
        osal_memcpy(&dstAddr,p->shortAddr,2);
        zb_SendDataRequest(dstAddr,TOGGLE_CMD_ID,
                       6,buf,0,FALSE,AF_DEFAULT_RADIUS);  //���͵���Ӧ�Ľڵ㡪���㲥
      } 
    }
  }  
}