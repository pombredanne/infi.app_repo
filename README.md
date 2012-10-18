Introduction
===========

`infi.app_repo` is a complementary solution to our Python-based applications that are managed using `infi.projector` and its skeleton.

`infi.app_repo` is a comibination of a FTP and HTTP services for the following services:
* APT repository
* YUM reopistory
* Update repository for VMware Studio appliances
* Archive for other distributions (e.g. MSI)

Based on our projects structure, versioning scheme and release process, we can upload distribution to a single incoming directory, and in the background process them and move them to the correct repository.

The HTTP service provides:
* Links for manual download of all packaes stored in the repository
* One-liners for setting up the apt/yum repositories in the matching Linux distributions.

Installation
============

Running from source
-------------------

The solution is designed and tested only on ubuntu.
You willl need to pre-install the following packages:

* dpkg
* alien
* createrepo
* yum
* vsftpd
* rng-tools
* dpkg-sig

You will also need to install the Python package `infi.projector` by running `easy_install infi.projector`.
After sorting all these requirements, run:

    projector devenv build
    bin/post_install

The `post_install` script does the following:
* creates user `app_repo`
* set up `vsftpd` on port 21
* set up the HTTP backend on port 80

Installing released versions
----------------------------

You can also download and install the released binaries

* `curl http://repo.infinidat.com/apt_source | sh -`
* apt-get install -y application-repository

Deploying a virtual appliance
-----------------------------

`infi.app_repo` is also packages as a VMware virtual appliance (ubuntu based).
You can download it from http://repo.infinidat.com.
