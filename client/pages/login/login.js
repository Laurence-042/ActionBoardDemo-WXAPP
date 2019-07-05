// pages/login.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    username: null,
    password: null
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  },

  onGotUserInfo: function(e) {
    var that = this
    console.log(e.detail.errMsg)
    console.log(e.detail.userInfo)
    console.log(e.detail.rawData)
    wx.login({
      success(res) {
        if (res.code) {
          console.log(res.code)
          //发起网络请求
          wx.request({
            url: 'https://' + app.globalData.tmp_host + '/wxapp/do_login/' + res.code + '/' + e.detail.userInfo['nickName'],
            success(res) {
              console.log('login success')
              console.log(res.data);
              app.globalData.userInfo = e.detail.userInfo;
              app.globalData.openid = res.data[0]['openid'];
              app.globalData.liked_activities_id = res.data[1]['liked_activities_id'];
              app.globalData.joined_activities_id = res.data[1]['joined_activities_id'];
              if (!app.globalData.liked_activities_id) {
                app.globalData.liked_activities_id = new Array()
              }
              if (!app.globalData.joined_activities_id) {
                app.globalData.joined_activities_id = new Array()
              }
              app.globalData.username = e.detail.userInfo['nickName']
              console.log(app.globalData);
              if (app.globalData.userInfo) {
                wx.switchTab({
                  url: '../my/my'
                })
              }
            }
          })
        } else {
          console.log('登录失败！' + res.errMsg)
        }
      }
    })
  },
})