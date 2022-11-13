from dataclasses import dataclass, field
import os
import json
import random as rn
from uuid import uuid4 as v4
import copy
# sorted
from tesla.database.jsondb.schema import User, settype

def Contains(column, obj):
    r = {}
    #print(obj)
    for k in obj.keys():
        r[k] = False
        if column[k] == obj[k]:
            r[k] = True
    for c in list(r.values()):
        if c == False:
            return False
    return True

def GreaterThan(columns, obj, k, op):
    key = k.find(f"__{op}t")
    #print(k)
   # print(columns["age"] > obj[k], columns)
    if op == 'g':
         statement = columns[k[:key]] > obj[k]
    else:
        statement = columns[k[:key]] < obj[k]
    #print(statement)
    if statement:
        
        o = {}
        for ky, v in obj.items():
           
            if ky.find(f"__{op}t") != -1:
                o[ky[:key]] = columns[k[:key]]
            else:
              o[ky] = v
             
            #print(o)
        return columns, o, True
        pass
    return columns, obj, False

@dataclass
class ColCache:
    db : dict = field(default_factory=dict)
    def update(self,collection , key, value):
        if self.db.get(collection):
            self.db[collection][key] = value
        raise Exception(f'No collection with name {collection}')   
    
    def get(self, collection, key=None):
        if key:
            return self.db.get(collection).get(key)
        return self.db.get(collection) 
    def set(self, key, json):
        if self.get(key) ==  None:
            self.db[key] = dict()
        self.db[key] = (json) 
    def delete(self, key):
        del self.db[key]
        # print(key)
        # print(self.db)
local_c_db = ColCache({})


@dataclass
class DBCache:
    db : dict = field(default_factory=dict)
    def update(self,collection , key, value):
        if self.db.get(collection):
            self.db[collection][key] = value
        raise Exception(f'No collection with name {collection}')   
    
    def get(self, collection, key=None):
        if key:
            return self.db.get(collection).get(key)
        return self.db.get(collection) 
    
    def set(self, key, col):
        if self.get(key) ==  None:
            self.db[key] = list()
        self.db[key].append(col) 
        
    def remove(self, collection, id):
        for c in self.db[collection]:
            if c.get('id') == id:
                self.db[collection].remove(c)
                break

        

local_db = DBCache({})


class Column:
    
    def __init__(self, file):
        self.file = file
        
        _, self.cls, id = file.split('/')
        self.id = id.split('.')[0]
        # local_c_db.db[self.id] = dict()
    def update(self, **obj):
        obj = dict(obj)
        json_db = local_c_db.get(self.id)
        if not json_db:   
            with open(self.file) as f:
                json_db = json.load(f)
        for key, value in obj.items():
            json_db[key] = value
        with open(self.file, 'w+') as f:
            json_db = json.dump(json_db, f)
            local_c_db.set(self.id, json_db)
            
    def readAll(self):
        if local_c_db.get(self.id):
            return local_c_db.get(self.id)
        json_db = {}
        with open(self.file) as f:
            json_db = json.load(f)
            local_c_db.set(self.id, json_db) 
        return json_db
  
    def get(self,key):
        if local_c_db.get(self.id):
            return local_c_db.get(self.id, key)
        
        # print(local_c_db.get(self.id))
        with open(self.file) as f:
            json_db = json.load(f)
            local_c_db.set(self.id, json_db)
        return json_db.get(key)
    def clear(self, key):
        if local_c_db.get(self.id):
            local_c_db.delete(self.id)
        with open(self.file, 'r+') as file:
           json_db = json.load(file)
           if type(key) == list:
               for k in key:
                   del (json_db[k])
           else:
               del (json_db[key])
        return None
    
           
    def delete(self):
        local_db.remove(self.cls, self.id)
        if local_c_db.get(self.id):
            local_c_db.delete(self.id)
        os.remove(self.file)
    def clearAll(self):
        if local_c_db.get(self.id):
            local_c_db.set(self.id, {}) 
        with open(self.file, 'w+') as file:
           json.dump({}, file)
        return None

    def __repr__(self):
        return f"Column {self.get('id')}"
  
       
class JsonDB:
    # db = {}
    def __init__(self, collection, path = './'):
        self.collection = collection
        self.path = path
         
        if os.path.isdir(path + collection) == False:
            os.mkdir(path + self.collection)
    def create_column(self, model, table_name):
           with open(self.path + self.collection + table_name + '.json', 'w+') as file:
            #    self.dump_db(model, self.collection) 
               json.dump(model, file)
               c = Column(self.path + self.collection + table_name + '.json')
               local_db.set(self.collection.split('/')[0],c)
            #    print(c)
            #    raise Exception('b')
            #    local_c_db.set(c.get('id'), c)
               return c
    
    def all(self):
        # print(local_db.get(self.collection))
        # print('here 1')
        # print(local_c_db.db)
        if local_db.get(self.collection.split('/')[0]):
           return local_db.get(self.collection.split('/')[0])
        # print('here 2')
        
        all = os.listdir(self.path + self.collection)
        for i in all:
            c = Column(self.path + self.collection + i)
            local_db.set(self.collection.split('/')[0], c)
            # print(c.get('id'))
            local_c_db.set(c.get('id'), c.readAll())
        # print('here 3')
        return  local_db.get(self.collection.split('/')[0]) if local_db.get(self.collection.split('/')[0]) else []
        
    def get(self,obj):
        all = self.all()
        
        for i in all:
            # print(i, obj)
            o = i.readAll() 
            keys = set(o.keys())
            keys2 = set(obj.keys())
            
            t = (keys2 & keys)
             
            if list(t) == list(keys2):
               
               contains = Contains(o, obj)
               if contains:
                   return Column(self.path + self.collection + i.get('id') + '.json')
        return None
    def filter(self, ob):
        all = self.all()
        result = []
        
        for i in all:
            obj = copy.deepcopy(ob)
            o = i.readAll() 
            #print(obj)
            keys = set(o.keys())
            keys2 = set(obj.keys())
            gt = None
            for k in keys2:
                if k.find("__") != -1 :
                    op = 'g' if k.find("__gt") != -1 else 'l' 
                    #print(op)
                    o, obj, gt = GreaterThan(o, obj ,k, op)
                    keys2 = set(obj.keys())
                    #print(obj)
            if gt == False:
                   #print(gt)
                   continue
            t = (keys2 & keys)
   
            if list(t) == list(keys2):
               contains = Contains(o, obj)
               #print(contains)
               if contains:
                   result.append(i)
        return result
  
        
# db = DB("users/", User)
# products = DB("products/", Product)
# pr1 = products.create_column("watch")
# pr1.update({"name": "US watch", "rate": 5})
#jafar = db.create_column('jafar')
#nura = db.create_column('nura')
#jafar.update({'name':'Jafar Idris','age':50, 'nura': nura.read('id')})
#nura.update({'name':'Nura Idris','age':50, 'nura': nura.read('id')})
#json_db = jafar.readAll()
#name = jafar.read('age')
#jafar.clear(['name','age', 'nura'])
#jafar.clearAll()
#json_db = jafar.readAll()
#print(json_db)
# all = db.filter({'age__gt':5, 'age__lt':59})
#pr1 = db.get({"id":"a58b1227-a97d-4705-a630-460604fdebf7"})
#print(pr1)
#print(all)
# for c in all:
#    print(c.read("name"), c.read('age'))
    