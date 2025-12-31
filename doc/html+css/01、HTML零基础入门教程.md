# HTML 零基础入门教程

你希望系统学习 HTML 来构建网页结构，这份教程将从基础概念到实战示例，带你逐步掌握 HTML 的核心用法，适合完全零基础的入门者。

## 一、HTML 基础认知

### 1. 什么是 HTML

HTML（HyperText Markup Language，超文本标记语言）**不是编程语言**，而是一种**标记语言**，用于定义网页的结构和内容布局。它通过一系列预定义的标记标签，告诉浏览器如何展示网页中的文字、图片、链接等内容。

### 2. HTML 文件特性

- 后缀名：`.html` 或 `.htm`（推荐使用 `.html`）
- 打开方式：可用任意文本编辑器（记事本、VS Code、Sublime 等）编辑，用任意浏览器（Chrome、Edge 等）打开预览效果
- 核心作用：搭建网页的 "骨架"，负责**结构呈现**，样式美化（CSS）和交互逻辑（JavaScript）需配合其他技术实现

## 二、HTML 基本文档结构

所有 HTML 页面都遵循固定的基本结构，这是浏览器解析网页的基础框架，缺一不可。

html



预览









```html
<!DOCTYPE html>
<!-- 根标签：包裹所有HTML内容，lang指定页面语言（zh-CN为中文，en为英文） -->
<html lang="zh-CN">
<!-- 头部：存放网页元信息，不直接显示在页面可视区域（除title外） -->
<head>
    <!-- 声明网页编码格式（UTF-8支持所有中文和特殊字符，避免乱码） -->
    <meta charset="UTF-8">
    <!-- 适配移动端网页（可选，用于响应式设计） -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- 网页标题：显示在浏览器标签栏上 -->
    <title>我的第一个HTML页面</title>
</head>
<!-- 主体：存放网页所有可视内容（文字、图片、链接等） -->
<body>
    <!-- 页面可视内容写在这里 -->
    你好，HTML！
</body>
</html>
```

### 结构说明

1. `<!DOCTYPE html>`：文档类型声明，告诉浏览器这是 HTML5 版本的网页，必须放在页面最顶部
2. `<html>`：根标签，所有其他标签都嵌套在这个标签内
3. `<head>`：头部标签，负责配置网页基础信息，核心标签包括 `meta`（编码、适配配置）、`title`（网页标题）
4. `<body>`：主体标签，网页的可视内容全部放在这里

## 三、常用文本排版标签

文本标签用于组织网页中的文字内容，实现标题、段落、换行等排版效果，是最基础的常用标签。

| 标签          | 作用                 | 特点                             |
| ------------- | -------------------- | -------------------------------- |
| `<h1>`~`<h6>` | 标题标签（1-6 级）   | h1 级别最高（最大最粗），h6 最低 |
| `<p>`         | 段落标签             | 自动在段落前后添加空白行         |
| `<br>`        | 换行标签             | 自闭合标签（无需结束标签）       |
| `<hr>`        | 水平线标签           | 自闭合标签，添加一条分隔线       |
| `<em>`        | 强调标签（斜体）     | 语义化标签，默认斜体显示         |
| `<strong>`    | 重点强调标签（加粗） | 语义化标签，默认加粗显示         |

示例代码：

html



预览









```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>文本排版示例</title>
</head>
<body>
    <h1>一级标题（文章主标题）</h1>
    <h2>二级标题（章节标题）</h2>
    <p>这是第一个段落，HTML是网页开发的基础，所有网页都离不开HTML的结构支撑。</p>
    <p>这是第二个段落，<br>这里使用br标签实现强制换行，不需要另起一个段落。</p>
    <hr>
    <p>这是一段带有强调的文字：<em>斜体强调内容</em>，<strong>加粗重点内容</strong></p>
    <h6>六级标题（最小标题）</h6>
</body>
</html>
```

## 四、HTML 属性

### 1. 什么是 HTML 属性

属性是为 HTML 标签提供额外信息的附加内容，用于控制标签的样式、行为或关联资源，所有属性都写在**开始标签**中。

### 2. 属性基本语法

- 格式：`标签名 属性名="属性值">`
- 特点：
  1. 属性名与属性值之间用等号 `=` 连接
  2. 属性值必须用双引号 `"` 或单引号 `'` 包裹（推荐双引号）
  3. 一个标签可以同时拥有多个属性，属性之间用空格分隔

### 3. 常用属性示例

html



预览









```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>属性示例</title>
</head>
<body>
    <!-- a标签：链接标签，href属性指定跳转地址，title属性指定鼠标悬浮提示文字 -->
    <a href="https://www.baidu.com" title="点击跳转到百度">百度首页</a>
    
    <!-- img标签：图片标签，src指定图片路径，alt指定图片加载失败时的替代文字，width/height指定图片尺寸 -->
    <img src="logo.png" alt="网站logo" width="200" height="100">
</body>
</html>
```

## 五、链接标签（`<a>`）

<a> 标签（锚标签）用于创建网页链接，实现页面跳转功能，是网页导航的核心标签。

