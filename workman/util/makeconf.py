import os
import sys
import yaml
from dataclasses import dataclass

def Bool(val):
    """ Use this func for boolean types in dataclasses. """
    # Convert known string to boolean.
    val = str(val)
    return val.lower() in ['1', 'true', 't', 'yes', 'y']

class Config:
    def __init__(self, yamlfile : str = None) -> None:
        self._yaml = {}
        self._sections = {}
        self._yaml_file = yamlfile

    def section(self, dclass : dataclass):
        inst = dclass()
        section = inst.__class__.__name__.lstrip("_")
        for key, field in inst.__dataclass_fields__.items():
            value = field.default

            # Override from the config file if set.
            value = self._get_cfg(section, key, field.type, value)

            # Override from environment variable if set.
            value = self._get_env(section, key, field.type, value)

            # Override from command line args if set.
            value = self._get_arg(section, key, field.type, value)

            # Set value.
            setattr(inst, key, value)

        self._sections[section] = inst
        return inst

    def load_yaml(self):
        try:
            with open(self._yaml_file) as fp:
                self._yaml = yaml.safe_load(fp)
        except:
            self._yaml = {'__loaded': False}
        return self

    def save_yaml(self):
        """ Save current settings to a yaml file. """
        d = { k : v.__dict__ for k, v in self._sections.items() }
        with open(self._yaml_file, 'w') as fp:
            yaml.safe_dump(d, fp, sort_keys=False, indent=4)
            print("Save OK:", self._yaml_file)

    def _get_cfg(self, section : str, key: str, dtype : callable, val):
        if not self._yaml:
            self.load_yaml()

        s = self._yaml.get(section, None)
        if s:
            env = s.get(key, None)
            if env is not None:
                try:
                    val = dtype(env)
                except:
                    print(f"Invalid YAML: {key}={env}, using {key}={val}")
        return val


    def _get_arg(self, section : str, key: str, dtype : callable, val):
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

    def _get_env(self, section : str, key: str, dtype : callable, val):
        # Prefix with section name and upper case.
        key = f"{section.upper()}_{key.upper()}"
        env = os.environ.get(key, None)
        if env is not None:
            try:
                val = dtype(env)
            except:
                print(f"Invalid ENV: {key}={env}, using {key}={val}")
        return val

