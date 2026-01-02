







## 问题描述

使用期间隔段时间服务就会奔掉。

## 错误日志

```tomcat
2025-12-10 13:36:23 Commons Daemon procrun stderr initialized
Configuration error
java.io.FileNotFoundException: D:\Program Files\s7\conf\logging.properties (系统找不到指定的文件。)
	at java.io.FileInputStream.open(Native Method)
	at java.io.FileInputStream.<init>(FileInputStream.java:138)
	at java.io.FileInputStream.<init>(FileInputStream.java:97)
	at org.apache.juli.ClassLoaderLogManager.readConfiguration(ClassLoaderLogManager.java:466)
	at org.apache.juli.ClassLoaderLogManager.readConfiguration(ClassLoaderLogManager.java:311)
	at java.util.logging.LogManager$2.run(LogManager.java:288)
	at java.util.logging.LogManager$2.run(LogManager.java:286)
	at java.security.AccessController.doPrivileged(Native Method)
	at java.util.logging.LogManager.readPrimordialConfiguration(LogManager.java:286)
	at java.util.logging.LogManager.getLogManager(LogManager.java:268)
	at java.util.logging.Logger.<init>(Logger.java:252)
	at java.util.logging.LogManager$RootLogger.<init>(LogManager.java:1311)
	at java.util.logging.LogManager$RootLogger.<init>(LogManager.java:1309)
	at java.util.logging.LogManager$1.run(LogManager.java:199)
	at java.security.AccessController.doPrivileged(Native Method)
	at java.util.logging.LogManager.<clinit>(LogManager.java:176)
	at java.util.logging.Logger.demandLogger(Logger.java:307)
	at java.util.logging.Logger.getLogger(Logger.java:361)
	at org.apache.juli.logging.impl.Jdk14Logger.getLogger(Jdk14Logger.java:164)
	at org.apache.juli.logging.impl.Jdk14Logger.<init>(Jdk14Logger.java:55)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:57)
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
	at java.lang.reflect.Constructor.newInstance(Constructor.java:525)
	at org.apache.juli.logging.impl.LogFactoryImpl.createLogFromClass(LogFactoryImpl.java:1025)
	at org.apache.juli.logging.impl.LogFactoryImpl.discoverLogImplementation(LogFactoryImpl.java:844)
	at org.apache.juli.logging.impl.LogFactoryImpl.newInstance(LogFactoryImpl.java:541)
	at org.apache.juli.logging.impl.LogFactoryImpl.getInstance(LogFactoryImpl.java:292)
	at org.apache.juli.logging.impl.LogFactoryImpl.getInstance(LogFactoryImpl.java:269)
	at org.apache.juli.logging.LogFactory.getLog(LogFactory.java:657)
	at org.apache.catalina.startup.Bootstrap.<clinit>(Bootstrap.java:59)
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/D:/Program%20Files/s7/webapps/ROOT/WEB-INF/lib/logback-classic-1.0.13.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/D:/Program%20Files/s7/webapps/ROOT/WEB-INF/lib/slf4j-log4j12-1.7.7.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [ch.qos.logback.classic.util.ContextSelectorStaticBinder]
```

你遇到了 Java 程序（看起来是 Tomcat）启动时的两类问题：

1. 是核心的配置文件缺失错误（找不到 logging.properties）
2. 二是 SLF4J 日志框架存在多绑定的警告，我会帮你逐一解决。

## 问题 1：logging.properties 文件缺失（核心错误）

这个错误是导致程序启动配置失败的主要原因，JVM 在初始化日志系统时，找不到指定路径下的`logging.properties`配置文件。

#### 解决方案

