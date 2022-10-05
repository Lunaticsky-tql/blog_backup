---
title: Hexo 博客增加侧边栏
categories: 博客搭建
tags:
  - Hexo
  - 前端
abbrlink: 43390
---
### Hexo 博客增加侧边栏

效果：

![image-20220924213358550](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/Hexo%20%E5%8D%9A%E5%AE%A2%E5%A2%9E%E5%8A%A0%E4%BE%A7%E8%BE%B9%E6%A0%8F/20220924220650778115_333_image-20220924213358550.png)

根据https://github.com/qixa/hexo-theme-fluid-mod修改

#### 修改主题配置文件

color下新增属性

```css
  # 侧边栏颜色
  sidebar_text_color: "#3c4858"
  sidebar_background_color: "rgba(246, 248, 250, 0.82)" #f6f8fad1
  sidebar_button_color: "#99a9bf"
  sidebar_button_shift_color: "#ffffff"
  sidebar_button_shift_shadow: "0.1rem 0.1rem 0.5rem #3e3e3e"
  sidebar_about_link_color: "#3c4858"
  sidebar_about_link_hover_color: "#57A7D9"
  sidebar_avatar_border: "5px solid #ffffff"
  sidebar_subtitle_color: "#999999"
  sidebar_friend_title: "#ffffff"
  sidebar_friend_title_background: "#8FABD7"
  sidebar_friend_link: "#3c4858"
  sidebar_friend_link_hover: "#ffffff"
  sidebar_friend_li_border: "1px dashed #bdbdbd"
  sidebar_friend_li_hover: "#57A7D9"
  sidebar_friend_ico: "#bfbfbf"
```

新增全局属性

```css
sidebar:
    enable: true
    name: Lunatic sky
    introduce:  # 支持 HTML，留空则使用网站subtitle
    icons: 
        "fab fa-github": https://github.com/Lunaticsky-tql
        "fas fa-envelope": mailto:******

#---------------------------
# 侧边栏链接
# Links
#---------------------------    
sidebar_links:
  "my repository": https://github.com/Lunaticsky-tql?tab=repositories
```



#### 新增侧边栏模板文件

新建layout/_partial/sidebar.ejs

```javascript
<% if(theme.sidebar.enable){ %>
<div id="sidebar" class="sidebar-hide">
  <span class="sidebar-button sidebar-button-shift" id="toggle-sidebar" >
    <i class="fa fa-arrow-right on" aria-hidden="true"></i>
  </span>
  <div class="sidebar-overlay"></div>
  <div class="sidebar-intrude">
    <div class="sidebar-avatar">
      <img src="<%- url_for(theme.avatar) %>" srcset="<%- url_for(theme.avatar) %>" alt="avatar"/>
    </div>
    <div class="text-center sidebar-about">
      <p class="h3 sidebar-author"><%= theme.sidebar.name || config.title %></p>
      <p class="sidebar-subtitle"><%- theme.sidebar.introduce || config.subtitle %></p>
      <% for(var i in theme.sidebar.icons) { %>
        <a href="<%- theme.sidebar.icons[i] %>" class="h4" target="_blank">
          <i class="<%- i %>" aria-hidden="true"></i>
        </a>
        &nbsp;&nbsp;
      <% } %>
    </div>
    <div class="sidebar-friend">
      <p class="h6 sidebar-friend-title">
        <span class="sidebar-label-left"><i class="fas fa-user-friends"></i></span>
        <span class="sidebar-label">相关链接</span>
      </p>
      <ul class="list-group">
        <% for(var i in theme.sidebar_links) { %>
          <a href="<%- theme.sidebar_links[i] %>" target="_blank">
            <li class="list-group-item">
              <i class="fas fa-quote-left"></i>&nbsp;
              <%- i %>
            </li>
          </a>
        <% } %>
    </ul>
    </div>
  </div>
</div>
<% } %>
```

layout.ejs中引入

![image-20220919235231945](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/Hexo%20%E5%8D%9A%E5%AE%A2%E5%A2%9E%E5%8A%A0%E4%BE%A7%E8%BE%B9%E6%A0%8F/20220920002715526487_276_image-20220919235231945.png)