### 核心属性

1. `href`：必填属性，指定跳转目标地址，支持两种类型：
   - 外部链接：跳转至其他网站，如 `href="https://www.qq.com"`
   - 内部链接：跳转至本站内其他页面，如 `href="about.html"`
2. `target`：可选属性，指定链接打开方式：
   - `_self`：默认值，在当前浏览器窗口打开链接
   - `_blank`：在新的浏览器窗口打开链接

### 示例代码

html



预览









```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>链接示例</title>
</head>
<body>
    <!-- 外部链接，新窗口打开 -->
    <a href="https://www.github.com" target="_blank">GitHub（新窗口打开）</a>
    <br>
    <!-- 内部链接，当前窗口打开 -->
    <a href="contact.html">联系我们（当前窗口打开）</a>
    <br>
    <!-- 锚点链接：跳转至页面内指定位置（先定义锚点，再跳转） -->
    <a href="#top">返回顶部</a>
    <h2 id="top">页面顶部</h2>
</body>
</html>
```

## 六、图片标签（`<img>`）

<img> 标签用于在网页中插入图片，是自闭合标签（无需写 </img>）。

### 核心属性

1. `src`：必填属性，指定图片的路径，支持两种类型：
   - 绝对路径：网络图片地址，如 `src="https://xxx.com/photo.jpg"`
   - 相对路径：本地图片地址，如 `src="images/photo.jpg"`（图片放在当前文件夹下的 images 目录中）
2. `alt`：必填属性，图片加载失败时显示的替代文字（提升无障碍访问性，利于 SEO）
3. `width`/`height`：可选属性，指定图片的宽度和高度，单位可以是像素（px，可省略）或百分比
4. 注意：若只设置宽度或高度，图片会按原比例自动缩放，避免变形

### 示例代码

html



预览









```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>图片示例</title>
</head>
<body>
    <!-- 网络图片 -->
    <img src="https://img.baidu.com/xxx.jpg" alt="风景图片" width="300">
    <br>
    <!-- 本地图片 -->
    <img src="cat.jpg" alt="猫咪图片" height="200">
</body>
</html>
```

## 七、列表标签

列表用于有序或无序地展示一组相关内容，HTML 提供了 3 种常用列表类型。

### 1. 无序列表（`<ul>` + `<li>`）

- 特点：列表项前显示项目符号（默认圆点），无先后顺序
- 结构：`<ul>` 包裹所有列表项，每个列表项用 `<li>` 表示
- 常用场景：导航菜单、商品列表、功能列表等

### 2. 有序列表（`<ol>` + `<li>`）

- 特点：列表项前显示数字编号（默认 1、2、3...），有先后顺序
- 结构：`<ol>` 包裹所有列表项，每个列表项用 `<li>` 表示
- 常用场景：步骤说明、排名列表、教程流程等

### 3. 定义列表（`<dl>` + `<dt>` + `<dd>`）

- 特点：用于展示 “术语 - 解释” 对应关系
- 结构：`<dl>` 包裹整体，`<dt>` 表示术语，`<dd>` 表示术语的解释
- 常用场景：名词解释、商品参数说明等

### 示例代码

html



预览









```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>列表示例</title>
</head>
<body>
    <h3>无序列表（水果）</h3>
    <ul>
        <li>苹果</li>
        <li>香蕉</li>
        <li>橙子</li>
    </ul>

    <h3>有序列表（学习步骤）</h3>
    <ol>
        <li>学习HTML</li>
        <li>学习CSS</li>
        <li>学习JavaScript</li>
    </ol>

    <h3>定义列表（电脑参数）</h3>
    <dl>
        <dt>处理器</dt>
        <dd>Intel i7-13700H</dd>
        <dt>内存</dt>
        <dd>16GB DDR5</dd>
        <dt>硬盘</dt>
        <dd>512GB SSD</dd>
    </dl>
</body>
</html>
```

## 八、表格标签

表格用于规整地展示二维数据（行 + 列），如成绩表、商品价格表、数据统计等。

### 核心标签

1. `<table>`：包裹整个表格
2. `<tr>`：表格的行（table row）
3. `<th>`：表头单元格（table header），默认加粗居中显示
4. `<td>`：内容单元格（table data），默认左对齐显示
5. 可选属性：`border`（设置表格边框宽度，单位 px）

### 基本结构

html



预览









```html
<table border="1">
    <!-- 表头行 -->
    <tr>
        <th>姓名</th>
        <th>语文</th>
        <th>数学</th>
    </tr>
    <!-- 内容行1 -->
    <tr>
        <td>张三</td>
        <td>90</td>
        <td>95</td>
    </tr>
    <!-- 内容行2 -->
    <tr>
        <td>李四</td>
        <td>88</td>
        <td>92</td>
    </tr>
</table>
```

## 九、表单标签（`<form>`）

表单用于收集用户输入的信息（如登录、注册、问卷调查等），是网页与用户交互的核心。

### 1. 核心表单标签

