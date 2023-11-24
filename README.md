# PyWorkMan
ZeroMQ-based workload management with web user interface.

## Installation
```sh
# Optional: create/load a conda env.
source make.sh

# Install pyworkman
pip install -e .

# Optional: Install webui dependencies.
pip install .[ui]

# Optional: Install postgres dependencies.
pip install .[db]
```

## Run
```sh
# Create YAML config file.
workman

# Run broker.
workman mgr

# Run web ui.
workman ui

# Create a tunnel.
workman tunnel <localport> <remoteport>
```

