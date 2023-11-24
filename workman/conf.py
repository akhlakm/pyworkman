from dataclasses import dataclass
from workman.util.makeconf import Config, Bool

@dataclass
class _postgres:
    db_host : str = 'localhost'
    db_port : int = 5454
    db_user : str = 'pguser'
    db_pswd : str = ''
    db_name : str = 'django'


@dataclass
class _backend:
    production : Bool = False
    postgres_db : Bool = False
    hosts : str = "127.0.0.1; localhost;"


@dataclass
class _workman:
    """ WorkMan configurations """
    mgr_url : str = 'tcp://127.0.0.1:5555'
    log_level : int = 8


_c = Config("config-wm.yaml").load_yaml()
PostGres    = _c.section(_postgres)
WebServer   = _c.section(_backend)
WorkMan     = _c.section(_workman)
