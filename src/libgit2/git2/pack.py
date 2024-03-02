# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common  import *  # noqa
from .oid     import git_oid
from .buffer  import git_buf
from .types   import git_repository
from .types   import git_packbuilder
from .types   import git_revwalk
from .indexer import git_indexer_progress_cb

# @file git2/pack.h
# @brief Git pack management routines
#
# Packing objects
# ---------------
#
# Creation of packfiles requires two steps:
#
# - First, insert all the objects you want to put into the packfile
#   using `git_packbuilder_insert` and `git_packbuilder_insert_tree`.
#   It's important to add the objects in recency order ("in the order
#   that they are 'reachable' from head").
#
#   "ANY order will give you a working pack, ... [but it is] the thing
#   that gives packs good locality. It keeps the objects close to the
#   head (whether they are old or new, but they are _reachable_ from the
#   head) at the head of the pack. So packs actually have absolutely
#   _wonderful_ IO patterns." - Linus Torvalds
#   git.git/Documentation/technical/pack-heuristics.txt
#
# - Second, use `git_packbuilder_write` or `git_packbuilder_foreach` to
#   write the resulting packfile.
#
#   libgit2 will take care of the delta ordering and generation.
#   `git_packbuilder_set_threads` can be used to adjust the number of
#   threads used for the process.
#
# See tests/pack/packbuilder.c for an example.
#
# @ingroup Git

# GIT_BEGIN_DECL

# Stages that are reported by the packbuilder progress callback.
#
git_packbuilder_stage_t = ct.c_int
(   GIT_PACKBUILDER_ADDING_OBJECTS,
    GIT_PACKBUILDER_DELTAFICATION,
) = (0, 1)

# Initialize a new packbuilder
#
# @param out The new packbuilder object
# @param repo The repository
#
# @return 0 or an error code
#
git_packbuilder_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_packbuilder)),
    ct.POINTER(git_repository))(
    ("git_packbuilder_new", dll), (
    (1, "out"),
    (1, "repo"),))

# Set number of threads to spawn
#
# By default, libgit2 won't spawn any threads at all;
# when set to 0, libgit2 will autodetect the number of
# CPUs.
#
# @param pb The packbuilder
# @param n Number of threads to spawn
# @return number of actual threads to be used
#
git_packbuilder_set_threads = CFUNC(ct.c_uint,
    ct.POINTER(git_packbuilder),
    ct.c_uint)(
    ("git_packbuilder_set_threads", dll), (
    (1, "pb"),
    (1, "n"),))

# Insert a single object
#
# For an optimal pack it's mandatory to insert objects in recency order,
# commits followed by trees and blobs.
#
# @param pb The packbuilder
# @param id The oid of the commit
# @param name The name; might be NULL
#
# @return 0 or an error code
#
git_packbuilder_insert = CFUNC(ct.c_int,
    ct.POINTER(git_packbuilder),
    ct.POINTER(git_oid),
    ct.c_char_p)(
    ("git_packbuilder_insert", dll), (
    (1, "pb"),
    (1, "id"),
    (1, "name"),))

# Insert a root tree object
#
# This will add the tree as well as all referenced trees and blobs.
#
# @param pb The packbuilder
# @param id The oid of the root tree
#
# @return 0 or an error code
#
git_packbuilder_insert_tree = CFUNC(ct.c_int,
    ct.POINTER(git_packbuilder),
    ct.POINTER(git_oid))(
    ("git_packbuilder_insert_tree", dll), (
    (1, "pb"),
    (1, "id"),))

# Insert a commit object
#
# This will add a commit as well as the completed referenced tree.
#
# @param pb The packbuilder
# @param id The oid of the commit
#
# @return 0 or an error code
#
git_packbuilder_insert_commit = CFUNC(ct.c_int,
    ct.POINTER(git_packbuilder),
    ct.POINTER(git_oid))(
    ("git_packbuilder_insert_commit", dll), (
    (1, "pb"),
    (1, "id"),))

# Insert objects as given by the walk
#
# Those commits and all objects they reference will be inserted into
# the packbuilder.
#
# @param pb the packbuilder
# @param walk the revwalk to use to fill the packbuilder
#
# @return 0 or an error code
#
git_packbuilder_insert_walk = CFUNC(ct.c_int,
    ct.POINTER(git_packbuilder),
    ct.POINTER(git_revwalk))(
    ("git_packbuilder_insert_walk", dll), (
    (1, "pb"),
    (1, "walk"),))

# Recursively insert an object and its referenced objects
#
# Insert the object as well as any object it references.
#
# @param pb the packbuilder
# @param id the id of the root object to insert
# @param name optional name for the object
# @return 0 or an error code
#
git_packbuilder_insert_recur = CFUNC(ct.c_int,
    ct.POINTER(git_packbuilder),
    ct.POINTER(git_oid),
    ct.c_char_p)(
    ("git_packbuilder_insert_recur", dll), (
    (1, "pb"),
    (1, "id"),
    (1, "name"),))

