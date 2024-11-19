class  Sender: 
    f=False
    @classmethod
    def report(cls): 
        print('Get away!' if cls.f else 'Greetings!')
        f=True
class ASker:
    @staticmethod
    def askall(self, lst):
        for i in lst: i.report()

    
