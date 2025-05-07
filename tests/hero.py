class Hero:
    def __init__(self, damage, monster):
        self.damage = damage
        self.monster = monster

    def attack(self):
        self.monster.get_damage(self.damage)




class Monster:
    def __init__(self, health):
        self.health = health


    def get_damage(self, amount):
        self.health -= amount


monster = Monster()

hero = Hero(10, Monster(100))