- `<form>`：包裹所有表单元素，定义表单的提交规则
  - 核心属性：`action`（表单提交的后台接口地址）、`method`（提交方式，常用`get`/`post`）
- `<input>`：单行输入框，通过`type`属性切换不同输入类型（最常用表单元素）
- `<textarea>`：多行文本输入框（用于输入大量文字，如留言、备注）
- `<select>`+`<option>`：下拉选择框（用于从固定选项中选择）
- `<button>`：提交 / 重置按钮

### 2. 常用`<input>`类型

| type 值    | 输入类型   | 场景                 |
| ---------- | ---------- | -------------------- |
| `text`     | 单行文本框 | 输入姓名、账号等     |
| `password` | 密码输入框 | 输入密码（内容隐藏） |
| `radio`    | 单选按钮   | 性别选择（互斥选项） |
| `checkbox` | 复选框     | 兴趣爱好（多选选项） |
| `submit`   | 提交按钮   | 提交表单数据         |
| `reset`    | 重置按钮   | 清空表单所有输入内容 |

### 示例代码

html



预览









```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>表单示例</title>
</head>
<body>
    <h3>用户注册表单</h3>
    <form action="submit.php" method="post">
        <!-- 单行文本框 -->
        <p>
            账号：<input type="text" name="username" placeholder="请输入账号">
        </p>
        <!-- 密码输入框 -->
        <p>
            密码：<input type="password" name="password" placeholder="请输入密码">
        </p>
        <!-- 单选按钮 -->
        <p>
            性别：
            <input type="radio" name="gender" value="male" checked> 男
            <input type="radio" name="gender" value="female"> 女
        </p>
        <!-- 复选框 -->
        <p>
            兴趣爱好：
            <input type="checkbox" name="hobby" value="read"> 阅读
            <input type="checkbox" name="hobby" value="sport"> 运动
            <input type="checkbox" name="hobby" value="music"> 音乐
        </p>
        <!-- 下拉选择框 -->
        <p>
            城市：
            <select name="city">
                <option value="beijing">北京</option>
                <option value="shanghai" selected>上海</option>
                <option value="guangzhou">广州</option>
            </select>
        </p>
        <!-- 多行文本框 -->
        <p>
            备注：
            <textarea name="remark" rows="3" cols="20" placeholder="请输入备注信息"></textarea>
        </p>
        <!-- 按钮 -->
        <p>
            <button type="submit">提交</button>
            <button type="reset">重置</button>
        </p>
    </form>
</body>
</html>
```

## 十、完整 HTML 示例（整合所有知识点）

html



预览









```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的第一个完整HTML页面</title>
</head>
<body>
    <!-- 标题与导航 -->
    <h1 align="center">我的个人主页</h1>
    <hr>
    <ul align="center">
        <li><a href="#info" target="_self">个人信息</a></li>
        <li><a href="#hobby" target="_self">兴趣爱好</a></li>
        <li><a href="#contact" target="_self">联系我</a></li>
    </ul>
    <hr>

    <!-- 个人信息区域 -->
    <h2 id="info">个人信息</h2>
    <img src="avatar.jpg" alt="我的头像" width="150" height="150">
    <p>姓名：张三</p>
    <p>年龄：25岁</p>
    <p>职业：<strong>前端开发工程师</strong></p>
    <p>简介：<em>热爱网页开发，专注于前端技术学习与实践</em></p>

    <!-- 兴趣爱好区域 -->
    <h2 id="hobby">兴趣爱好</h2>
    <ol>
        <li>编程（HTML/CSS/JavaScript）</li>
        <li>阅读（技术书籍、文学作品）</li>
        <li>运动（跑步、篮球）</li>
    </ol>

    <!-- 联系我区域（表单） -->
    <h2 id="contact">联系我</h2>
    <form action="" method="post">
        <p>
            您的姓名：<input type="text" name="name" placeholder="请输入您的姓名">
        </p>
        <p>
            您的邮箱：<input type="text" name="email" placeholder="请输入您的邮箱">
        </p>
        <p>
            留言内容：<textarea name="message" rows="3" cols="30"></textarea>
        </p>
        <input type="submit" value="发送留言">
        <input type="reset" value="清空内容">
    </form>

    <hr>
    <p align="center">© 2025 张三的个人主页 版权所有</p>
</body>
</html>
```

## 十一、学习总结

1. HTML 是网页的结构骨架，核心作用是定义页面内容的布局和组织形式
2. 所有 HTML 页面都遵循「DOCTYPE + html + head + body」的基本结构
3. 标签是 HTML 的核心组成，分为双标签（`<p></p>`）和自闭合标签（`<img>`）
4. 属性为标签提供额外信息，语法为「属性名 ="属性值"」，写在开始标签中
5. 常用核心标签：文本标签（h1-h6、p）、链接标签（a）、图片标签（img）、列表标签（ul/ol/dl）、表格标签、表单标签
6. HTML 仅负责结构，若需美化页面（如颜色、布局）需学习 CSS，若需实现交互（如点击事件）需学习 JavaScript