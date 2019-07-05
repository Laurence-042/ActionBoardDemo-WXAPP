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
    this.refresh()
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
    console.log("my refresh")
    console.log(app.globalData)
    var that = this
    var activities = app.globalData.liked_activities_id
    if (activities) {
      if (activities.length > 0) {
        wx.request({
          url: 'https://' + app.globalData.tmp_host + '/wxapp/get_specific_activities/' + activities.join(','),
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
            console.log("my refresh successfully")
            console.log(res.data)
          }
        })
      } else {
        that.setData({
          has_activity: false
        })
      }
    }
  },
  discard_activity: function(e) {
    var that = this;
    var activities = app.globalData.liked_activities_id;
    var target_id = e["target"]["id"];

    console.log("my discard_activity")
    console.log(activities)

    var i = 0;
    for (i = 0; i < activities.length; i++) {
      if (activities[i] == target_id) {
        break;
      }
    }
    activities.splice(i, 1);

    if (activities.length == 0) {
      activities.push("0")
    }

    wx.request({
      url: 'https://' + app.globalData.tmp_host + '/wxapp/modify_user_activities/' + app.globalData.openid + '/' + activities.join(','),
      header: {
        'content-type': 'application/json' // 默认值
      },
      success(res) {
        console.log(res.data)
        if (res.data[0]['status'] == 'success') {
          app.globalData.liked_activities_id = res.data[1]['liked_activities_id'];
          that.refresh()
        }
      }
    })
    wx.request({
      url: 'https://' + app.globalData.tmp_host + '/wxapp/leave_activity/' + target_id + '/' + app.globalData.openid,
      header: {
        'content-type': 'application/json' // 默认值
      },
      success(res) {
        console.log(res.data)
        if (res.data[0]['status'] == 'success') {
          app.globalData.joined_activities_id = res.data[1]['joined_activities_id'];
          that.refresh()
        }
      }
    })
  }

})