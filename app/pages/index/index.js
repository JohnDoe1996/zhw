//index.js
//获取应用实例
const app = getApp()
var ws = require("../../utils/ws.js");

Page({
  data: {
    userInfo: {},
  },

  //扫二维码
  sweepQR : e => {
    console.log(e);
    var act = e.currentTarget.id
    wx.scanCode({
      onlyFromCamera: true,
      scanType: ['qrCode'],
      success(res) {
        console.log(res);
        try {
          var data = JSON.parse(res.result);
          if (typeof data == "object") {
            if (data.host == "zhw"){
              data.act = act;
              var dataStr = JSON.stringify(data);
              wx.navigateTo({
                url: '/pages/action/action?data=' + dataStr,
              })
            }else{
              wx.showToast({
                title: '二维码不正确',
                icon: 'none',
                duration: 2000
              })
            }
          }else{
            wx.showToast({
              title: '二维码不正确',
              icon: 'none',
              duration: 2000
            })
          }
        } catch (e) {
          console.log(e);
          wx.showToast({
            title: '二维码不正确',
            icon: 'none',
            duration: 2000
          })

        }
      }
    })
  },

  gotoPage: e => {
    var page = e.currentTarget.id;
    wx.navigateTo({
      url: '/pages/' + page + '/' + page,
    })
  },

  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
          })
        }
      })
    }

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        wx.request({
          url: app.globalData.url + '/wx_login',
          method: "POST",
          dataType: "json",
          header: {
            "Content-Type": "application/x-www-form-urlencoded"
          },
          data: {
            js_code: res.code
          },
          success: res => {
            console.log(res);
            var openId = res.data.openId;
            ws.wsConnect(openId);
          }
        })
      }
    })

  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
    })
  }
})
