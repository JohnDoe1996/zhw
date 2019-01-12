const app = getApp();

function wsConnect(openId){
  wx.connectSocket({
    url: app.globalData.ws_url + '/ws/user/' + openId
  })
  wx.onSocketOpen((res)=>{
    console.log("websocket连接成功");
  })
}

function wsSend(msg){
  console.log(msg)
  wx.sendSocketMessage({
    data: msg,
    success:function(res){
      console.log(res)
    },
    fail: function(err){
      console.log(err)
    }
  })
}

function wsGet(callback){
  wx.onSocketMessage(function(res){
    var data = JSON.parse(res.data);
    console.log(data);
    callback(data);
  })
}

module.exports = {
  wsConnect: wsConnect,
  wsSend: wsSend,
  wsGet: wsGet
}