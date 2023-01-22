from sqlalchemy.orm import mapper, relationship, sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import mapper, relationship

from repository.abstract import *
from domain.entities import *

#
class SqlAlchemyRepository(AbstractRepository):
    
    #
    def __init__(self):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///data/db.sqlite3'
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)
        self.metadata = MetaData()

    #    
    def init(self):
        
        mapper = SQLAlchemyMapper()
        mapper.run(self.metadata)
        
        self.metadata.create_all(bind=self.engine)

    #    
    def create_register(self, entity_register):
        
        Session = sessionmaker(bind=self.engine)
        session = Session()
        
        session.add(entity_register)

        session.commit()
        session.close()
        
    #
    def read_register(self, entity, id_register):
        
        Session = sessionmaker(bind=self.engine)
        session = Session()
        
        register = session.query(entity).get(id_register)

        session.commit()
        session.close()
        
        return register

    #
    def update_register(self, entity, id_register, action_func):
        
        Session = sessionmaker(bind=self.engine)
        session = Session()
        
        register = session.query(entity).get(id_register)
        action_func(register)

        session.commit()
        session.close()
        
    #    
    def delete_register(self, entity, id_register):
        
        Session = sessionmaker(bind=self.engine)
        session = Session()

        session.commit()
        session.close()


#
class SQLAlchemyMapper():

    #
    def __init__(self):
        pass

    #
    def run(self, metadata):
        mapper(
            User,
            self._get_user_map(metadata),
            properties={
                'things': relationship(Thing, backref='tb_user')
            },
        )
        mapper(
            Thing,
            self._get_thing_map(metadata)
        )
            
    #
    def _get_user_map(self, metadata):
        user_map = Table(
            'tb_user',
            metadata,
            Column('id_user', Integer, primary_key=True, autoincrement=True),
            Column('name', String(50)),
        )
        return user_map

    #
    def _get_thing_map(self, metadata):
        thing_map = Table(
            'tb_thing',
            metadata,
            Column('id_thing', Integer, primary_key=True, autoincrement=True),
            Column("fk_id_user", Integer, ForeignKey("tb_user.id_user")),
            Column('desc', String(50)),
        )
        return thing_map