# GitBook在Windows下安装部署

参考教程

https://blog.csdn.net/Lowerce/article/details/107579261

https://www.jianshu.com/p/ba34b48d806e

## 一、nodejs安装

建议下载这个版本

https://nodejs.org/dist/v10.21.0/node-v10.21.0-x64.msi

cmd控制台输入： 

```
node -v

C:\Users\Anita>node -v
v10.21.0
```

## 二、安装gitbook

cmd控制台输入：

```
npm install gitbook-cli -g
```

查看gitbook是否安装成功：

```
gitbook -v
```

有的人说会输出gitbook版本号，可是我的这个电脑什么都没有输出。
这样就算安装完成了


### 1、手动创建目录

创建好之后在CMD中切换到这个目录下

```
cd E:\gitbook
```

### 2、创建gitbook空间

```
gitbook init
```

过程：

```
E:\gitbook>gitbook init
Installing GitBook 3.2.3
gitbook@3.2.3 C:\Users\Anita\AppData\Local\Temp\tmp-8912zstxwXVR0vkJ\node_modules\gitbook
├── escape-html@1.0.3
├── destroy@1.0.4
├── escape-string-regexp@1.0.5
├── ignore@3.1.2
├── bash-color@0.0.4
├── gitbook-plugin-livereload@0.0.1
├── cp@0.2.0
├── graceful-fs@4.1.4
├── nunjucks-do@1.0.0
├── github-slugid@1.0.1
├── spawn-cmd@0.0.2
├── q@1.4.1
├── gitbook-plugin-fontsettings@2.0.0
├── is@3.3.0
├── open@0.0.5
├── direction@0.1.5
├── object-path@0.9.2
├── extend@3.0.2
├── json-schema-defaults@0.1.1
├── gitbook-plugin-search@2.2.1
├── jsonschema@1.1.0
├── crc@3.4.0
├── urijs@1.18.0
├── semver@5.1.0
├── front-matter@2.3.0
├── immutable@3.8.2
├── error@7.0.2 (xtend@4.0.2, string-template@0.2.1)
├── tmp@0.0.28 (os-tmpdir@1.0.2)
├── npmi@2.0.1 (semver@4.3.6)
├── send@0.13.2 (fresh@0.3.0, etag@1.7.0, range-parser@1.0.3, statuses@1.2.1, ms@0.7.1, depd@1.1.2, debug@2.2.0, mime@1.3.4, http-errors@1.3.1, on-finished@2.3.0)
├── omit-keys@0.1.0 (isobject@0.2.0, array-difference@0.0.1)
├── dom-serializer@0.1.0 (domelementtype@1.1.3, entities@1.1.2)
├── mkdirp@0.5.1 (minimist@0.0.8)
├── resolve@1.1.7
├── rmdir@1.2.0 (node.flow@1.2.3)
├── fresh-require@1.0.3 (is-require@0.0.1, shallow-copy@0.0.1, sleuth@0.1.1, astw@1.3.0, through2@0.6.5, escodegen@1.14.3, acorn@0.9.0)
├── tiny-lr@0.2.1 (parseurl@1.3.3, livereload-js@2.4.0, qs@5.1.0, debug@2.2.0, body-parser@1.14.2, faye-websocket@0.10.0)
├── js-yaml@3.14.0 (esprima@4.0.1, argparse@1.0.10)
├── cpr@1.1.1 (rimraf@2.4.5)
├── gitbook-plugin-theme-default@1.0.7
├── gitbook-plugin-lunr@1.2.0 (html-entities@1.2.0, lunr@0.5.12)
├── read-installed@4.0.3 (debuglog@1.0.1, util-extend@1.0.3, slide@1.1.6, readdir-scoped-modules@1.1.0, read-package-json@2.1.2)
├── chokidar@1.5.0 (async-each@1.0.3, path-is-absolute@1.0.1, inherits@2.0.4, glob-parent@2.0.0, is-glob@2.0.1, is-binary-path@1.0.1, anymatch@1.3.2, readdirp@2.2.1)
├── nunjucks@2.5.2 (asap@2.0.6, yargs@3.32.0, chokidar@1.7.0)
├── gitbook-plugin-highlight@2.0.2 (highlight.js@9.2.0)
├── moment@2.13.0
├── gitbook-plugin-sharing@1.0.2 (lodash@3.10.1)
├── i18n-t@1.0.1 (lodash@4.17.20)
├── gitbook-markdown@1.3.2 (kramed-text-renderer@0.2.1, gitbook-html@1.3.3, kramed@0.5.6, lodash@4.17.20)
├── gitbook-asciidoc@1.2.2 (gitbook-html@1.3.3, asciidoctor.js@1.5.5-1, lodash@4.17.20)
├── cheerio@0.20.0 (entities@1.1.2, css-select@1.2.0, htmlparser2@3.8.3, jsdom@7.2.2, lodash@4.17.20)
├── request@2.72.0 (aws-sign2@0.6.0, forever-agent@0.6.1, oauth-sign@0.8.2, tunnel-agent@0.4.3, caseless@0.11.0, is-typedarray@1.0.0, stringstream@0.0.6, aws4@1.10.1, isstream@0.1.2, json-stringify-safe@5.0.1, tough-cookie@2.2.2, qs@6.1.2, node-uuid@1.4.8, combined-stream@1.0.8, mime-types@2.1.27, bl@1.1.2, hawk@3.1.3, har-validator@2.0.6, http-signature@1.1.1, form-data@1.0.1)
├── juice@2.0.0 (deep-extend@0.4.2, slick@1.12.2, batch@0.5.3, cssom@0.3.1, commander@2.9.0, cross-spawn-async@2.2.5, web-resource-inliner@2.0.0)
└── npm@3.9.2
warn: no summary file in this book
info: create README.md
info: create SUMMARY.md
info: initialization is finished
```



