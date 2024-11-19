class Age: 
    def __init__(self): 
        self.age=None
    @property
    def age(self): 
        if self.age==42: 
            print('secret value!'); return -1
        else: return self.age 
    @age.setter
    def age(self, val): 
        if val>128: 
            raise ValueError('too old')
        else: self.age=val 