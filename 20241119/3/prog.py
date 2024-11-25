class Vowel:
    __slots__ = 'a', 'e', 'i', 'o', 'u', 'y'
    answer=42

    def __init__(self, **kwargs):
        self.a = kwargs.get('a')
        self.e = kwargs.get('e')
        self.i = kwargs.get('i')
        self.o = kwargs.get('o')
        self.u = kwargs.get('u')
        self.y = kwargs.get('y')
    
    @property
    def full(self):
        # Проверка на заполненность слотов
        return all(getattr(self, slot) is not None for slot in self.__slots__)
    
    def __setattr__(self, key, value):
        if key not in self.__slots__:
            raise AttributeError(f"'Vowel' object has no attribute 'key'")
        if key == 'answer':
            raise AttributeError("can't set attribute 'answer'")
        if key not in self.__slots__:
            raise AttributeError(f"'Vowel' object has no attribute 'key'")
        
        if value is not None and not isinstance(value, int):
            raise ValueError("Values must be integers")
        
        # Сохраняем значение только если это одна из гласных
        super().__setattr__(key, value)

    def __str__(self):
        result = ', '.join(f"{slot}: {getattr(self, slot)}" for slot in sorted(self.__slots__) if hasattr(self, slot) and getattr(self, slot) is not None)
        return result if result else "no vowels"
import sys
exec(sys.stdin.read())