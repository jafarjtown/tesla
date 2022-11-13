from dataclasses import dataclass
from tesla.pyhtml.tags import CT

@dataclass
class Form:

    def save(self):
        fields = self.fields()
        print(self.html())
    
    def fields(self):

        return self.__dict__

    def html(self):
        return ''.join(map(lambda f: f.field(), self.fields().values()))

    def __repr__(self):
        return self.html()

    def __str__(self):
        return (self.html())
        
    

 



@dataclass
class Field:
    placeholder : str = 'Input'
    type : str = 'text'
    name : str = 'name'
    label: bool = True
    label_text : str = ''
    

    def __str__(self):
        return  self.field()

    def __repr__(self):
        return self.__str__()
    
    def field(self):
        input = CT('input', type=self.type, placeholder = self.placeholder, name=self.name)
        if self.label:
            if self.label_text == '':
                self.label_text = self.name
            input = CT('label', self.label_text ,input)
        return (input.html())
