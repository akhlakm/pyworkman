from dataclasses import dataclass, field
from workman.util.makeconf import Config, Bool


@dataclass
class _workman:
    """ WorkMan configurations """
    mgr_url : str = 'tcp://127.0.0.1:5555'
    log_level : int = 8


@dataclass
class _postgres:
    db_host : str = 'localhost'
    db_port : int = 5432
    db_user : str = 'postgres'
    db_pswd : str = ''
    db_name : str = 'postgres'


@dataclass
class _workers:
    iwc_url : str = "https://localhost.com"

_c = Config("config-svc.yaml").load_yaml()
WorkMan     = _c.section(_workman)
PostGres    = _c.section(_postgres)
Workers     = _c.section(_workers)

if __name__ == '__main__':
    _c.save_yaml()
