// pages/accredit/accredit.js
var timer;

Page({

  /**
   * 页面的初始数据
   */
  data: {
  },

  toAuthorize: function () {
    //重新调起授权
    wx.getSetting({
      success: (res) => {
        if (res.authSetting['scope.userInfo']) {
          clearInterval(timer);
          //reLaunch
          wx.reLaunch({
            url: '/pages/index/index'
          })
        }
      }
    })
  },

  userLogin:function(){
    timer = setInterval(this.toAuthorize,100);
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.toAuthorize();
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