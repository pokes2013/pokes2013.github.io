# FineReport教程

需求：ERP运维实施需求，用于报表开发，打印模板

教程地址：[FineReport报表工程师从入门到精通](https://www.bilibili.com/video/BV1i9jdzrETM/?spm_id_from=333.337.search-card.all.click&vd_source=9dc23d072b0edbf78ffed52f1fcb2318)

‍

## 开发商

官网地址：https://www.finereport.com/

提供商介绍：帆软（FanRuan） 是中国领先的商业智能（BI）和数据分析软件提供商，专注于为企业提供数据可视化、报表工具和大数据分析解决方案。以下是关于帆软的主要信息：

核心产品

- FineReport  
  专业的企业级报表工具，支持快速制作各类复杂报表、大屏可视化、移动端报表等。  
  特点：拖拽式操作、多数据源整合、强大的打印导出功能。  
  适用场景：财务、生产、销售等固定报表需求。  
- FineBI  
  自助式BI工具，面向业务人员，支持数据探索、动态分析和交互式仪表板。  
  特点：自助分析、实时计算、AI辅助建模（如智能预测）。  
  适用场景：业务部门自主分析、敏捷决策。  
- 简道云  
  低代码应用搭建平台，无需编程即可创建表单、流程管理和数据应用。  
  适用场景：OA、CRM、进销存等个性化管理系统。

‍

## FineReport的常用词汇



## 2. 设计器



|                             名词                             |                             释义                             |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| [普通报表](https://help.fanruan.com/finereport/doc-view-129.html) | 保存的文件类型为 cpt，依靠着单元格的扩展与父子格的关系来实现模板效果，可进行参数查询，填报报表，图表设计等等，但是在分页预览模式下不能在报表主体中展示控件，而且单元格间相互影响，很难保持独立性 |
| [FineVis数据可视化](https://help.fanruan.com/finereport/doc-view-4222.html) | 又名 FVS 可视化看板，专注于数据可视化，制作过程所见即所得。力图用便捷、专业的产品化方式满足参观、监控、汇报等可视化看板需求 |
| [聚合报表](https://help.fanruan.com/finereport/doc-view-132.html) | 一般适用于一张模板中显示多个独立模块的报表，每一块都类似一张单独的报表或者一张图表，块与块之间相对独立，互不影响 |
| [决策报表](https://help.fanruan.com/finereport/doc-view-432.htm) | 保存的文件类型为 frm，自由灵活的设计风格，可以说其专为大屏和移动端而生，可制作画面美观、内容丰富的管理驾驶舱，制作在手机、平板等移动设备端查看的敏捷报表 |
| [Word 报告](https://help.fanruan.com/finereport/doc-view-4270.html) | 基于 Word 加入动态数据、表格、图表进行报告设计，实现报告数据实时变化。详细介绍请参考：[Word 报告](https://help.fanruan.com/finereport/doc-view-4270.html) |
| [分页预览](https://help.fanruan.com/finereport/doc-view-135.html) | 是 FineReport 的默认预览方式，当模板中的数据内容无法在一页内展示时会自动分页，一般在只需要查看报表数据时使用 |
| [填报预览](https://help.fanruan.com/finereport/doc-view-136.html) | 指在 Web 端预览用来填报数据的模板，一般在只需要录入修改数据的时候使用，也可用来查看数据 |
| [数据分析](https://help.fanruan.com/finereport/doc-view-1545.html) | 指在预览模板时可以对数据进行简单的分析操作，包括：排序、条件筛选、列表筛选 |
| [移动端预览](https://help.fanruan.com/finereport/doc-view-2432.html) | 指通过扫码直接在手机上展现报表，让用户直观地看到当前设计模板的实际效果 |
| [开发者调试](https://help.fanruan.com/finereport/doc-view-4280.html) |          指新版决策报表可以在浏览器中调整模板的布局          |
|                          PC 端预览                           |     针对于决策报表设计模式而言，指在 Web 端预览决策报表      |
| [工作目录](https://help.fanruan.com/finereport/doc-view-195.html) | 工作目录是指当前设计器所工作的工程。工作目录又分为「本地目录」和「远程服务器」。「本地目录」指从官网下载安装的设计器中已内置的 Tomcat 服务器。「远程服务器」指使用远程设计或者将 FineReport 报表工程部署到其他服务器上时所使用的另外创建的一个工程 |
|                          单元格元素                          | 指在单元格内插入的内容，可以插入数据列、普通文本、富文本、公式、图表、图片、斜线、子报表 |
|                           悬浮元素                           | 指插入的内容悬浮于报表主体上面，可以插入普通文本、公式、图表、图片 |
| [富文本](https://help.fanruan.com/finereport/doc-view-1171.html) | 指多文本格式，可以对字体进行样式设置的一种文本。一个单元格中所有内容只能设置一种样式，通过富文本可将一个单元格中的内容设置不同的样式 |
| [扩展](https://help.fanruan.com/finereport/doc-view-140.html) | 指数据集中的字段拖入到单元格后数据的扩展方向。可分为：1）纵向扩展：单元格中字段的数据纵向扩展，在不同单元格中展示2）横向扩展：单元格中字段的数据横向扩展，在不同单元格中展示3）不扩展：单元格中字段的数据不扩展，所有数据在一个单元格中展示 |
| [父子格](https://help.fanruan.com/finereport/doc-view-141.html) | 单元格中的数据列在进行扩展的过程中存在相互关联的关系。单元格进行扩展的过程中，在无父格的情况下，相对于其右（下）边的单元格而言，扩展格是主动复制的，被称为其他格（其右/下的格）的父格，而其右（下）的单元格是被动跟随复制的，被称为扩展格的子格。父格和子格是相对的概念，即某格是另一格的父格或子格，不存在单独的父格或子格。 从父格的定义中看，显然只有扩展格才能是其他格的父格 |
|                            左父格                            |      单元格进行纵向扩展时，我们称其为其右边格子的左主格      |
|                            上父格                            |     单元格进行横向扩展时，我们又称其为其下边格子的上主格     |
|                            最父格                            | 严格来说要分为「最左父格」和「最上父格」，指父子格关系上面的最左或最上。最父格必满足以下特点：1）存在跟随其扩展的子单元格，也就是有单元格以它为父格2）最父格自身是没有父格的，所以其扩展不受其他单元格影响 |
| [可伸展性](https://help.fanruan.com/finereport/doc-view-154.html) | 可伸展性指单元格中的数据在扩展时，其对应的父格可随数据的扩展而进行伸展使得父格中的内容居中或者靠左靠右显示。可分为：1）纵向可伸展：数据从上到下纵向扩展时，可以设置扩展格左侧单元格的纵向可伸展性2）横向可伸展：数据从左到右横向扩展时，可以设置扩展格上方单元格的横向可伸展性 |
|                         单元格实际值                         |                      是指单元格实际的值                      |
|                         单元格显示值                         |         指对实际值进行形态和样式设置后显示在页面的值         |
| [数据字典](https://help.fanruan.com/finereport/doc-view-219.html) | 在原始数据当中，保存的是编码性质的数据，而在数据呈现时，需要显示的是有意义的值，即根据编码表显示相应的数据，这个编码表就是「数据字典」 |
| [内容提示](https://help.fanruan.com/finereport/doc-view-227.html) | 类似于 Word 里面的注释，当我们将鼠标移动到相应单元格时，会弹出对应的注释 |
|                         跟随页面设置                         | 当前单元格，Web 端展示以及打印导出时，根据内容的多少，自动调整行高和列宽，显示全部内容 |
|                          不自动调整                          | 当前单元格，Web 端展示以及打印导出时，以设计器中实际大小展示，单元格中的内容，截取显示 |
|                         自动调整行高                         | 当前单元格，设计器中的大小不足以摆放下全部文字时，Web 端展示以及打印导出时，将保持列宽不变，根据内容的多少，自动调整行高，显示全部内容 |
|                         自动调整列宽                         | 当前单元格，设计器中的大小不足以摆放下全部文字时，Web 端展示以及打印导出时，将保持行高不变，根据内容的多少，自动调整列宽，显示全部内容 |
|                           行前分页                           |     每页显示固定的行数后分页，在指定的行前对数据进行分页     |
|                           行后分页                           |     每页显示固定的行数后分页，在指定的行后对数据进行分页     |
|                           列前分页                           |     每页显示固定的列数后分页，在指定的列前对数据进行分页     |
|                           列后分页                           |     每页显示固定的列数后分页，在指定的列后对数据进行分页     |
|                          分页时断开                          | 要是为合并格服务的，当分页断开正好位于合并格的中间时，合并格里的值是否拆分后在两页里显示 |
|                            不分栏                            |                 指数据全部纵向排列或横向排列                 |
|                            行分栏                            |            指分栏的数据超过固定的行就另起一栏显示            |
|                            列分栏                            |                 指超过固定的列就另起一栏显示                 |
| [卡片分栏](https://help.fanruan.com/finereport/doc-view-354.html) | 信息以卡片的形式在页面显示，每个卡片均有大标题和表头，并且各卡片之间有空行或空列进行分割 |
|                           普通分组                           |             将数据列中相同项合并为一组显示的方式             |
|                         相邻连续分组                         |            只将连在一起的相同数据才进行合并的方式            |
|                           高级分组                           |         可分为条件分组和公式分组，可自定义分组的条件         |
| [模板 Web 属性](https://help.fanruan.com/finereport/doc-view-1228.html) | 指模板在浏览器中预览时所需要设置的基本属性，设置模板基本属性、打印机属性、分页预览设置、填报页面设置、数据分析设置、浏览器背景、引用CSS 或 引用JavaScript |
|                            自适应                            | 指用户在 PC 端或移动端预览模板时，模板能够根据屏幕分辨率自适应。详细介绍请参见：[PC端自适应属性](https://help.fanruan.com/finereport/doc-view-788.html) ，[［通用］移动端自适应](https://help.fanruan.com/finereport/doc-view-575.html) |
| [超级链接](https://help.fanruan.com/finereport/doc-view-223.html) | 可以实现打开一个网页，钻取另一张报表，发送电子邮件，下载文件，数据排序，结合传参实现联动等效果的链接 |
|                             参数                             | 指在设置或赋值不同的数值来实现一个目标结果，这些数值就是参数。参数的主要作用是实现用户与数据的实时交互，即进行数据的过滤 |
| [模板参数](https://help.fanruan.com/finereport/doc-view-157.html) | 模板参数是指在当前模板下创建的参数，只有当前报表可以使用该参数来设计报表，且必须与过滤条件结合筛选数据 |
| [全局参数](https://help.fanruan.com/finereport/doc-view-159.html) | 全局参数是在当前报表工程下创建的参数，前报表工程下的所有报表都可以使用该参数来设计报表，必须与过滤条件结合筛选数据。详细介绍请查看：[全局参数](http://help.finereport.com/doc-view-159.htm) |
| [数据集参数](https://help.fanruan.com/finereport/doc-view-158.html) | 新建数据集时，在 SQL 查询语句中定义数据集参数，直接在数据查询时就完成数据的过滤操作。数据集参数根据使用范围不同分为模板数据集参数和服务器数据集参数 |

## 3. 数据准备

|                             名词                             |                           **释义**                           |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| [数据连接](https://help.fanruan.com/finereport/doc-view-100.html) | 指建立 FineReport 产品与数据库的连接，让 FineReport 能获取到数据库中的数据 |
| [数据集](https://help.fanruan.com/finereport/doc-view-106.html) | 指可直接应用于模板设计的数据展现集合。按其来源范围数据集可以分为数据库查询 ， 内置数据集 ， 文件数据集 ， SAP 数据集， 存储过程 ， 多维数据库 ，关联数据集 以及 树数据集 |
| [数据库查询](https://help.fanruan.com/finereport/doc-view-107.html) | 对数据源中的数据库表，直接使用 SQL 语句，来选择所需要的数据字段 |
| [内置数据集](https://help.fanruan.com/finereport/doc-view-109.html) |  指新建一个类似数据库表的原表，可作为模板的数据源来设计报表  |
| [文件数据集](https://help.fanruan.com/finereport/doc-view-1244.html) | 指以 txt 文本文件、Excel 文件和 XML 文件中的数据为数据集，将这些文件中的数据加载进行，并以二维表的结构展示在数据集当中，以供模板使用 |
| [SAP数据集](https://help.fanruan.com/finereport/doc-view-119.html) |     建立一个 SAP 数据连接，通过该数据连接建立 SAP 数据集     |
| [存储过程](https://help.fanruan.com/finereport/doc-view-117.html) | 直接将存储过程作为数据集，不需要在数据库查询而是去调用存储过程 |
| [多维数据库](https://help.fanruan.com/finereport/doc-view-120.html) |     在XMLA 数据连接的基础上，新建多维数据库 XMLA 数据集      |
| [关联数据集](https://help.fanruan.com/finereport/doc-view-125.html) | 在不同的数据源进行筛选取数或访问不同的数据库；利用来自不同的数据源形成一个数据集 |
| [树数据集](https://help.fanruan.com/finereport/doc-view-126.html) |  指控件绑定树数据集， Web 端查看时就会自动生成树形层级结构   |

## 4. 控件

|                             名词                             |                           **释义**                           |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| [文本控件](https://help.fanruan.com/finereport/doc-view-254.html) |      主要用于昵称、名称等填写，用户按照规则要求输入即可      |
| [文本域控件](https://help.fanruan.com/finereport/doc-view-266.html) | 文本域控件支持换行符，当用户需要输入或编辑长字符串时可使用该控件 |
| [数字控件](https://help.fanruan.com/finereport/doc-view-259.html) |         可通过该控件输入数字信息（整数、负数、小数）         |
| [密码控件](https://help.fanruan.com/finereport/doc-view-267.html) |              可通过该控件输入密码信息，录入密码              |
| [按钮控件](https://help.fanruan.com/finereport/doc-view-265.html) | 可通过该控件执行提交、插入行、删除行、树节点展开与关闭等操作 |
| [复选按钮控件](https://help.fanruan.com/finereport/doc-view-257.html) |                 可通过该控件执行批量选中操作                 |
| [单选按钮组控件](https://help.fanruan.com/finereport/doc-view-262.html) |       当选项数量小于等于 4 时，一般使用单选按钮组控件        |
| [复选按钮组控件](https://help.fanruan.com/finereport/doc-view-263.html) |         当选项数量大于 4 时，一般使用复选按钮组控件          |
| [下拉框控件](https://help.fanruan.com/finereport/doc-view-255.html) |  通过该控件下拉选择某个选项信息，录入或查询数据，仅支持单选  |
| [下拉复选框控件](https://help.fanruan.com/finereport/doc-view-256.html) |   通过该控件下拉选择多个选项信息，录入或查询数据，支持多选   |
| [日期控件](https://help.fanruan.com/finereport/doc-view-258.html) |  当用户需要输入一个时间，使用日期控件，弹出时间面板进行选择  |
| [下拉树控件](https://help.fanruan.com/finereport/doc-view-260.html) |    可通过该控件选择具有多层树状结构的数据，录入或查询数据    |
| [视图树控件](https://help.fanruan.com/finereport/doc-view-261.html) |    可通过该控件选择具有多层树状结构的数据，录入或查询数据    |
| [文件控件](https://help.fanruan.com/finereport/doc-view-264.html) |                     可通过该控件上传文件                     |
| [列表控件](https://help.fanruan.com/finereport/doc-view-1859.html) |                 可通过该控件选择单条数据信息                 |
| [网页框控件](https://help.fanruan.com/finereport/doc-view-3491.html) |          可通过该控件在报表页面中嵌入其他网页或报表          |
| [标签控件](https://help.fanruan.com/finereport/doc-view-4655.html) |          可通过标签控件给控件的「标签名称」进行赋值          |
|                           查询按钮                           |                     点击该按钮后查询数据                     |
| [预定义控件](https://help.fanruan.com/finereport/doc-view-240.html) |        一般应用于定义比较复杂且需要重复使用控件的地方        |
