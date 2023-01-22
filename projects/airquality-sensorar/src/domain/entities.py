
from typing import List

class Thing(object):
    
    def __init__(self, id_thing:int, fk_id_user:int, desc:str):
        self.id_thing = id_thing
        self.fk_id_user = fk_id_user
        self.desc = desc

class User(object):
    
    def __init__(self, id_user:int, name:str, things:List[Thing]):
        self.id_user = id_user
        self.name = name
        self.things = things
    
    def add_thing(self, thing):
        self.things.append(thing)
