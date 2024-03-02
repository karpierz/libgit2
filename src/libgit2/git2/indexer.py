# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .oid    import git_oid_t
from .oid    import git_oid
from .types  import git_odb

# GIT_BEGIN_DECL

# A git indexer object
class git_indexer(ct.Structure): pass

# This structure is used to provide callers information about the
# progress of indexing a packfile, either directly or part of a
# fetch or clone that downloads a packfile.
#
class git_indexer_progress(ct.Structure):
    _fields_ = [
    # number of objects in the packfile being indexed
    ("total_objects", ct.c_uint),

    # received objects that have been hashed
    ("indexed_objects", ct.c_uint),

    # received_objects: objects which have been downloaded
    ("received_objects", ct.c_uint),

    # locally-available objects that have been injected in order
    # to fix a thin pack
    ("local_objects", ct.c_uint),

    # number of deltas in the packfile being indexed
    ("total_deltas", ct.c_uint),

    # received deltas that have been indexed
    ("indexed_deltas", ct.c_uint),

    # size of the packfile received up to now
    ("received_bytes", ct.c_size_t),
]

# Type for progress callbacks during indexing.  Return a value less
# than zero to cancel the indexing or download.
#
# @param stats Structure containing information about the state of the transfer
# @param payload Payload provided by caller
#
git_indexer_progress_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_indexer_progress),  # stats
    ct.c_void_p)                       # payload

# Options for indexer configuration
#
class git_indexer_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    *([
    # permissions to use creating packfile or 0 for defaults
    ("mode", ct.c_uint),

    # object database from which to read base objects when
    # fixing thin packs. This can be NULL if there are no thin
    # packs; if a thin pack is encountered, an error will be
    # returned if there are bases missing.
    #
    ("odb", ct.POINTER(git_odb)),
    ] if defined("GIT_EXPERIMENTAL_SHA256") else []),

    # progress_cb function to call with progress information
    ("progress_cb", git_indexer_progress_cb),

    # progress_cb_payload payload for the progress callback
    ("progress_cb_payload", ct.c_void_p),

    # Do connectivity checks for the received pack
    ("verify", ct.c_ubyte),
]

GIT_INDEXER_OPTIONS_VERSION = 1
#define GIT_INDEXER_OPTIONS_INIT = { GIT_INDEXER_OPTIONS_VERSION }

# Initializes a `git_indexer_options` with default values. Equivalent to
# creating an instance with GIT_INDEXER_OPTIONS_INIT.
#
# @param opts the `git_indexer_options` struct to initialize.
# @param version Version of struct; pass `GIT_INDEXER_OPTIONS_VERSION`
# @return Zero on success; -1 on failure.
#
git_indexer_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_indexer_options),
    ct.c_uint)(
    ("git_indexer_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

if defined("GIT_EXPERIMENTAL_SHA256"):
    # Create a new indexer instance
    #
    # @param out where to store the indexer instance
    # @param path to the directory where the packfile should be stored
    # @param oid_type the oid type to use for objects
    # @return 0 or an error code.
    #
    git_indexer_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_indexer)),
        ct.c_char_p,
        git_oid_t,
        ct.POINTER(git_indexer_options))(
        ("git_indexer_new", dll), (
        (1, "out"),
        (1, "path"),
        (1, "oid_type"),
        (1, "opts"),))
else:
    # Create a new indexer instance
    #
    # @param out where to store the indexer instance
    # @param path to the directory where the packfile should be stored
    # @param mode permissions to use creating packfile or 0 for defaults
    # @param odb object database from which to read base objects when
    # fixing thin packs. Pass NULL if no thin pack is expected (an error
    # will be returned if there are bases missing)
    # @param opts Optional structure containing additional options. See
    # `git_indexer_options` above.
    # @return 0 or an error code.
    #
    git_indexer_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_indexer)),
        ct.c_char_p,
        ct.c_uint,
        ct.POINTER(git_odb),
        ct.POINTER(git_indexer_options))(
        ("git_indexer_new", dll), (
        (1, "out"),
        (1, "path"),
        (1, "mode"),
        (1, "odb"),
        (1, "opts"),))
# endif

# Add data to the indexer
#
# @param idx the indexer
# @param data the data to add
# @param size the size of the data in bytes
# @param stats stat storage
# @return 0 or an error code.
#
git_indexer_append = CFUNC(ct.c_int,
    ct.POINTER(git_indexer),
    ct.c_void_p,
    ct.c_size_t,
    ct.POINTER(git_indexer_progress))(
    ("git_indexer_append", dll), (
    (1, "idx"),
    (1, "data"),
    (1, "size"),
    (1, "stats"),))

# Finalize the pack and index
#
# Resolve any pending deltas and write out the index file
#
# @param idx the indexer
# @param stats Stat storage.
# @return 0 or an error code.
#
git_indexer_commit = CFUNC(ct.c_int,
    ct.POINTER(git_indexer),
    ct.POINTER(git_indexer_progress))(
    ("git_indexer_commit", dll), (
    (1, "idx"),
    (1, "stats"),))

if not defined("GIT_DEPRECATE_HARD"):
    # Get the packfile's hash
    #
    # A packfile's name is derived from the sorted hashing of all object
    # names. This is only correct after the index has been finalized.
    #
    # @deprecated use git_indexer_name
    # @param idx the indexer instance
    # @return the packfile's hash
    #
    git_indexer_hash = CFUNC(ct.POINTER(git_oid),
        ct.POINTER(git_indexer))(
        ("git_indexer_hash", dll), (
        (1, "idx"),))
# endif

# Get the unique name for the resulting packfile.
#
# The packfile's name is derived from the packfile's content.
# This is only correct after the index has been finalized.
#
# @param idx the indexer instance
# @return a NUL terminated string for the packfile name
#
git_indexer_name = CFUNC(ct.c_char_p,
    ct.POINTER(git_indexer))(
    ("git_indexer_name", dll), (
    (1, "idx"),))

# Free the indexer and its resources
#
# @param idx the indexer to free
#
git_indexer_free = CFUNC(None,
    ct.POINTER(git_indexer))(
    ("git_indexer_free", dll), (
    (1, "idx"),))

# GIT_END_DECL
