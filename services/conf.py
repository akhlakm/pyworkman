from dataclasses import dataclass, field
from workman.util.makeconf import Config, Bool

@dataclass
class _workman:
    """ WorkMan configurations """
    mgr_url : str = 'tcp://127.0.0.1:5555'
    log_level : int = 8


_c = Config("config.yaml").load_yaml()
WorkMan     = _c.section(_workman)

if __name__ == '__main__':
    _c.save_yaml()
