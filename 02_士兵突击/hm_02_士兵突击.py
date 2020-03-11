__author__ = 'cedar'

class Gun:

    def __init__(self, model):
        self.model = model
        self.bullet_count = 0

    def add_bullet(self, count):
        self.bullet_count += count

    def shoot(self, shoot_count=1):
        # 1.如果没子弹，提示装弹
        if self.bullet_count <= 0:
            print('{} 没有子弹！'.format(self.model))
            return

        if self.bullet_count-shoot_count >= 0:
            self.bullet_count -= shoot_count
        else:
            shoot_count = self.bullet_count
            self.bullet_count = 0

        print('{} {} [{}]'.format(self.model,'突' * shoot_count, self.bullet_count))

class Soldier:

    def __init__(self, name):
        self.name = name
        self.gun = None

    def fire(self, add_bullet_count=50, shoot_count=1):

        # 1. 判断有没有枪
        if self.gun == None:
            print('{} 没有枪'.format(self.name))
            return

        # 2. 喊口号
        print('冲啊！！！')

        # 3. 装子弹
        self.gun.add_bullet(add_bullet_count)

        # 4. 开枪
        self.gun.shoot(shoot_count)


xu = Soldier('xu')
xu.gun = Gun('AK47')

xu.fire(5,10)



