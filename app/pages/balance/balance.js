// pages/balance/balance.js
const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo: {},
    balance: ""
  },

  gotoPage: function(e) {
    var page = e.currentTarget.id;
    wx.navigateTo({
      url: '/pages/' + page + '/' + page + "?balance=" + this.data.balance,
    })
  },

  getBalance(){
    wx.request({
      url: app.globalData.url + '/user/balance',
      method:"POST",
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      data:{
        open_id: app.globalData.openId
      },
      success: res => {
        console.log(res);
        if (res.statusCode == 200 && res.data.code == 0){
          this.setData({
            balance: res.data.data.balance
          })
        }else{
          wx.showToast({
            icon: 'none',
            title: '余额查询失败',
            duration: 2000,
          })
        }
      },
      fail: err => {
        wx.showToast({
          icon: 'none',
          title: '余额查询失败',
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
    })
    this.getBalance();
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
    this.getBalance();
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