```javascript
<%- partial('_partials/sidebar.ejs') %>
```

#### 修改CSS文件

source/css/_variables/base.styl

增加侧边栏相关变量

```css
//toc
$tocbot-link-shadow = theme-config("color.tocbot_link_shadow", "0.1em 0.1em 0.2em #ffffff")
$tocbot-active-link-shadow = theme-config("color.tocbot_active_link_shadow", "0.1em 0.1em 0.2em #ffbcbc")

//sidebar
$sidebar-text-color = theme-config("color.sidebar_text_color", "#3c4858")
$sidebar-background-color = theme-config("color.sidebar_background_color", "#f6f8fad1")
$sidebar-button-color = theme-config("color.sidebar_button_color", "#99a9bf")
$sidebar-button-shift-color = theme-config("color.sidebar_button_shift_color", "#ffffff")
$sidebar-button-shift-shadow = theme-config("color.sidebar_button_shift_shadow", "0.1rem 0.1rem 0.5rem #3e3e3e")
$sidebar-about-link-color = theme-config("color.sidebar_about_link_color", "#3c4858")
$sidebar-about-link-hover-color = theme-config("color.sidebar_about_link_hover_color", "#fe4365")
$sidebar-avatar-border = theme-config("color.sidebar_avatar_border", "5px solid #ffffff")
$sidebar-subtitle-color = theme-config("color.sidebar_subtitle_color", "#999999")
$sidebar-friend-title = theme-config("color.sidebar_friend_title", "#ffffff")
$sidebar-friend-title-background = theme-config("color.sidebar_friend_title_background", "#fe91b4")
$sidebar-friend-link = theme-config("color.sidebar_friend_link", "#3c4858")
$sidebar-friend-link-hover = theme-config("color.sidebar_friend_link_hover", "#ffffff")
$sidebar-friend-li-border = theme-config("color.sidebar_friend_li_border", "1px dashed #bdbdbd")
$sidebar-friend-li-hover = theme-config("color.sidebar_friend_li_hover", "#fe91b4")
$sidebar-friend-ico = theme-config("color.sidebar_friend_ico", "#bfbfbf")
```

layout/_partials/css.ejs

引入需要的图标字体

```javascript
<%- css_ex(theme.static_prefix.font_awesome, "css/all.min.css") %>
```

#### JS 文件

source/js/main.js

增加侧边栏相关控制代码

```javascript
/* Sidebar */
var toggleSidebar = function(){
  $("#sidebar").toggleClass('sidebar-hide');
  $("#toggle-sidebar").toggleClass('sidebar-button-shift');
}
var hideSidebar = function(){
  $("#sidebar").addClass('sidebar-hide');
  $("#toggle-sidebar").addClass('sidebar-button-shift');
}
$("#toggle-sidebar").on("click",toggleSidebar);
$("header").on("click",hideSidebar);
$("#mainContent").on("click",hideSidebar);
$("#footerContent").on("click",hideSidebar);
```

layout/_partials/scripts.ejs中进行引用

![image-20220920000758138](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/Hexo%20%E5%8D%9A%E5%AE%A2%E5%A2%9E%E5%8A%A0%E4%BE%A7%E8%BE%B9%E6%A0%8F/20220920002717155064_217_image-20220920000758138.png)

```javascript
<%- js_ex(theme.static_prefix.internal_js, 'main.js') %>
```

配置完成后，可以从左下角箭头打开侧边栏。

---

### 去除图片阴影

主题中图片自带的阴影有些不够干净简洁。可以通过修改styl去除之。

在source/css/_variables/base.styl

将图片阴影的属性修改即可。

![image-20220925171400552](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/Hexo%20%E5%8D%9A%E5%AE%A2%E5%A2%9E%E5%8A%A0%E4%BE%A7%E8%BE%B9%E6%A0%8F/20220924220653383643_614_image-20220924213743047.png)

### 去除图片标题显示

这个就很简单了。

![image-20221001000113637](/Users/tianjiaye/Library/Application Support/typora-user-images//image-20221001000113637.png)