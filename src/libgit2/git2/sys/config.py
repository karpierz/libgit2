# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa
from ..config import git_config_level_t
from ..config import git_config_entry
from ..types  import git_config
from ..types  import git_config_backend
from ..types  import git_repository

# @file git2/sys/config.h
# @brief Git config backend routines
# @defgroup git_backend Git custom backend APIs
# @ingroup Git

# GIT_BEGIN_DECL

# Every iterator must have this struct as its first element,
# so the API can talk to it. You'd define your iterator as
#
#     class my_iterator(ct.Structure):
#        _fields_ = [
#             ("parent", git_config_iterator),
#             ...
#     ]
#
# and assign `iter->parent.backend` to your `git_config_backend`.
#
class git_config_iterator(ct.Structure): pass
git_config_iterator._fields_ = [
    ("backend", ct.POINTER(git_config_backend)),
    ("flags",   ct.c_uint),

    # Return the current entry and advance the iterator.
    # The memory belongs to the library.
    #
    ("next", GIT_CALLBACK(ct.c_int,
                 ct.POINTER(ct.POINTER(git_config_entry)),  # entry
                 ct.POINTER(git_config_iterator))),         # iter

    # Free the iterator
    #
    ("free", GIT_CALLBACK(None,
                 ct.POINTER(git_config_iterator))),  # iter
]

# Generic backend that implements the interface to
# access a configuration file
#
class git_config_backend(ct.Structure): pass
git_config_backend._fields_ = [
    ("version",  ct.c_uint),
    # True if this backend is for a snapshot
    ("readonly", ct.c_int),
    ("cfg",      ct.POINTER(git_config)),

    # Open means open the file/database and parse if necessary
    ("open",          GIT_CALLBACK(ct.c_int,
                          ct.POINTER(git_config_backend),  # cfg
                          git_config_level_t,              # level
                          ct.POINTER(git_repository))),    # repo
    ("get",           GIT_CALLBACK(ct.c_int,
                          ct.POINTER(git_config_backend),              # cfg
                          ct.c_char_p,                                 # key
                          ct.POINTER(ct.POINTER(git_config_entry)))),  # entry
    ("set",           GIT_CALLBACK(ct.c_int,
                          ct.POINTER(git_config_backend),  # cfg
                          ct.c_char_p,                     # key
                          ct.POINTER(ct.c_byte))),         # value # TODO: ??? was: const char *
    ("set_multivar",  GIT_CALLBACK(ct.c_int,
                          ct.POINTER(git_config_backend),  # cfg
                          ct.c_char_p,                     # name
                          ct.c_char_p,                     # regexp
                          ct.POINTER(ct.c_byte))),         # value # TODO: ??? was: const char *
    ("del",           GIT_CALLBACK(ct.c_int,
                          ct.POINTER(git_config_backend),  # cfg
                          ct.c_char_p)),                   # key
    ("del_multivar",  GIT_CALLBACK(ct.c_int,
                          ct.POINTER(git_config_backend),  # cfg
                          ct.c_char_p,                     # key
                          ct.c_char_p)),                   # regexp
    ("iterator",      GIT_CALLBACK(ct.c_int,
                          ct.POINTER(ct.POINTER(git_config_iterator)),  # iter
                          ct.POINTER(git_config_backend))),             # cfg
    # Produce a read-only version of this backend
    ("snapshot",      GIT_CALLBACK(ct.c_int,
                          ct.POINTER(ct.POINTER(git_config_backend)),   # ???
                          ct.POINTER(git_config_backend))),             # cfg
    # Lock this backend.
    #
    # Prevent any writes to the data store backing this
    # backend. Any updates must not be visible to any other
    # readers.
    #
    ("lock",          GIT_CALLBACK(ct.c_int,
                          ct.POINTER(git_config_backend))),  # cfg
    # Unlock the data store backing this backend. If success is
    # true, the changes should be committed, otherwise rolled
    # back.
    #
    ("unlock",        GIT_CALLBACK(ct.c_int,
                          ct.POINTER(git_config_backend),    # cfg
                          ct.c_int)),                        # success
    ("free",          GIT_CALLBACK(None,
                          ct.POINTER(git_config_backend))),  # cfg
]

GIT_CONFIG_BACKEND_VERSION = 1
#define GIT_CONFIG_BACKEND_INIT = { GIT_CONFIG_BACKEND_VERSION }

# Initializes a `git_config_backend` with default values. Equivalent to
# creating an instance with GIT_CONFIG_BACKEND_INIT.
#
# @param backend the `git_config_backend` struct to initialize.
# @param version Version of struct; pass `GIT_CONFIG_BACKEND_VERSION`
# @return Zero on success; -1 on failure.
#
git_config_init_backend = CFUNC(ct.c_int,
    ct.POINTER(git_config_backend),
    ct.c_uint)(
    ("git_config_init_backend", dll), (
    (1, "backend"),
    (1, "version"),))

# Add a generic config file instance to an existing config
#
# Note that the configuration object will free the file
# automatically.
#
# Further queries on this config object will access each
# of the config file instances in order (instances with
# a higher priority level will be accessed first).
#
# @param cfg the configuration to add the file to
# @param file the configuration file (backend) to add
# @param level the priority level of the backend
# @param repo optional repository to allow parsing of
#  conditional includes
# @param force if a config file already exists for the given
#  priority level, replace it
# @return 0 on success, GIT_EEXISTS when adding more than one file
#  for a given priority level (and force_replace set to 0), or error code
#
git_config_add_backend = CFUNC(ct.c_int,
    ct.POINTER(git_config),
    ct.POINTER(git_config_backend),
    git_config_level_t,
    ct.POINTER(git_repository),
    ct.c_int)(
    ("git_config_add_backend", dll), (
    (1, "cfg"),
    (1, "file"),
    (1, "level"),
    (1, "repo"),
    (1, "force"),))

# GIT_END_DECL
