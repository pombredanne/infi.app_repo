from .base import Indexer
from infi.gevent_utils.os import path
from infi.app_repo.utils import ensure_directory_exists, hard_link_or_raise_exception


class PythonIndexer(Indexer): # TODO implement this
    INDEX_TYPE = "python"

    def initialise(self):
        ensure_directory_exists(self.base_directory)

    def are_you_interested_in_file(self, filepath, platform, arch):
        return path.basename(filepath).startswith("python-") and filepath.endswith(".tar.gz")

    def consume_file(self, filepath, platform, arch):
        hard_link_or_raise_exception(filepath, self.base_directory)

    def rebuild_index(self):
        pass