1. **检查并创建目录**首先确认路径 `D:\Program Files\s7\conf\` 是否存在：

   - 如果不存在，手动创建 `conf` 文件夹（在 `D:\Program Files\s7\` 目录下新建文件夹，命名为 `conf`）。

2. **添加 logging.properties 文件**你需要在 `D:\Program Files\s7\conf\` 目录下放入 Tomcat 默认的`logging.properties`文件，有两种方式：

   - **方式 1（推荐）**：从正常的 Tomcat 安装包的`conf`目录中复制`logging.properties`文件到该路径。
   - **方式 2**：手动创建基础版的`logging.properties`，内容如下（可直接复制使用）：

   ```properties
   handlers = 1catalina.org.apache.juli.FileHandler, java.util.logging.ConsoleHandler
   
   .level = INFO
   
   ############################################################
   # Handler specific properties.
   # Describes specific configuration info for Handlers.
   ############################################################
   
   1catalina.org.apache.juli.FileHandler.level = FINE
   1catalina.org.apache.juli.FileHandler.directory = ${catalina.base}/logs
   1catalina.org.apache.juli.FileHandler.prefix = catalina.
   
   java.util.logging.ConsoleHandler.level = FINE
   java.util.logging.ConsoleHandler.formatter = java.util.logging.SimpleFormatter
   
   ############################################################
   # Facility specific properties.
   # Provides extra control for each logger.
   ############################################################
   
   org.apache.catalina.core.ContainerBase.[Catalina].[localhost].level = INFO
   org.apache.catalina.core.ContainerBase.[Catalina].[localhost].handlers = 2localhost.org.apache.juli.FileHandler
   
   2localhost.org.apache.juli.FileHandler.level = FINE
   2localhost.org.apache.juli.FileHandler.directory = ${catalina.base}/logs
   2localhost.org.apache.juli.FileHandler.prefix = localhost.
   
   org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/manager].level = INFO
   org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/manager].handlers = 3manager.org.apache.juli.FileHandler
   
   3manager.org.apache.juli.FileHandler.level = FINE
   3manager.org.apache.juli.FileHandler.directory = ${catalina.base}/logs
   3manager.org.apache.juli.FileHandler.prefix = manager.
   
   org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/host-manager].level = INFO
   org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/host-manager].handlers = 4host-manager.org.apache.juli.FileHandler
   
   4host-manager.org.apache.juli.FileHandler.level = FINE
   4host-manager.org.apache.juli.FileHandler.directory = ${catalina.base}/logs
   4host-manager.org.apache.juli.FileHandler.prefix = host-manager.
   
   java.util.logging.SimpleFormatter.format = %1$tY-%1$tm-%1$td %1$tH:%1$tM:%1$tS %4$s %2$s %5$s%6$s%n
   
   org.apache.jasper.compiler.TldLocationsCache.level = WARNING
   org.apache.catalina.startup.ContextConfig.level = WARNING
   org.apache.catalina.startup.TldConfig.level = WARNING
   org.apache.catalina.core.StandardContext.level = INFO
   ```

## 问题 2：SLF4J 多绑定警告

这个是警告（非致命错误），但会导致日志行为可能不符合预期 —— 你的项目中同时引入了`logback`和`log4j`两种 SLF4J 的实现包，SLF4J 只能选择其中一个生效（日志显示实际用的是 logback）。

#### 解决方案：

清理多余的日志绑定包，只保留一个即可：

1. 找到路径 `D:/Program Files/s7/webapps/ROOT/WEB-INF/lib/`。
2. 删除其中的 `slf4j-log4j12-1.7.7.jar` 文件（保留 logback 相关包即可）。
3. 重启程序，该警告会消失。

### 验证修复效果

1. 完成上述两个问题的修复后，重新启动你的 Java 程序（Tomcat）。
2. 检查启动日志：
   - 不再出现 `FileNotFoundException: logging.properties` 错误；
   - SLF4J 的多绑定警告消失；
   - 程序能正常启动。

### 总结

1. **核心错误解决**：在`D:\Program Files\s7\conf\`目录下创建 / 放入`logging.properties`文件，解决文件缺失问题。
2. **警告解决**：删除`WEB-INF/lib`下的`slf4j-log4j12-1.7.7.jar`，消除 SLF4J 多绑定冲突。
3. 修复后重启程序，验证日志无核心错误、警告（可选）消失即为修复成功。