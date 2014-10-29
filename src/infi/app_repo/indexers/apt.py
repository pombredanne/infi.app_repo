from .base import Indexer
from infi.app_repo.utils import ensure_directory_exists
from infi.gevent_utils.os import path, remove
from infi.gevent_utils.deferred import create_threadpool_executed_func
from infi.app_repo.utils import temporary_directory_context, log_execute_assert_success, hard_link_or_raise_exception


KNOWN_DISTRIBUTIONS = {
    'linux-ubuntu': {
        'lucid': ('i386', 'amd64'),
        'natty': ('i386', 'amd64'),
        'oneiric': ('i386', 'amd64'),
        'precise': ('i386', 'amd64'),
        'quantal': ('i386', 'amd64'),
        'raring': ('i386', 'amd64'),
        'saucy': ('i386', 'amd64'),
        'trusty': ('i386', 'amd64'),
    }
}

TRANSLATE_ARCH = {'x86': 'i386', 'x64': 'amd64', 'i386': 'i386', 'amd64': 'amd64'}
RELEASE_FILE_HEADER = "Codename: {}\nArchitectures: {}\nComponents: main\n{}"


@create_threadpool_executed_func
def write_to_packages_file(dirpath, contents, mode):
    import gzip
    packages_filepath = path.join(dirpath, 'Packages')
    with open(packages_filepath, mode) as fd:
        fd.write(contents)
    fd = gzip.open(packages_filepath + '.gz', 'wb')
    fd.write(contents)
    fd.close()


def apt_ftparchive(cmdline_arguments):
    return log_execute_assert_success(['apt-ftparchive'] + cmdline_arguments).get_stdout()


def dpkg_scanpackages(cmdline_arguments):
    return log_execute_assert_success(['dpkg-scanpackages'] + cmdline_arguments).get_stdout()


class AptIndexer(Indexer):
    INDEX_TYPE = 'apt'

    def initialise(self):
        ensure_directory_exists(self.base_directory)
        for distribution_name, distribution_dict in KNOWN_DISTRIBUTIONS.items():
            for version, architectures in distribution_dict.items():
                for arch in architectures:
                    dirpath = self.deduce_dirname(distribution_name, version, arch)
                    ensure_directory_exists(dirpath)
                    write_to_packages_file(dirpath, '', 'w')
                self.generate_release_file_for_specific_distribution_and_version(distribution_name, version)

    def deduce_dirname(self, distribution_name, codename, arch): # based on how apt likes it
        return path.join(self.base_directory, distribution_name, 'dists', codename, 'main', 'binary-%s' % TRANSLATE_ARCH[arch])

    def are_you_interested_in_file(self, filepath, platform, arch):
        distribution_name, codename = platform.rsplit('-', 1)
        return filepath.endswith('.deb') and \
               distribution_name in KNOWN_DISTRIBUTIONS and \
               codename in KNOWN_DISTRIBUTIONS[distribution_name] and \
               arch in TRANSLATE_ARCH and \
               TRANSLATE_ARCH[arch] in KNOWN_DISTRIBUTIONS[distribution_name][codename]

    def generate_release_file_for_specific_distribution_and_version(self, distribution, codename):
        dirpath = path.join(self.base_directory, distribution, 'dists', codename)
        in_release = path.join(dirpath, 'InRelease')
        release = path.join(dirpath, 'Release')

        def write_release_file():
            cache = path.join(dirpath, 'apt_cache.db')
            contents = apt_ftparchive(['--db', cache, 'release', dirpath])

            @create_threadpool_executed_func
            def _write():
                with open(release, 'w') as fd:
                    available_archs = sorted(KNOWN_DISTRIBUTIONS[distribution][codename])
                    fd.write(RELEASE_FILE_HEADER.format(codename, " ".join(available_archs), contents))

            _write()

        def delete_old_release_signature_files():
            for filepath in [in_release, '%s.gpg' % release]:
                if path.exists(filepath):
                    remove(filepath)

        def sign_release_file():
            log_execute_assert_success(['gpg', '--clearsign', '-o', in_release, release])
            log_execute_assert_success(['gpg', '-abs', '-o', '%s.gpg' % release, release])

        write_release_file()
        delete_old_release_signature_files()
        sign_release_file()

    def consume_file(self, filepath, platform, arch):
        distribution_name, codename = platform.rsplit('-', 1)
        dirpath = self.deduce_dirname(distribution_name, codename, arch)
        hard_link_or_raise_exception(filepath, dirpath)
        with temporary_directory_context() as tempdir:
            hard_link_or_raise_exception(filepath, tempdir)
            contents = dpkg_scanpackages(['--multiversion', tempdir, '/dev/null'])
            relapath = dirpath.replace(path.join(self.base_directory, distribution_name), '').strip(path.sep)
            fixed_contents = contents.replace(tempdir, relapath)
            write_to_packages_file(dirpath, fixed_contents, 'a')
        self.generate_release_file_for_specific_distribution_and_version(distribution_name, codename)

    def rebuild_index(self):
        for version, architectures in distribution_dict.items():
            for arch in architectures:
                dirpath = self.deduce_dirname(distribution_name, version, arch)
                contents = dpkg_scanpackages(['--multiversion', dirpath, '/dev/null'])
                write_to_packages_file(dirpath, contents, 'w')
            self.generate_release_file_for_specific_distribution_and_version(distribution_name, version)
