# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common  import *  # noqa
from .oid     import git_oid_t
from .oid     import git_oid
from .types   import git_object_size_t
from .types   import git_odb_backend
from .indexer import git_indexer_progress

# @file git2/backend.h
# @brief Git custom backend functions
# @defgroup git_odb Git object database routines
# @ingroup Git

# GIT_BEGIN_DECL

# Constructors for in-box ODB backends.
#

# Options for configuring a packfile object backend.
class git_odb_backend_pack_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),  # version for the struct

    # Type of object IDs to use for this object database,
    # or 0 for default (currently SHA1).
    ("oid_type", git_oid_t),
]

# The current version of the diff options structure
GIT_ODB_BACKEND_PACK_OPTIONS_VERSION = 1

# Stack initializer for odb pack backend options.  Alternatively use
# `git_odb_backend_pack_options_init` programmatic initialization.
#
#define GIT_ODB_BACKEND_PACK_OPTIONS_INIT = { GIT_ODB_BACKEND_PACK_OPTIONS_VERSION }

# Create a backend for the packfiles.
#
# @param out location to store the odb backend pointer
# @param objects_dir the Git repository's objects directory
#
# @return 0 or an error code
#
if defined("GIT_EXPERIMENTAL_SHA256"):
    git_odb_backend_pack = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_odb_backend)),
        ct.c_char_p,
        ct.POINTER(git_odb_backend_pack_options))(
        ("git_odb_backend_pack", dll), (
        (1, "out"),
        (1, "objects_dir"),
        (1, "opts"),))
else:
    git_odb_backend_pack = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_odb_backend)),
        ct.c_char_p)(
        ("git_odb_backend_pack", dll), (
        (1, "out"),
        (1, "objects_dir"),))
# endif

# Create a backend out of a single packfile
#
# This can be useful for inspecting the contents of a single
# packfile.
#
# @param out location to store the odb backend pointer
# @param index_file path to the packfile's .idx file
#
# @return 0 or an error code
#
if defined("GIT_EXPERIMENTAL_SHA256"):
    git_odb_backend_one_pack = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_odb_backend)),
        ct.c_char_p,
        ct.POINTER(git_odb_backend_pack_options))(
        ("git_odb_backend_one_pack", dll), (
        (1, "out"),
        (1, "index_file"),
        (1, "opts"),))
else:
    git_odb_backend_one_pack = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_odb_backend)),
        ct.c_char_p)(
        ("git_odb_backend_one_pack", dll), (
        (1, "out"),
        (1, "index_file"),))
# endif

git_odb_backend_loose_flag_t = ct.c_int
(   GIT_ODB_BACKEND_LOOSE_FSYNC,
) = (1 << 0,)

# Options for configuring a loose object backend.
class git_odb_backend_loose_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),  # version for the struct

    # A combination of the `git_odb_backend_loose_flag_t` types.
    ("flags", ct.c_uint32),

    # zlib compression level to use (0-9), where 1 is the fastest
    # at the expense of larger files, and 9 produces the best
    # compression at the expense of speed.  0 indicates that no
    # compression should be performed.  -1 is the default (currently
    # optimizing for speed).
    #
    ("compression_level", ct.c_int),

    # Permissions to use creating a directory or 0 for defaults
    ("dir_mode", ct.c_uint),

    # Permissions to use creating a file or 0 for defaults
    ("file_mode", ct.c_uint),

    # Type of object IDs to use for this object database, or
    # 0 for default (currently SHA1).
    #
    ("oid_type", git_oid_t),
]

# The current version of the diff options structure
GIT_ODB_BACKEND_LOOSE_OPTIONS_VERSION = 1

# Stack initializer for odb loose backend options.  Alternatively use
# `git_odb_backend_loose_options_init` programmatic initialization.
#
#define GIT_ODB_BACKEND_LOOSE_OPTIONS_INIT = { GIT_ODB_BACKEND_LOOSE_OPTIONS_VERSION, 0, -1 }

