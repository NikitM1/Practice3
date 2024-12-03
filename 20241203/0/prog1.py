class sole:
    def __new__( metacls, name, parents, ns):
        if len(parents)>1: 
            raise TypeErroe("Can't have more than one parent")
        return super().__new__(metacls, name, parents, ns)
