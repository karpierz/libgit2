# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa

# GIT_BEGIN_DECL

# Initialize the OpenSSL locks
#
# OpenSSL requires the application to determine how it performs
# locking.
#
# This is a last-resort convenience function which libgit2 provides for
# allocating and initializing the locks as well as setting the
# locking function to use the system's native locking functions.
#
# The locking function will be cleared and the memory will be freed
# when you call git_threads_sutdown().
#
# If your programming language has an OpenSSL package/bindings, it
# likely sets up locking. You should very strongly prefer that over
# this function.
#
# @return 0 on success, -1 if there are errors or if libgit2 was not
# built with OpenSSL and threading support.
#
git_openssl_set_locking = CFUNC(ct.c_int)(
    ("git_openssl_set_locking", dll),)

# GIT_END_DECL
