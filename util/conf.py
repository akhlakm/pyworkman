import os
import sys
import yaml
from dataclasses import dataclass

_yaml = {}
_sections = {}
_yaml_config : str = 'config.yaml'

def _bool(val):
    """ Use this func for boolean types in dataclasses. """
    # Convert known string to boolean.
    val = str(val)
    return val.lower() in ['1', 'true', 't', 'yes', 'y']

def _get_cfg(section : str, key: str, dtype : callable, val):
    if not _yaml: load_config()
    s = _yaml.get(section, None)
    if s:
        env = s.get(key, None)
        if env is not None:
            try:
                val = dtype(env)
            except:
                print(f"Invalid YAML: {key}={env}, using {key}={val}")
    return val

def _get_arg(section : str, key: str, dtype : callable, val):
    # Prefix with section name.
    # Value can be specified with --section-key=value format.
    key = f"--{section}-{key}"

    ckey1 = key
    ckey2 = key.replace('_', '-')
    ckey3 = key.lower()
    ckey4 = key.lower().replace('_', '-')

    for arg in sys.argv:
        # Do not break the loop, later values will override earlier ones.
        criteria = [
            arg.startswith(ckey1),
            arg.startswith(ckey2),
            arg.startswith(ckey3),
            arg.startswith(ckey4),
        ]
        if any(criteria):
            # Default value is boolean/1
            env = 1
            if '=' in arg:
                env = '='.join(arg.split('=')[1:])
            try:
                val = dtype(env)
            except:
                print(f"Invalid ARG: {arg}, using {key}={val}")
    return val

def _get_env(section : str, key: str, dtype : callable, val):
    # Prefix with section name and upper case.
    key = f"{section.upper()}_{key.upper()}"
    env = os.environ.get(key, None)
    if env is not None:
        try:
            val = dtype(env)
        except:
            print(f"Invalid ENV: {key}={env}, using {key}={val}")
    return val

def load_config():
    global _yaml
    try:
        with open(_yaml_config) as fp:
            _yaml = yaml.safe_load(fp)
    except:
        _yaml = {'__loaded': False}

def save_config():
    """ Save current settings to a yaml file. """
    d = { k : v.__dict__ for k, v in _sections.items() }
    with open(_yaml_config, 'w') as fp:
        yaml.safe_dump(d, fp, sort_keys=False, indent=4)
        print("Save OK:", _yaml_config)


def new_config(dclass : dataclass):
    inst = dclass()
    section = inst.__class__.__name__.lstrip("_")
    for key, field in inst.__dataclass_fields__.items():
        value = field.default

        # Override from the config file if set.
        value = _get_cfg(section, key, field.type, value)

        # Override from environment variable if set.
        value = _get_env(section, key, field.type, value)

        # Override from command line args if set.
        value = _get_arg(section, key, field.type, value)

        # Set value.
        setattr(inst, key, value)

    _sections[section] = inst
    return inst

### --------------------- Config Section Definitions ---------------------------

@dataclass
class _pg:
    db_host : str = 'localhost'
    db_port : int = 5454
    db_user : str = 'pguser'
    db_pswd : str = ''
    db_name : str = 'django'
    db_textgen : str = 'textgen'

PostGres = new_config(_pg)


@dataclass
class _ws:
    production : _bool = False

WebServer = new_config(_ws)


@dataclass
class _wm:
    mgr_url : str = 'tcp://127.0.0.1:5555'

WorkMan = new_config(_wm)


@dataclass
class _workers:
    iwc_url : str = 'https://localhost.com'

Workers = new_config(_workers)


if __name__ == '__main__':
    load_config()
    save_config()
