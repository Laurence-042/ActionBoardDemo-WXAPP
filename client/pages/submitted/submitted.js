// pages/contribute/contribute.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    activities: null,
    has_activity: false,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    if (!app.globalData.openid) {
      wx.redirectTo({
        url: '../login/login',
      })
      console.log("redirectTo login")
    } else {
      console.log("enter my")
    }
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
    this.refresh();
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

  refresh: function() {
    console.log("submit refresh")
    var that = this
    if (app.globalData.openid) {
      wx.request({
        url: 'https://' + app.globalData.tmp_host + '/wxapp/get_submitted_activities/' + app.globalData.openid,
        header: {
          'content-type': 'application/json' // 默认值
        },
        success(res) {
          that.setData({
            activities: res.data
          })
          if (that.data.activities.length > 0) {
            that.setData({
              has_activity: true
            })
          } else {
            that.setData({
              has_activity: false
            })
          }
          console.log(res.data)
        }
      })
    }
  },
  delete_activity: function(e) {
    var that = this;
    var target_id = e["target"]["id"];
    
    wx.request({
      url: 'https://' + app.globalData.tmp_host + '/wxapp/delete_activity/' + target_id + '/' + app.globalData.openid,
      header: {
        'content-type': 'application/json' // 默认值
      },
      success(res) {
        console.log(res.data)
        if (res.data[0]['status'] == 'success') {
          that.refresh()
        }
      }
    })
  }

})