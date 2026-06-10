# docsify部署教程



## 准备工作

> - 官网：https://docsify.js.org/#/
>
> - 下载nodejs：https://www.nodejs.com.cn/download.html ，这里使用的nodejs18.19.0长期维护版本

## 安装docsify

### 安装nodejs

一直到下一步完成.

```powershell
PS C:\Users\Anita> node -v
v18.19.0
```

全局安装docsify

```powershell
npm i docsify-cli -g
```

安装过程如下：

```powershell
PS C:\Users\Anita> npm i docsify-cli -g
npm WARN deprecated docsify-server-renderer@4.13.1: docsify-server-renderer 4.x and below is no longer supported while we investigate the future of SSR and SSG for Docsify

added 205 packages in 20s

17 packages are looking for funding
  run `npm fund` for details
npm notice
npm notice New major version of npm available! 10.2.3 -> 11.5.2
npm notice Changelog: https://github.com/npm/cli/releases/tag/v11.5.2
npm notice Run npm install -g npm@11.5.2 to update!
npm notice
PS C:\Users\Anita> docsify serve docs

No docs found C:\Users\Anita\docs\index.html
Please run docsify init first.
```

## 初始化目录

创建web目录

> E:\DATA\Myweb-data\mydoc

创建完目录之后，命令行进入目录，然后执行`docsify init`

```powershell
PS E:\DATA\Myweb-data> cd .\mydoc\
PS E:\DATA\Myweb-data\mydoc> docsify init
. already exists.
√ Are you sure you want to rewrite it? (y/N) true

Initialization succeeded! Please run docsify serve

PS E:\DATA\Myweb-data\mydoc> docsify serve

Serving E:\DATA\Myweb-data\mydoc now.
Listening at http://localhost:3000    #访问此地址即可看见网站
```





## 启动

```
docsify serve
```



## 多页面

建议创建多个目录进行分类，不要放在根目录下。

## 配置index

‘index.html’文件的配置，非常重要，尽量不要去改。

所有的配置都是基于index文件，它包含了站点的主题、导航、侧边栏、插件等。

```html
<!-- docs/index.html -->

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>pokes学习笔记档案</title>
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
  <meta name="description" content="Description">
  <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
  <!-- 下面这一行就是主题 -->
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/vue.css">
  
</head>
<body>

  <div id="app"></div>
  
  <script>
      window.$docsify = {
        name: '<span>spokes</span>',
        repo: '',
        el: '#app',
        loadSidebar: true,
        autoHeader: true,

        // 导航栏支持，默认加载的是项目根目录下的_navbar.md文件
        loadNavbar: true,

        // 封面支持，默认加载的是项目根目录下的_coverpage.md文件
        coverpage: true,
        // 最大支持渲染的标题层级
        maxLevel: 5,
        // 自定义侧边栏后默认不会再生成目录，设置生成目录的最大层级（建议配置为2-4）
        subMaxLevel: 4,
        // 小屏设备下合并导航栏到侧边栏
        mergeNavbar: true,

        loadSidebar: true,//加载侧边栏
        subMaxLevel: 2    //目录显示层级


       // logo: '/_media/icon.svg'


    }
  </script>
  <!-- <script src="//cdn.jsdelivr.net/npm/docsify@4"></script> -->
    <!-- docsify的js依赖 -->
    <script src="//cdn.jsdelivr.net/npm/docsify/lib/docsify.min.js"></script>
    <!-- emoji表情支持 -->
    <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/emoji.min.js"></script>
    <!-- 图片放大缩小支持 -->
    <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/zoom-image.min.js"></script>
    <!-- 搜索功能支持 -->
    <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/search.min.js"></script>
    <!--在所有的代码块上添加一个简单的Click to copy按钮来允许用户从你的文档中轻易地复制代码-->
    <script src="//cdn.jsdelivr.net/npm/docsify-copy-code/dist/docsify-copy-code.min.js"></script>



</body>
</html>
```

## 侧边栏

- 创建“_sidebar.md”文件；
- 然后在index文件中开启侧边栏；
  - loadSidebar: true  //加载侧边栏；
  - subMaxLevel: 2   //目录显示层级；
- 在“_sidebar.md”文件中写入如下内容：

```html
<!-- docs/_sidebar.md -->

* [首页](/ "首页")
* [01.ERP服务器容灾恢复步骤](docs/ERP服务器容灾恢复步骤.md)
* [02.docsify文档教程手册部署](docs/docsify部署.md)
```

框架会自动解析到文件。

## 顶部导航栏

- 创建“_navbar.md”文件；
- 在index文件中，开启“loadNavbar: true”
- 在“_navbar.md”文件中增加下面的内容，二级导航需要缩进。

```html
<!-- _navbar.md -->

* [首页](/)

* 数通技术
    * [华为HCIE](mddocs/)
    * [思科CCIE](mddocs/)
* Linux运维
    * CentOS基础
    * Shell脚本
    * Linux应用部署
* MySQL技术
* 链接到我
  * [CSDN](https://blog.csdn.net/annita2019)
  * [Github](https://github.com/spokess)
  * [Gitee](https://gitee.com/)
* 友情链接
  * [Docsify](https://docsify.js.org/#/)
  * [博客园](https://www.cnblogs.com/)

```



## 插件

下面部分是插件，存在于index文件中

```html
  </script>
  <!-- <script src="//cdn.jsdelivr.net/npm/docsify@4"></script> -->
    <!-- docsify的js依赖 -->
    <script src="//cdn.jsdelivr.net/npm/docsify/lib/docsify.min.js"></script>
    <!-- emoji表情支持 -->
    <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/emoji.min.js"></script>
    <!-- 图片放大缩小支持 -->
    <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/zoom-image.min.js"></script>
    <!-- 搜索功能支持 -->
    <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/search.min.js"></script>
    <!--在所有的代码块上添加一个简单的Click to copy按钮来允许用户从你的文档中轻易地复制代码-->
    <script src="//cdn.jsdelivr.net/npm/docsify-copy-code/dist/docsify-copy-code.min.js"></script>
```

## 主题

下面部分是主题，存在于index文件中

```html
<link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/vue.css">
```

