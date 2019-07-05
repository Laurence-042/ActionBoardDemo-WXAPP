// pages/editor/editor.js

const app = getApp()


Page({

  /**
   * 页面的初始数据
   */
  data: {
    date:null,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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
    this.setData({
      date: Date()
    })
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

  },

  formSubmit: function (e) {
    console.log('form发生了submit事件，携带数据为：', e.detail.value)
    var post_data = e.detail.value
    wx.request({
      url: 'https://' + app.globalData.tmp_host + '/wxapp/submit_activity/' + app.globalData.username + '/' + app.globalData.openid,
      method:'POST',
      data:post_data,
      success(res) {
        console.log(res.data);
      }
    })
  },
  formReset: function () {
    console.log('form发生了reset事件')
  }

})