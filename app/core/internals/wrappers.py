from contextvars import ContextVar
from peewee import *
from peewee import PostgresqlDatabase, InterfaceError as PeeWeeInterfaceError
import logging
from playhouse.db_url import connect, parse
from playhouse.shortcuts import ReconnectMixin

from config import SRC_LOG_LEVELS

log = logging.getLogger(__name__)

log.setLevel(SRC_LOG_LEVELS['DB'])

db_state_default = {"closed": None, "conn":None, "ctx": None, "transaction":None}

db_state = ContextVar("db_state", default=db_state_default.copy())



class PeeweeConnectionState(object):
    def __init__(self,**kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)
    
    def __set_attr__(self,name,value):
        self._state.get()[name]=value
    
    def __getattr__(self,name):
        value = self._state.get()[name]
        return value

class CustomReconnectionMixin(ReconnectMixin):
    reconnect_errors=(
        (OperationalError, "termin"),
        (InterfaceError, "closed"),
        
        (PeeWeeInterfaceError, "closed"),
    )

class ReconnectingPostgressqlDatabase(CustomReconnectionMixin, PostgresqlDatabase):
    pass 


def register_connection(db_url):
    db = connect(db_url)
    if isinstance(db, PostgresqlDatabase):
        #Enable autoconnect for Sqllit databases, managed by Peewwee
            
        db.autoconnect = True
        db.resue_if_open = True
        log.info("Connected to PostgresSql database")
        
        
        connection = parse(db_url)
        
        
        #use our custom database class that supports reconnection
        
        db = ReconnectingPostgressqlDatabase(
            
            connection["database"],
            user=connection["user"],
            password=connection["password"],
            host=connection["host"],
            port=connection["port"],
        )
        db.connect(reuse_if_open=True)

    elif isinstance(db, SqliteDatabase):
        
        db.autoconnect=True
        db.reuse_if_open= True
        log.info("Connected to Sqlite database")
        
    else:
        raise ValueError("Unsupported database connection")
    
    return db


                    
            