# Create a backend for loose objects
#
# @param out location to store the odb backend pointer
# @param objects_dir the Git repository's objects directory
# @param opts options for the loose object backend or NULL
#
# @return 0 or an error code
#
if defined("GIT_EXPERIMENTAL_SHA256"):
    git_odb_backend_loose = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_odb_backend)),
        ct.c_char_p,
        ct.POINTER(git_odb_backend_loose_options))(
        ("git_odb_backend_loose", dll), (
        (1, "out"),
        (1, "objects_dir"),
        (1, "opts"),))
else:
    git_odb_backend_loose = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_odb_backend)),
        ct.c_char_p,
        ct.c_int,
        ct.c_int,
        ct.c_uint,
        ct.c_uint)(
        ("git_odb_backend_loose", dll), (
        (1, "out"),
        (1, "objects_dir"),
        (1, "compression_level"),
        (1, "do_fsync"),
        (1, "dir_mode"),
        (1, "file_mode"),))
# endif

# Streaming mode
git_odb_stream_t = ct.c_int
(   GIT_STREAM_RDONLY,
    GIT_STREAM_WRONLY,
    GIT_STREAM_RW,
) = (
    1 << 1,
    1 << 2,
    (1 << 1) | (1 << 2), # GIT_STREAM_RDONLY | GIT_STREAM_WRONLY
)

# A stream to read/write from a backend.
#
# This represents a stream of data being written to or read from a
# backend. When writing, the frontend functions take care of
# calculating the object's id and all `finalize_write` needs to do is
# store the object with the id it is passed.
#
class git_odb_stream(ct.Structure): pass
git_odb_stream._fields_ = [
    ("backend", ct.POINTER(git_odb_backend)),
    ("mode", ct.c_uint),
    ("hash_ctx", ct.c_void_p),

    *([("oid_type", git_oid_t)]
      if defined("GIT_EXPERIMENTAL_SHA256") else []),

    ("declared_size",  git_object_size_t),
    ("received_bytes", git_object_size_t),

    # Write at most `len` bytes into `buffer` and advance the stream.
    #
    ("read", GIT_CALLBACK(ct.c_int,
                 ct.POINTER(git_odb_stream),  # stream
                 git_buffer_t,                # buffer
                 ct.c_size_t)),               # len

    # Write `len` bytes from `buffer` into the stream.
    #
    ("write", GIT_CALLBACK(ct.c_int,
                  ct.POINTER(git_odb_stream),  # stream
                  git_buffer_t,                # buffer
                  ct.c_size_t)),               # len

    # Store the contents of the stream as an object with the id
    # specified in `oid`.
    #
    # This method might not be invoked if:
    # - an error occurs earlier with the `write` callback,
    # - the object referred to by `oid` already exists in any backend, or
    # - the final number of received bytes differs from the size declared
    #   with `git_odb_open_wstream()`
    #
    ("finalize_write", GIT_CALLBACK(ct.c_int,
                           ct.POINTER(git_odb_stream),  # stream
                           ct.POINTER(git_oid))),       # oid

    # Free the stream's memory.
    #
    # This method might be called without a call to `finalize_write` if
    # an error occurs or if the object is already present in the ODB.
    #
    ("free", GIT_CALLBACK(None,
                 ct.POINTER(git_odb_stream))),  # stream
]

# A stream to write a pack file to the ODB
class git_odb_writepack(ct.Structure): pass
git_odb_writepack._fields_ = [
    ("backend", ct.POINTER(git_odb_backend)),

    ("append", GIT_CALLBACK(ct.c_int,
                   ct.POINTER(git_odb_writepack),       # writepack
                   ct.c_void_p,                         # data
                   ct.c_size_t,                         # size
                   ct.POINTER(git_indexer_progress))),  # stats
    ("commit", GIT_CALLBACK(ct.c_int,
                   ct.POINTER(git_odb_writepack),       # writepack
                   ct.POINTER(git_indexer_progress))),  # stats
    ("free",   GIT_CALLBACK(None,
                   ct.POINTER(git_odb_writepack))),     # writepack
]

# GIT_END_DECL
