// pages/main/main.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    activities: [],
    actions: [{
        title: "围观鶸在deadline后的反应",
        start_time: "2108/12/10 8:00",
        duration: "1小时",
        location: "人类存在之地",
        current_people_num: 6,
        max_people_num: 42
      },
      {
        title: "围观鶸在deadline前的反应",
        start_time: "2108/12/9 8:00",
        duration: "1小时",
        location: "人类存在之地",
        current_people_num: 6,
        max_people_num: 42
      },
      {
        title: "围观舍友在deadline前的反应",
        start_time: "2108/12/16 18:00",
        duration: "2小时",
        location: "6049",
        current_people_num: 1,
        max_people_num: 6
      },
      {
        title: "围观舍友在deadline前的反应",
        start_time: "2108/12/16 18:00",
        duration: "2小时",
        location: "6049",
        current_people_num: 1,
        max_people_num: 6
      },
      {
        title: "围观舍友在deadline前的反应",
        start_time: "2108/12/16 18:00",
        duration: "2小时",
        location: "6049",
        current_people_num: 1,
        max_people_num: 6
      },
      {
        title: "围观舍友在deadline前的反应",
        start_time: "2108/12/16 18:00",
        duration: "2小时",
        location: "6049",
        current_people_num: 1,
        max_people_num: 6
      },
      {
        title: "围观舍友在deadline前的反应",
        start_time: "2108/12/16 18:00",
        duration: "2小时",
        location: "6049",
        current_people_num: 1,
        max_people_num: 6
      },
    ]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    var that = this;
    if (!app.globalData.openid) {
      wx.redirectTo({
        url: '../login/login',
      })
      console.log("redirectTo login")
    } else {
      console.log("mian load");
      wx.request({
        url: 'https://' + app.globalData.tmp_host + '/wxapp/index/10',
        header: {
          'content-type': 'application/json' // 默认值
        },
        success(res) {
          that.setData({
            activities: res.data
          })
          console.log(res.data)
        }
      })
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
    if (app.globalData.openid) {
      this.refresh();
    }
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
    this.refresh()
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

  keep_an_eye_on: function(e) {
    var that = this;
    if (app.globalData.openid) {
      var activities = app.globalData.liked_activities_id
      var target_id = e["target"]["id"]
      if (!activities) {
        activities = new Array()
      }
      activities.push(target_id)
      wx.request({
        url: 'https://' + app.globalData.tmp_host + '/wxapp/modify_user_activities/' + app.globalData.openid + '/' + activities.join(','),
        header: {
          'content-type': 'application/json' // 默认值
        },
        success(res) {
          console.log("main keep")
          console.log(res.data)
          if (res.data[0]['status'] == 'success') {
            app.globalData.liked_activities_id = res.data[1]['liked_activities_id']
            that.refresh()
          }
        }
      })
    } else {
      wx.redirectTo({
        url: '../login/login',
      })
      console.log("redirectTo login")
    }
  },
  join: function(e) {
    var that = this;
    if (app.globalData.openid) {
      var target_id = e["target"]["id"]

      wx.request({
        url: 'https://' + app.globalData.tmp_host + '/wxapp/join_activity/' + target_id + '/' + app.globalData.openid,
        header: {
          'content-type': 'application/json' // 默认值
        },
        success(res) {
          console.log("main join")
          console.log(res.data);
          if (res.data[0]['status'] == 'success') {
            app.globalData.joined_activities_id = res.data[1]['joined_activities_id']
            that.keep_an_eye_on(e);
            that.refresh()
          }
        }
      })
    } else {
      wx.redirectTo({
        url: '../login/login',
      })
      console.log("redirectTo login")
    }
  },
  refresh: function() {
    var that = this;
    console.log("main refresh");
    console.log('https://' + app.globalData.tmp_host + '/wxapp/index/10')
    wx.request({
      url: 'https://' + app.globalData.tmp_host + '/wxapp/index/10',
      header: {
        'content-type': 'application/json' // 默认值
      },
      success(res) {
        for (var i = 0; i < res.data.length; i++) {
          if ((app.globalData.liked_activities_id).indexOf(res.data[i]['id'].toString()) === -1) {
            res.data[i]['liked'] = false;
          } else {
            res.data[i]['liked'] = true;
          }
          if ((app.globalData.joined_activities_id).indexOf(res.data[i]['id'].toString()) === -1) {
            res.data[i]['joined'] = false;
          } else {
            res.data[i]['joined'] = true;
          }
        }
        that.setData({
          activities: res.data
        })
        console.log("main refreshed")
        console.log(res.data)
        console.log(app.globalData)
      }
    })
  }
})