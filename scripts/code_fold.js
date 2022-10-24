"use strict";

// 获取唯一 ID
function getUuid() {
  return Math.random().toString(36).substring(2, 8) + Date.now().toString(36);
}

hexo.extend.filter.register(
  "after_post_render",
  (data) => {
    const { line_number, lib } = hexo.theme.config.code.highlight;

    let reg;
    if (lib === "highlightjs") {
      if (line_number) {
        reg = /(<figure class="highlight.+?>)(.+?hljs (.*?)".+?)(<\/figure>)/gims;
      } else {
        reg = /(<div class="code-wrapper.+?>)(.+?hljs (.*?)".+?)(<\/div>)/gims;
      }
    } else if (lib === "prismjs") {
      reg = /(<div class="code-wrapper.+?>)(.+?data-language="(.*?)".+?)(<\/div>)/gims;
    }

    data.content = data.content.replace(reg, (match, begin, inner, lang, end, offset, string) => {
      const collapseId = `collapse-${getUuid()}`;
      //                             ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ 设置折叠按钮图标，此处使用 GitHub 图标
      const collapseBtn = `<i class="fa fa-chevron-down" type="button" data-toggle="collapse" data-target="#${collapseId}"></i>`;
      // const collapseDiv = `<div class="collapse show" id="${collapseId}">${inner}</div>`; // 默认不折叠
      const collapseDiv = `<div class="collapse show" id="${collapseId}">${inner}</div>`; // 默认折叠
      const langSpan = `<span>${lang}</span>`;
      return begin + collapseBtn + langSpan + collapseDiv + end;
    });
    return data;
  },
  10000 // 应该在完成其他渲染后执行，因此将优先级设大一点
);