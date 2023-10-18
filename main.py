class Student:
    def __init__(self, name, age, grade, power):
        self.name = name
        self.age = age
        self.grade = grade
        self.power = power

    def vrezat_vliso(self, other):
        if self.grade == other.grade:
            print(f'{other.name}, я тибя бить не буду, мыэ кенты')
        elif self.name[0] == other.name[0]:
            print(f'{other.name}, я тибя бить не буду, мыэ кенты')
        elif self.power >= other.power:
            print(f'{other.name}, я тибе сейчас набью лицо')
        elif self.age >= other.age:
            print(f'{other.name}, я тибе сейчас набью лицо')
        else:
            print(f'{other.name}, ты мине сейчас набьёшь лицо')


student1 = Student("Даня", 16, 1, 100)
student2 = Student("Ваня", 16, 1, 10)
student3 = Student("Ибрагим", 16, 23, 120)
student4 = Student("Дамирчик", 16, 42, 50)
student5 = Student("Инакентий", 20, 42, 101)

student1.vrezat_vliso(student2)
student1.vrezat_vliso(student3)
student1.vrezat_vliso(student4)
student1.vrezat_vliso(student5)