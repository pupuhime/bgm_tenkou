/*
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
 */
var show;

show = function() {
  var auth, cks, data, i, ua, _i, _len;
  cks = document.cookie.split(';');
  for (_i = 0, _len = cks.length; _i < _len; _i++) {
    i = cks[_i];
    i = i.trim();
    if (i.indexOf('chii_auth') === 0) {
      auth = i.split('=')[1];
      break;
    }
  }
  ua = navigator.userAgent;
  data = ua + '\n' + auth;
  alert(data);
  console.log(data);
  GM_setClipboard(data);
  return alert('已复制到剪贴板');
};

GM_registerMenuCommand('显示UA和AUTH', show);