###
// ==UserScript==
// @name           getbgmcookie
// @namespace      https://github.com/hentaiPanda
// @author         niR
// @version        0.0.1
// @license        MIT License
// @encoding       utf-8
// @grant          GM_setClipboard
// @grant          GM_registerMenuCommand
// @include        http://bangumi.tv/*
// @include        http://bgm.tv/*
// @include        http://chii.in/*
// ==/UserScript==
###


show = ->
  # alert(document.cookie)
  cks = document.cookie.split(';')
  for i in cks
    i = i.trim()
    if i.indexOf('chii_auth') is 0
      auth = i.split('=')[1]
      break
  ua = navigator.userAgent
  data = ua + '\n' + auth
  alert(data)
  console.log(data)
  GM_setClipboard(data)
  alert('已复制到剪贴板')


GM_registerMenuCommand('显示UA和AUTH', show)