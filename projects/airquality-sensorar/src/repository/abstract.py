from abc import ABC, abstractmethod

#
class AbstractRepository(ABC):

    @abstractmethod
    def init():
        raise NotImplementedError
    
    @abstractmethod
    def create_register(register):
        raise NotImplementedError
        
    @abstractmethod
    def read_register(entity, register_id):
        raise NotImplementedError

    @abstractmethod
    def update_register(entity, register_id, action_func):
        raise NotImplementedError
    
    @abstractmethod
    def delete_register(entity, register_id):
        raise NotImplementedError



