# TelemetryEndpoint
#### Backend system for Network operation telemetry and control.

TelemetryEndpoint was designed for efficient, centralised telemetry gathering. This repo is used in conjunction with closed-source code to provide the Network Operations team with valuable insights into overall system health, individual node health and performance, and network performance.

### Setting up

The provided ``start_example.sh`` file is designed to be run with the wsgi **Gunicorn**.

Installation of Gunicorn on Debian/Ubuntu Linux is simply

```
# apt install gunicorn
```

Once you have gunicorn installed, you can install the python required dependencies.

```
pip install -r requirements.txt
```

Once dependencies are installed, you can run ``start_example.sh`` or simply rename it to ``start.sh``