### 3、编译gitbook

```
E:\gitbook>gitbook build
info: 7 plugins are installed
info: 6 explicitly listed
info: loading plugin "highlight"... OK
info: loading plugin "search"... OK
info: loading plugin "lunr"... OK
info: loading plugin "sharing"... OK
info: loading plugin "fontsettings"... OK
info: loading plugin "theme-default"... OK
info: found 1 pages
info: found 0 asset files
info: >> generation finished with success in 0.5s !
```



### 4、运行gitbook

```
E:\gitbook>gitbook serve
Live reload server started on port: 35729
Press CTRL+C to quit ...

info: 7 plugins are installed
info: loading plugin "livereload"... OK
info: loading plugin "highlight"... OK
info: loading plugin "search"... OK
info: loading plugin "lunr"... OK
info: loading plugin "sharing"... OK
info: loading plugin "fontsettings"... OK
info: loading plugin "theme-default"... OK
info: found 1 pages
info: found 0 asset files
info: >> generation finished with success in 0.5s !

Starting server ...
Serving book on http://localhost:4000
```

这样就OK了



## 三、过程中遇到的坑



### 1、报错一

```
PS E:\gitbook> gitbook init
gitbook : 无法加载文件 C:\Users\Anita\AppData\Roaming\npm\gitbook.ps1，因为在此系统上禁止运行脚本。有关详细信息，请参阅
 https:/go.microsoft.com/fwlink/?LinkID=135170 中的 about_Execution_Policies。
所在位置 行:1 字符: 1
+ gitbook init
+ ~~~~~~~
    + CategoryInfo          : SecurityError: (:) []，PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

解决

以管理员身份运行powerShell

```
set-ExecutionPolicy RemoteSigned
```

敲 A 或者 Y 即可



### 2、报错二

`npm install gitbook-cli -g`过程中反复报错，错误信息如下：

```
TypeError: cb.apply is not a function
```

更新graceful-fs组件并重新尝试安装，尝试过后并没有什么卵用
删除node.js后重新进行全部安装过程，尝试过后并没有什么卵用

我仔细阅读了各个不同时间发布的gitbook安装文章，决定参照一些版本信息更加详细的安装过程进行重试。

==我开始考虑是版本问题的锅==

这次我选择的是nodejs的v10.21.0版本，下载地址：https://nodejs.org/dist/v10.21.0/node-v10.21.0-x64.msi

所有问题全部解决，安装一切顺利。