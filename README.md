# PyWorkMan
ZeroMQ-based workload management via a web interface.
```sh
git clone git@github.com:akhlakm/pyworkman.git
```

## Installation
```sh
# Install pyworkman
pip install -e .
```


## Broker
The message broker (`mgr`) should be setup as a long running process in a easily accessible server.

```sh
# Create YAML config file, set the mgr_url (default 5455).
workman

# Start the broker.
workman mgr
```

## WebUI
The webUI (`ui`) should be run on the local workstation/laptop where you can open up a web browser.
```sh
# Install webui dependencies.
pip install .[ui]

# Create a SSH tunnel to the broker port (default 5455 -> 5455).
workman tunnel

# Create YAML config file, update the mgr_url to the local port.
workman

# Run the web ui.
workman ui
```

## Services
Service workers can be run on any machine. Each service can have many workers.
```sh
# Create a SSH tunnel to the broker port (default 5455 -> 5455).
workman tunnel

# Create config-svc.yaml file.
# Use mgr_url pointing to the local port.
```

Overview of the connections and ports. First create the SSH tunnel from local ports to the broker then use the local connections.

![](connection-setup.svg)
