# 零基础学习 Vue 教程（Vue 3 + Vite 版）
Vue 是一套用于构建用户界面的**渐进式 JavaScript 框架**，Vue 3 是目前的主流版本，搭配 Vite 构建工具可以大幅提升开发效率。本教程从环境搭建到核心语法，带你零基础入门 Vue。

## 一、前置知识（建议掌握）
1.  **HTML**：熟悉标签、属性、表单元素等基础结构
2.  **CSS**：掌握选择器、盒模型、Flex/Grid 布局
3.  **JavaScript 基础**：变量、函数、数组、对象、箭头函数、Promise、ES6 模块化（`import/export`）

> 提示：如果 JS 基础薄弱，先花 1-2 周补一下 ES6 核心语法，再学 Vue 会更轻松。

## 二、环境搭建
### 1. 安装 Node.js
Vue 项目依赖 Node.js 的包管理工具 `npm` 或 `yarn`，必须先安装 Node.js。
- 下载地址：[Node.js 官网](https://nodejs.org/zh-cn/)
- 选择 **LTS 长期支持版**安装，安装完成后打开命令行（CMD/PowerShell/终端），输入以下命令验证：
  ```bash
  node -v  # 查看 Node 版本，出现版本号即为成功
  npm -v   # 查看 npm 版本
  ```

### 2. 创建 Vue 3 项目（Vite 版）
Vite 是 Vue 官方推荐的新一代构建工具，比传统的 Webpack 更快。
1.  打开命令行，进入你想存放项目的文件夹，执行创建命令：
    ```bash
    npm create vite@latest my-vue-app -- --template vue
    ```
    - `my-vue-app` 是你的项目名称，可以自定义
    - `--template vue` 指定模板为 Vue 3

2.  进入项目目录并安装依赖
    ```bash
    cd my-vue-app  # 进入项目文件夹
    npm install    # 安装项目依赖
    ```

3.  启动开发服务器
    ```bash
    npm run dev
    ```
    启动成功后，浏览器访问命令行提示的地址（一般是 `http://localhost:5173/`），就能看到 Vue 的默认页面。

### 3. 开发工具推荐
- **VS Code**：免费轻量的代码编辑器，下载地址：[VS Code 官网](https://code.visualstudio.com/)
- **必装插件**：
  - Volar：Vue 官方推荐的语法高亮、智能提示插件（替代旧版 Vetur）
  - JavaScript and TypeScript Nightly：增强 TS/JS 语法支持

## 三、Vue 核心语法（从基础到进阶）
### 1. 项目目录结构（核心文件说明）
```
my-vue-app/
├── node_modules/  # 项目依赖包
├── public/        # 静态资源（不会被 Vite 处理）
├── src/           # 核心代码目录
│   ├── assets/    # 静态资源（会被 Vite 处理，如图片、CSS）
│   ├── components/# 组件文件夹（可复用的 Vue 组件）
│   ├── App.vue    # 根组件
│   └── main.js    # 入口文件（创建 Vue 实例，挂载到页面）
├── index.html     # 单页面入口
├── package.json   # 项目配置和依赖清单
└── vite.config.js # Vite 配置文件
```

### 2. 第一个 Vue 组件（App.vue）
Vue 组件的后缀是 `.vue`，一个组件由 **3 个部分**组成：
```vue
<template>
  <!-- 1. 模板区域：HTML 结构，必须有且只有一个根元素 -->
  <div class="hello">
    <h1>{{ msg }}</h1>
    <button @click="changeMsg">点击修改文字</button>
  </div>
</template>

<script setup>
// 2. 脚本区域：JavaScript 逻辑，setup 是 Vue 3 的语法糖
// 响应式数据：用 ref 定义基本类型的响应式变量
import { ref } from 'vue'

// 定义响应式变量 msg
const msg = ref('Hello Vue 3!')

// 定义点击事件函数
const changeMsg = () => {
  msg.value = '你好，Vue！'  // ref 定义的变量，修改值需要加 .value
}
</script>

<style scoped>
/* 3. 样式区域：CSS 样式，scoped 表示样式只作用于当前组件 */
.hello {
  text-align: center;
  margin-top: 40px;
}
button {
  padding: 8px 16px;
  margin-top: 20px;
  cursor: pointer;
}
</style>
```
核心知识点：
- **插值表达式 `{{ }}`**：用于在模板中显示变量的值
- **`script setup`**：Vue 3 推荐的写法，无需手动注册组件和导出变量
- **响应式数据 `ref`**：用于定义字符串、数字、布尔等**基本类型**的响应式数据
- **事件绑定 `@click`**：`@` 是 `v-on` 的简写，用于绑定事件

### 3. 核心指令（Vue 的特色语法）
指令是 Vue 提供的**带有 `v-` 前缀的特殊属性**，用于操作 DOM。

![image-20260113181500845](./零基础学习Vue教程(Vue3+Vite版).assets/image-20260113181500845.png)

**示例：指令综合使用**
```vue
<template>
  <div>
    <!-- 双向绑定：输入框内容同步到 username 变量 -->
    <input v-model="username" placeholder="请输入用户名">
    <p>你输入的是：{{ username }}</p>

    <!-- 条件渲染 -->
    <div v-if="username.length > 5">用户名长度合格</div>
    <div v-else>用户名太短啦</div>

    <!-- 列表渲染 -->
    <ul>
      <li v-for="(item, index) in fruitList" :key="index">
        {{ index + 1 }}. {{ item }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const username = ref('')
const fruitList = ref(['苹果', '香蕉', '橙子'])
</script>
```

### 4. 响应式数据进阶（`ref` vs `reactive`）
Vue 3 有两种定义响应式数据的方式：
| 类型 | 适用场景 | 特点 |
|------|----------|------|
| `ref` | 基本类型（字符串、数字、布尔） | 修改值需要 `.value`，模板中可省略 |
| `reactive` | 复杂类型（对象、数组） | 直接修改属性，无需 `.value` |

**`reactive` 示例**
```vue
<template>
  <div>
    <p>姓名：{{ user.name }}</p>
    <p>年龄：{{ user.age }}</p>
    <button @click="updateUser">修改用户信息</button>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
// 定义复杂对象的响应式数据
const user = reactive({
  name: '张三',
  age: 20
})

const updateUser = () => {
  // 直接修改属性，无需 .value
  user.name = '李四'
  user.age += 1
}
</script>
```

### 5. 组件通信（父子组件传值）
在 Vue 中，组件是可复用的，大型项目会拆分成多个组件，组件之间需要传递数据。

#### （1）父组件向子组件传值（`props`）
步骤 1：创建子组件 `src/components/Child.vue`
```vue
<template>
  <div class="child">
    <h3>我是子组件</h3>
    <p>父组件传来的标题：{{ title }}</p>
    <p>父组件传来的用户信息：{{ user.name }}</p>
  </div>
</template>

<script setup>
// 定义 props，接收父组件传递的数据
const props = defineProps({
  title: String, // 指定类型为字符串
  user: {
    type: Object,
    required: true // 必填项
  }
})
</script>

<style scoped>
.child {
  border: 1px solid #ccc;
  padding: 20px;
  margin-top: 20px;
}
</style>
```
步骤 2：在父组件（App.vue）中使用子组件并传值
```vue
<template>
  <div class="parent">
    <h2>我是父组件</h2>
    <!-- 父组件传值给子组件：用 v-bind 绑定 props -->
    <Child :title="parentTitle" :user="parentUser" />
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
// 1. 导入子组件
import Child from './components/Child.vue'

// 2. 定义要传递的数据
const parentTitle = ref('父组件的标题')
const parentUser = reactive({
  name: '张三',
  age: 20
})
</script>
```

#### （2）子组件向父组件传值（`emit`）
子组件不能直接修改父组件的数据，需要通过**触发事件**的方式通知父组件。
修改 `Child.vue`，添加一个按钮触发事件：
```vue
<template>
  <div class="child">
    <button @click="sendMsgToParent">向父组件发送消息</button>
  </div>
</template>

<script setup>
// 定义要触发的事件
const emit = defineEmits(['childMsg'])

const sendMsgToParent = () => {
  // 触发事件，并传递数据
  emit('childMsg', '我是子组件发来的消息')
}
</script>
```
在父组件中监听子组件的事件：
```vue
<template>
  <div class="parent">
    <p>子组件传来的消息：{{ childMsg }}</p>
    <!-- 监听子组件的 childMsg 事件 -->
    <Child @childMsg="handleChildMsg" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Child from './components/Child.vue'

const childMsg = ref('')
// 接收子组件的消息
const handleChildMsg = (msg) => {
  childMsg.value = msg
}
</script>
```

### 6. 生命周期钩子
Vue 组件从创建到销毁的过程称为**生命周期**，我们可以通过钩子函数在不同阶段执行代码。
Vue 3 中常用的生命周期钩子（在 `script setup` 中直接使用）：

| 钩子函数 | 执行时机 |
|----------|----------|
| `onMounted` | 组件挂载到 DOM 后执行（常用：获取 DOM、发起网络请求） |
| `onUpdated` | 组件数据更新后执行 |
| `onUnmounted` | 组件被销毁后执行（常用：清除定时器、取消监听） |

**示例：发起网络请求**
```vue
<template>
  <div>
    <p v-for="item in list" :key="item.id">{{ item.title }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
// 假设用 axios 发起请求，需要先安装：npm install axios
import axios from 'axios'

const list = ref([])

// 组件挂载后发起请求
onMounted(async () => {
  const res = await axios.get('https://jsonplaceholder.typicode.com/todos')
  list.value = res.data.slice(0, 5) // 取前 5 条数据
})
</script>
```

## 四、进阶学习方向
1.  **Vue Router**：实现单页面应用的路由跳转（不同 URL 对应不同组件）
2.  **Pinia**：Vue 官方推荐的状态管理库，用于管理全局共享数据（替代旧版 Vuex）
3.  **Element Plus**：基于 Vue 3 的 UI 组件库（快速搭建后台管理系统）
4.  **TypeScript**：结合 TS 开发，提升代码的可维护性
5.  **打包部署**：通过 `npm run build` 打包项目，部署到 Nginx 或云服务器

## 五、学习资源推荐
1.  **官方文档**：[Vue 3 官方文档](https://cn.vuejs.org/guide/introduction.html)（最权威，建议反复看）
2.  **视频教程**：B站搜索「Vue 3 零基础教程」，推荐尚硅谷、黑马程序员的免费视频
3.  **实战项目**：从 TodoList → 博客系统 → 后台管理系统，一步步积累经验

---

是否需要我帮你整理**Vue 3 常用 API 速查表**，方便你学习时随时查阅？