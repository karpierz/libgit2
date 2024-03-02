# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa
from ..oid    import git_oid
from ..types  import git_index

# @file git2/sys/index.h
# @brief Low-level Git index manipulation routines
# @defgroup git_backend Git custom backend APIs
# @ingroup Git

# GIT_BEGIN_DECL

# Representation of a rename conflict entry in the index.
class git_index_name_entry(ct.Structure):
    _fields_ = [
    ("ancestor", ct.c_char_p),
    ("ours",     ct.c_char_p),
    ("theirs",   ct.c_char_p),
]

# Representation of a resolve undo entry in the index.
class git_index_reuc_entry(ct.Structure):
    _fields_ = [
    ("mode", (ct.c_uint32 * 3)),
    ("oid",  (git_oid     * 3)),
    ("path", ct.c_char_p),
]

# @name Conflict Name entry functions
#
# These functions work on rename conflict entries.
#

# Get the count of filename conflict entries currently in the index.
#
# @param index an existing index object
# @return integer of count of current filename conflict entries
#
git_index_name_entrycount = CFUNC(ct.c_size_t,
    ct.POINTER(git_index))(
    ("git_index_name_entrycount", dll), (
    (1, "index"),))

# Get a filename conflict entry from the index.
#
# The returned entry is read-only and should not be modified
# or freed by the caller.
#
# @param index an existing index object
# @param n the position of the entry
# @return a pointer to the filename conflict entry; NULL if out of bounds
#
git_index_name_get_byindex = CFUNC(ct.POINTER(git_index_name_entry),
    ct.POINTER(git_index),
    ct.c_size_t)(
    ("git_index_name_get_byindex", dll), (
    (1, "index"),
    (1, "n"),))

# Record the filenames involved in a rename conflict.
#
# @param index an existing index object
# @param ancestor the path of the file as it existed in the ancestor
# @param ours the path of the file as it existed in our tree
# @param theirs the path of the file as it existed in their tree
#
git_index_name_add = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.c_char_p,
    ct.c_char_p,
    ct.c_char_p)(
    ("git_index_name_add", dll), (
    (1, "index"),
    (1, "ancestor"),
    (1, "ours"),
    (1, "theirs"),))

# Remove all filename conflict entries.
#
# @param index an existing index object
# @return 0 or an error code
#
git_index_name_clear = CFUNC(ct.c_int,
    ct.POINTER(git_index))(
    ("git_index_name_clear", dll), (
    (1, "index"),))

# @name Resolve Undo (REUC) index entry manipulation.
#
# These functions work on the Resolve Undo index extension and contains
# data about the original files that led to a merge conflict.
#

# Get the count of resolve undo entries currently in the index.
#
# @param index an existing index object
# @return integer of count of current resolve undo entries
#
git_index_reuc_entrycount = CFUNC(ct.c_size_t,
    ct.POINTER(git_index))(
    ("git_index_reuc_entrycount", dll), (
    (1, "index"),))

# Finds the resolve undo entry that points to the given path in the Git
# index.
#
# @param at_pos the address to which the position of the reuc entry is written (optional)
# @param index an existing index object
# @param path path to search
# @return 0 if found, < 0 otherwise (GIT_ENOTFOUND)
#
git_index_reuc_find = CFUNC(ct.c_int,
    ct.POINTER(ct.c_size_t),
    ct.POINTER(git_index),
    ct.c_char_p)(
    ("git_index_reuc_find", dll), (
    (1, "at_pos"),
    (1, "index"),
    (1, "path"),))

# Get a resolve undo entry from the index.
#
# The returned entry is read-only and should not be modified
# or freed by the caller.
#
# @param index an existing index object
# @param path path to search
# @return the resolve undo entry; NULL if not found
#
git_index_reuc_get_bypath = CFUNC(ct.POINTER(git_index_reuc_entry),
    ct.POINTER(git_index),
    ct.c_char_p)(
    ("git_index_reuc_get_bypath", dll), (
    (1, "index"),
    (1, "path"),))

# Get a resolve undo entry from the index.
#
# The returned entry is read-only and should not be modified
# or freed by the caller.
#
# @param index an existing index object
# @param n the position of the entry
# @return a pointer to the resolve undo entry; NULL if out of bounds
#
git_index_reuc_get_byindex = CFUNC(ct.POINTER(git_index_reuc_entry),
    ct.POINTER(git_index),
    ct.c_size_t)(
    ("git_index_reuc_get_byindex", dll), (
    (1, "index"),
    (1, "n"),))

# Adds a resolve undo entry for a file based on the given parameters.
#
# The resolve undo entry contains the OIDs of files that were involved
# in a merge conflict after the conflict has been resolved.  This allows
# conflicts to be re-resolved later.
#
# If there exists a resolve undo entry for the given path in the index,
# it will be removed.
#
# This method will fail in bare index instances.
#
# @param index an existing index object
# @param path filename to add
# @param ancestor_mode mode of the ancestor file
# @param ancestor_id oid of the ancestor file
# @param our_mode mode of our file
# @param our_id oid of our file
# @param their_mode mode of their file
# @param their_id oid of their file
# @return 0 or an error code
#
git_index_reuc_add = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.c_char_p,
    ct.c_int,
    ct.POINTER(git_oid),
    ct.c_int,
    ct.POINTER(git_oid),
    ct.c_int,
    ct.POINTER(git_oid))(
    ("git_index_reuc_add", dll), (
    (1, "index"),
    (1, "path"),
    (1, "ancestor_mode"),
    (1, "ancestor_id"),
    (1, "our_mode"),
    (1, "our_id"),
    (1, "their_mode"),
    (1, "their_id"),))

# Remove an resolve undo entry from the index
#
# @param index an existing index object
# @param n position of the resolve undo entry to remove
# @return 0 or an error code
#
git_index_reuc_remove = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.c_size_t)(
    ("git_index_reuc_remove", dll), (
    (1, "index"),
    (1, "n"),))

# Remove all resolve undo entries from the index
#
# @param index an existing index object
# @return 0 or an error code
#
git_index_reuc_clear = CFUNC(ct.c_int,
    ct.POINTER(git_index))(
    ("git_index_reuc_clear", dll), (
    (1, "index"),))

# GIT_END_DECL
