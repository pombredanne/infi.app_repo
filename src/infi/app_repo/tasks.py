from logging import getLogger
from infi.pyutils.contexts import contextmanager
from . import worker

logger = getLogger(__name__)

@worker.celery.task
def sleep(seconds):
    from time import sleep
    sleep(int(seconds))

@worker.celery.task
def pull_package(remote_fqdn, base_directory, packge_uri):
    from infi.execute import execute_assert_success
    from os import remove, path, chown
    from shutil import move
    with temporary_directory_context():
        filename = path.basename(packge_uri)
        if path.exists(filename):
            return
        url = "ftp://{0}/{1}".format(remote_fqdn, packge_uri)
        execute_assert_success(["wget", url])
        dst = path.join(base_directory, "incoming", filename)
        move(filename, dst)

@worker.celery.task
def push_package(remote_fqdn, remote_username, remote_password, base_directory, packge_uri):
    from infi.execute import execute_assert_success
    from os import path
    src = path.join(base_directory, packge_uri)
    url = "ftp://{0}:{1}@{2}:".format(remote_username, remote_password, remote_fqdn)
    execute_assert_success(["curl", "-T", item, url])

@worker.celery.task
def process_incoming(base_directory, force=False):
    from os import path
    from . import ApplicationRepository
    app_repo = ApplicationRepository(base_directory)
    source_path = path.join(base_directory, 'incoming')
    if not app_repo.add(source_path) and force:
        app_repo.update_metadata()

def _chdir_and_log(path):
    from os import chdir
    chdir(path)
    logger.debug("Changed directory to {!r}".format(path))

@contextmanager
def chdir(path):
    from os.path import abspath
    from os import curdir
    path = abspath(path)
    current_dir = abspath(curdir)
    _chdir_and_log(path)
    try:
        yield
    finally:
        _chdir_and_log(current_dir)

@contextmanager
def temporary_directory_context():
    from tempfile import mkdtemp
    from shutil import rmtree
    tempdir = mkdtemp()
    with chdir(tempdir):
        yield tempdir
    rmtree(tempdir, ignore_errors=True)
