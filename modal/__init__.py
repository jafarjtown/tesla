from dataclasses import dataclass
from datetime import datetime
from tesla.database.jsondb import JsonDB
import uuid


def ModalId():
    cache = {}
    def generate(modal):
         
        if modal in cache.keys():
             
            cache[modal] += 1
            return  cache[modal]
        cache[modal] = 1
        return 1
    return generate

id_gener = ModalId()

class ModalObject:
    def __init__(self, obj):
        self.obj = obj


    def filter(self, **kwargs):
        pass

    def get(self, **kwargs):
        return self.obj.get(**kwargs)
        

class Modal:

    @classmethod
    def get(cls, **kwargs):
        # print(dir(cls))
        db = JsonDB(collection = cls.__name__ + "/") 
        return db.get(kwargs)

    @classmethod
    def filter(cls, **kwargs):
        # print(dir(cls))
        db = JsonDB(collection = cls.__name__ + "/") 
        return db.filter(kwargs)   

    @classmethod
    def all(cls, **kwargs):
        # print(dir(cls))
        db = JsonDB(collection = cls.__name__ + "/") 
        return db.all()       
    
    @property
    def db(self):
        return JsonDB(collection = self.modal_name() + "/") 

    def modal_name(self):
        return (self.__class__.__name__)

    def save(self):
        data = self.__dict__
        self.id = str(uuid.uuid4())
        data['timestamp'] = str(datetime.now())
        return self.db.create_column(model = data, table_name = str(self.id))


        

class Field:
    def __init__(self, verbose_name: str, max_length: int, unique: bool = False, default = None):
        self.verbose_name = verbose_name
        self.max_length = max_length
        self.unique = unique
    
    def __str__(self):
        return self.verbose_name

    def value(self):
        pass

class CharField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = str

    def title(self):
        return self.value.title()



