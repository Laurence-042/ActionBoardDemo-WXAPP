// app.js
const app = getApp()

App({
  onLaunch: function() {
    var that = this

        // 展示本地存储能力
        var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
  },
  globalData: {
    tmp_host: 'yourHost.com:yourPort',
    openid: null,
    userInfo: null,
    username: null,
    liked_activities_id: null,
    joined_activities_id: null

  }
})