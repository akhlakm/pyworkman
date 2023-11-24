from dataclasses import dataclass, field
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
    host : str = "localhost"


@dataclass
class _workman:
    """ WorkMan configurations """
    mgr_url : str = 'tcp://127.0.0.1:5555'



_c = Config("config.yaml").load_yaml()
PostGres    = _c.section(_postgres)
WebServer   = _c.section(_backend)
WorkMan     = _c.section(_workman)

if __name__ == '__main__':
    _c.save_yaml()
