class Animal:
    # 类属性
    type = "动物"

    # 有参初始化方法
    def __init__(self, name, food):
        self.name = name  # 实例属性
        self.food = food  # 实例属性

    # 实例方法
    def eat(self):
        print(f"{self.name}爱吃{self.food}")

    # 类方法
    @classmethod
    def change_type(cls, new_type):
        cls.type = new_type

    # 静态方法
    @staticmethod
    def run():
        print("所有动物都会跑")

# 1. 实例化
cat = Animal("波比", "猫条")

# 2. 调用实例属性/方法
print(Animal.type)  # 类属性：动物
print(cat.name)     # 实例属性：波比
cat.eat()           # 实例方法：波比爱吃猫条

# 3. 调用类方法/静态方法
cat.change_type("脊椎动物")
print(Animal.type)  # 类属性修改后：脊椎动物
cat.run()           # 静态方法：所有动物都会跑

# 4. 匿名对象调用
Animal("小鸟", "虫子").eat()  # 小鸟爱吃虫子
