// pages/action/action.js
const app = getApp();
var ws = require("../../utils/ws.js");

Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo: {},
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    this.setData({
      userInfo: app.globalData.userInfo
    })
    console.log(options);
    var code = JSON.parse(options.data)
    this.setData({
      code : code
    });
    wx.request({
      url: app.globalData.url + '/shop/' + code.act,
      method: "POST",
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      data:code,
      success:function(res){
        console.log(res)
        if (res.statusCode == 200) {
          if (res.data.code == 0){
            that.setData({
              act: res.data.data.act,
              price: res.data.data.price
            })
          } else {
            that.setData({
              act: "other",
              errmsg: res.data.data
            })
          }
        }else{
          that.setData({
            act: "other",
            errmsg: "服务器连接错误"
          })
        }
      },
      fail:function(err){
        that.setData({
          act: "other",
          errmsg:"网络连接错误"
        })
      }
    })
  },

  // 错误时弹出对话框
  errorMsgBox: function (title, content, callback) {
    var that = this;
    wx.showModal({
      title: title,
      content: content,
      success: function () {
        callback();
      }
    })
  },

  sellSubmit:function(e){
    var that = this;
    console.log(e);
    var value = e.detail.value.value;
    if(value == "" || value <= 0){
      that.errorMsgBox("错误","输入金额有误")
    }else{
      wx.showModal({
        title: '提示',
        content: '确定要出售此商品吗？',
        success(res){
          if (res.confirm) {
            var msg = {
              act: "sell",
              id: that.data.code.id,
              num: that.data.code.num,
              price: value
            }
            ws.wsSend(JSON.stringify(msg));
            that.waitResult();
          }
        }
      })
    }

  },

  buySubmit:function(e){
    var that = this;
    wx.showModal({
      title: '提示',
      content: '确定要购买此商品吗？',
      success(res) {
        if (res.confirm) {
          var msg = {
            act: "buy",
            id: that.data.code.id,
            num: that.data.code.num,
          }
          ws.wsSend(JSON.stringify(msg));
          that.waitResult();
        }
      }
    })

  },

  waitResult: function(){
    ws.wsGet(this.andThen);
  },

  andThen: function(res){
    var that = this;
    if(res.code == 0){
      var msg = '操作成功';
      if (that.data.act == "buy")
        msg = "购买成功";
      wx.showToast({
        title: msg,
        duration: 5000,
        success: res => {
          setTimeout(that.backPage, 5000);
        }
      })
    }else{
      var msg = '操作失败';
      if (that.data.act == "buy")
        msg = "购买失败";
      that.errorMsgBox(msg,res.data,()=>{});
    }
  },

  backPage: () => {
    wx.navigateBack({
      delta: 1,
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})