from sqlalchemy.orm import mapper, relationship, sessionmaker
from sqlalchemy import Table, Column, Integer, Float, String, DateTime
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import mapper, relationship

from domain.entities import *

#
class SqlAlchemyRepository():
    
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
    def create_registers(self, entity_registers):
        
        Session = sessionmaker(bind=self.engine)
        session = Session()
        
        session.add(entity_registers)

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
            Sample,
            self._get_sample_map(metadata)
        )

    #
    def _get_sample_map(self, metadata):
        sample_map = Table(
            'sample_tb',
            metadata,
            Column('sensorar_sample_id', Integer, primary_key=True, autoincrement=True),
            Column('ttn_gateway_id', String, nullable=True),
            Column('ttn_gateway_lat', Float(20), nullable=False),
            Column('ttn_gateway_lng', Float(20), nullable=False),
            Column('ttn_device_id', String, nullable=False),
            Column('ttn_received_at', DateTime, nullable=False),
            Column('ttn_payload_frm', String, nullable=False),
            Column('ttn_payload_temp', Float, nullable=False),
            Column('ttn_payload_rh', Float, nullable=False),
            Column('ttn_payload_pm1_0', Float, nullable=False),
            Column('ttn_payload_pm2_5', Float, nullable=False),
            Column('ttn_payload_pm10_0', Float, nullable=False),
        )
        return sample_map