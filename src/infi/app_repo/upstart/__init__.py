
TEMPLATE = """
author "Infinidat, Ltd."
description "Infinidat Application Repository"
version {version}
chdir {chdir}
exec {exec}
kill signal INT
expect stop
respawn
respawn limit 5 1
start on (local-filesystems and net-device-up IFACE!=lo)
stop on runlevel [016]
"""

def install(): # pragma: no cover
    from infi.app_repo import __version__
    from infi.app_repo.scripts import PROJECT_DIRECTORY
    from os.path import join, sep
    kwargs = {'version':__version__.__version__,
              'chdir':PROJECT_DIRECTORY,
              'exec':join(PROJECT_DIRECTORY, 'bin', 'webserver'),
              }
    config = TEMPLATE.format(**kwargs)
    with open(join(sep, 'etc', 'init', 'app_repo.conf'), 'w') as fd:
        fd.write(config)

def signal_init_that_i_am_ready(): # pragma: no cover
    # http://upstart.ubuntu.com/cookbook/#expect-stop
    # Specifies that the job's main process will raise the SIGSTOP signal to indicate that it is ready.
    # init(8) will wait for this signal before running the job's post-start script,
    # or considering the job to be running.
    from os import getpid, kill
    from signal import SIGSTOP
    kill(getpid(), SIGSTOP)

