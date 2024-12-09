
class Point: 
    def __init__(self, _id, value): 
        self.id = _id 
        self.value = value 

    def dim_count(self): 
        return len(self.value) 

    def at(self, i): 
        return self.value[i]
        