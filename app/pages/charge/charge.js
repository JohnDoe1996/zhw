// pages/charge/charge.js
const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  backPage: () => {
    wx.navigateBack({
      delta: 1,
    })
  },

  chargeSubmit: function(e) {
    var that = this;
    console.log(e.detail.value.money);
    var money = e.detail.value.money;
    wx.request({
      url: app.globalData.url + '/user/charge',
      method: "POST",
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      data: {
        open_id: app.globalData.openId,
        money:money
      },
      success: res => {
        console.log(res);
        if (res.statusCode == 200 ) {
          if (res.data.code == 0){
            wx.showToast({
              title: res.data.data,
              duration: 3000,
              success: res => {
                setTimeout(that.backPage,3000);
              }
            })
          }else{
            wx.showToast({
              icon: 'none',
              title: res.data.data,
              duration: 2000,
            })
          }
        } else {
          wx.showToast({
            icon: 'none',
            title: '充值失败',
            duration: 2000,
          })
        }
      },
      fail: err => {
        wx.showToast({
          icon: 'none',
          title: '充值失败',
          duration: 2000,
        })
      }
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      userInfo: app.globalData.userInfo
    });
    this.setData({
      balance: options.balance
    });
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