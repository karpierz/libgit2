libgit2
=======

Python binding for the *libgit2* C library.

Overview
========

| Python |package_bold| module is a low-level binding for *libgit2* C library.
| It is an effort to allow python programs full access to the API implemented
  and provided by the well known `*libgit2* <https://curl.se/libcurl/>`__ library.

`PyPI record`_.

`Documentation`_.

| |package_bold| is a lightweight Python package, based on the *ctypes* library.
| It is fully compliant implementation of the original C *libgit2* API
  by implementing whole its functionality in a clean Python instead of C.
|
| *libgit2* API documentation can be found at:

  `libgit2 API overview <https://curl.se/libcurl/c/libcurl.html>`__

|package_bold| uses the underlying *libgit2* C shared library as specified in
libgit2.cfg (included libgit2-X.X.* is the default), but there is also ability
to specify it programmatically by one of the following ways:

.. code:: python

  import libgit2
  libgit2.config(LIBCURL="libgit2 C shared library absolute path")
  # or
  libgit2.config(LIBCURL=None)  # included libgit2-X.X.* will be use

About original libgit2:
-----------------------

Borrowed from the `original website <https://curl.se/libcurl/>`__:

**libgit2** - the multiprotocol file transfer library

**Overview**

**libgit2** is a free and easy-to-use client-side URL transfer library,
supporting DICT, FILE, FTP, FTPS, GOPHER, GOPHERS, HTTP, HTTPS, IMAP, IMAPS,
LDAP, LDAPS, MQTT, POP3, POP3S, RTMP, RTMPS, RTSP, SCP, SFTP, SMB, SMBS,
SMTP, SMTPS, TELNET and TFTP.

**libgit2** supports SSL certificates, HTTP POST, HTTP PUT, FTP uploading,
HTTP form based upload, proxies, HTTP/2, HTTP/3, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, Kerberos), file transfer
resume, http proxy tunneling and more!

**libgit2** is highly portable, it builds and works identically on numerous
platforms, including Solaris, NetBSD, FreeBSD, OpenBSD, Darwin, HPUX, IRIX,
AIX, Tru64, Linux, UnixWare, HURD, Windows, Amiga, OS/2, BeOs, Mac OS X,
Ultrix, QNX, OpenVMS, RISC OS, Novell NetWare, DOS and more...

**libgit2** is free, thread-safe, IPv6 compatible, feature rich, well
supported, fast, thoroughly documented and is already used by many known,
big and successful companies. 

Requirements
============

- | It is a fully independent package.
  | All necessary things are installed during the normal installation process.
- ATTENTION: currently works and tested only for Windows.

Installation
============

Prerequisites:

+ Python 3.8 or higher

  * https://www.python.org/
  * with C libgit2 1.7.1 is a primary test environment.

+ pip and setuptools

  * https://pypi.org/project/pip/
  * https://pypi.org/project/setuptools/

To install run:

  .. parsed-literal::

    python -m pip install --upgrade |package|

Development
===========

Prerequisites:

+ Development is strictly based on *tox*. To install it run::

    python -m pip install --upgrade tox

Visit `Development page`_.

Installation from sources:

clone the sources:

  .. parsed-literal::

    git clone |respository| |package|

and run:

  .. parsed-literal::

    python -m pip install ./|package|

or on development mode:

  .. parsed-literal::

    python -m pip install --editable ./|package|

License
=======

  | Copyright (c) 2023-2024 Adam Karpierz
  | Licensed under the zlib/libpng License
  | https://opensource.org/license/zlib
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Adam Karpierz <adam@karpierz.net>

.. |package| replace:: libgit2
.. |package_bold| replace:: **libgit2**
.. |respository| replace:: https://github.com/karpierz/libgit2.git
.. _Development page: https://github.com/karpierz/libgit2
.. _PyPI record: https://pypi.org/project/libgit2/
.. _Documentation: https://libgit2.readthedocs.io/