# Write the contents of the packfile to an in-memory buffer
#
# The contents of the buffer will become a valid packfile, even though there
# will be no attached index
#
# @param buf Buffer where to write the packfile
# @param pb The packbuilder
# @return 0 or an error code
#
git_packbuilder_write_buf = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_packbuilder))(
    ("git_packbuilder_write_buf", dll), (
    (1, "buf"),
    (1, "pb"),))

# Write the new pack and corresponding index file to path.
#
# @param pb The packbuilder
# @param path Path to the directory where the packfile and index should be stored, or NULL for default location
# @param mode permissions to use creating a packfile or 0 for defaults
# @param progress_cb function to call with progress information from the indexer (optional)
# @param progress_cb_payload payload for the progress callback (optional)
#
# @return 0 or an error code
#
git_packbuilder_write = CFUNC(ct.c_int,
    ct.POINTER(git_packbuilder),
    ct.c_char_p,
    ct.c_uint,
    git_indexer_progress_cb,
    ct.c_void_p)(
    ("git_packbuilder_write", dll), (
    (1, "pb"),
    (1, "path"),
    (1, "mode"),
    (1, "progress_cb"),
    (1, "progress_cb_payload"),))

if not defined("GIT_DEPRECATE_HARD"):
    # Get the packfile's hash
    #
    # A packfile's name is derived from the sorted hashing of all object
    # names. This is only correct after the packfile has been written.
    #
    # @deprecated use git_packbuilder_name
    # @param pb The packbuilder object
    # @return 0 or an error code
    #
    git_packbuilder_hash = CFUNC(ct.POINTER(git_oid),
        ct.POINTER(git_packbuilder))(
        ("git_packbuilder_hash", dll), (
        (1, "pb"),))
# endif

# Get the unique name for the resulting packfile.
#
# The packfile's name is derived from the packfile's content.
# This is only correct after the packfile has been written.
#
# @param pb the packbuilder instance
# @return a NUL terminated string for the packfile name
#
git_packbuilder_name = CFUNC(ct.c_char_p,
    ct.POINTER(git_packbuilder))(
    ("git_packbuilder_name", dll), (
    (1, "pb"),))

# Callback used to iterate over packed objects
#
# @see git_packbuilder_foreach
#
# @param buf A pointer to the object's data
# @param size The size of the underlying object
# @param payload Payload passed to git_packbuilder_foreach
# @return non-zero to terminate the iteration
#
git_packbuilder_foreach_cb = GIT_CALLBACK(ct.c_int,
    ct.c_void_p,  # buf
    ct.c_size_t,  # size
    ct.c_void_p)  # payload

# Create the new pack and pass each object to the callback
#
# @param pb the packbuilder
# @param cb the callback to call with each packed object's buffer
# @param payload the callback's data
# @return 0 or an error code
#
git_packbuilder_foreach = CFUNC(ct.c_int,
    ct.POINTER(git_packbuilder),
    git_packbuilder_foreach_cb,
    ct.c_void_p)(
    ("git_packbuilder_foreach", dll), (
    (1, "pb"),
    (1, "cb"),
    (1, "payload"),))

# Get the total number of objects the packbuilder will write out
#
# @param pb the packbuilder
# @return the number of objects in the packfile
#
git_packbuilder_object_count = CFUNC(ct.c_size_t,
    ct.POINTER(git_packbuilder))(
    ("git_packbuilder_object_count", dll), (
    (1, "pb"),))

# Get the number of objects the packbuilder has already written out
#
# @param pb the packbuilder
# @return the number of objects which have already been written
#
git_packbuilder_written = CFUNC(ct.c_size_t,
    ct.POINTER(git_packbuilder))(
    ("git_packbuilder_written", dll), (
    (1, "pb"),))

# Packbuilder progress notification function
git_packbuilder_progress = GIT_CALLBACK(ct.c_int,
    ct.c_int,     # stage
    ct.c_uint32,  # current
    ct.c_uint32,  # total
    ct.c_void_p)  # payload

# Set the callbacks for a packbuilder
#
# @param pb The packbuilder object
# @param progress_cb Function to call with progress information during
# pack building. Be aware that this is called inline with pack building
# operations, so performance may be affected.
# @param progress_cb_payload Payload for progress callback.
# @return 0 or an error code
#
git_packbuilder_set_callbacks = CFUNC(ct.c_int,
    ct.POINTER(git_packbuilder),
    git_packbuilder_progress,
    ct.c_void_p)(
    ("git_packbuilder_set_callbacks", dll), (
    (1, "pb"),
    (1, "progress_cb"),
    (1, "progress_cb_payload"),))

# Free the packbuilder and all associated data
#
# @param pb The packbuilder
#
git_packbuilder_free = CFUNC(None,
    ct.POINTER(git_packbuilder))(
    ("git_packbuilder_free", dll), (
    (1, "pb"),))

# GIT_END_DECL
