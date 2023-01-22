
#
from domain.entities import *
from repository.sqlalchemy import *


if __name__ == '__main__':

    repo = SqlAlchemyRepository()
    repo.init()


    thing = Thing(
        id_thing=None,
        fk_id_user=None,
        desc='keyboard'
    )

    user = User(
        id_user=None,
        name='sergio',
        things=[ thing ]
    )
    

    repo.create_register(user)
    #user = repo.read_register(User, 1)

    # em entity ou usecase
    def update_func(register):
        thing = register.things[0]
        thing.desc = 'aaa'

    # em entity ou usecase
    def update_func(register):
        register.name = 'SS'
        
    #repo.update_register(User, 1, update_func)
    
    #repo.delete_register(User, 1)    

