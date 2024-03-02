# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .oid    import git_oid
from .types  import git_signature
from .types  import git_repository
from .types  import git_reflog
from .types  import git_reflog_entry

# @file git2/reflog.h
# @brief Git reflog management routines
# @defgroup git_reflog Git reflog management routines
# @ingroup Git

# GIT_BEGIN_DECL

# Read the reflog for the given reference
#
# If there is no reflog file for the given
# reference yet, an empty reflog object will
# be returned.
#
# The reflog must be freed manually by using
# git_reflog_free().
#
# @param out pointer to reflog
# @param repo the repository
# @param name reference to look up
# @return 0 or an error code
#
git_reflog_read = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_reflog)),
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_reflog_read", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "name"),))

# Write an existing in-memory reflog object back to disk
# using an atomic file lock.
#
# @param reflog an existing reflog object
# @return 0 or an error code
#
git_reflog_write = CFUNC(ct.c_int,
    ct.POINTER(git_reflog))(
    ("git_reflog_write", dll), (
    (1, "reflog"),))

# Add a new entry to the in-memory reflog.
#
# `msg` is optional and can be NULL.
#
# @param reflog an existing reflog object
# @param id the OID the reference is now pointing to
# @param committer the signature of the committer
# @param msg the reflog message
# @return 0 or an error code
#
git_reflog_append = CFUNC(ct.c_int,
    ct.POINTER(git_reflog),
    ct.POINTER(git_oid),
    ct.POINTER(git_signature),
    ct.c_char_p)(
    ("git_reflog_append", dll), (
    (1, "reflog"),
    (1, "id"),
    (1, "committer"),
    (1, "msg"),))

# Rename a reflog
#
# The reflog to be renamed is expected to already exist
#
# The new name will be checked for validity.
# See `git_reference_create_symbolic()` for rules about valid names.
#
# @param repo the repository
# @param old_name the old name of the reference
# @param name the new name of the reference
# @return 0 on success, GIT_EINVALIDSPEC or an error code
#
git_reflog_rename = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.c_char_p)(
    ("git_reflog_rename", dll), (
    (1, "repo"),
    (1, "old_name"),
    (1, "name"),))

# Delete the reflog for the given reference
#
# @param repo the repository
# @param name the reflog to delete
# @return 0 or an error code
#
git_reflog_delete = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_reflog_delete", dll), (
    (1, "repo"),
    (1, "name"),))

# Get the number of log entries in a reflog
#
# @param reflog the previously loaded reflog
# @return the number of log entries
#
git_reflog_entrycount = CFUNC(ct.c_size_t,
    ct.POINTER(git_reflog))(
    ("git_reflog_entrycount", dll), (
    (1, "reflog"),))

# Lookup an entry by its index
#
# Requesting the reflog entry with an index of 0 (zero) will
# return the most recently created entry.
#
# @param reflog a previously loaded reflog
# @param idx the position of the entry to lookup. Should be greater than or
# equal to 0 (zero) and less than `git_reflog_entrycount()`.
# @return the entry; NULL if not found
#
git_reflog_entry_byindex = CFUNC(ct.POINTER(git_reflog_entry),
    ct.POINTER(git_reflog),
    ct.c_size_t)(
    ("git_reflog_entry_byindex", dll), (
    (1, "reflog"),
    (1, "idx"),))

# Remove an entry from the reflog by its index
#
# To ensure there's no gap in the log history, set `rewrite_previous_entry`
# param value to 1. When deleting entry `n`, member old_oid of entry `n-1`
# (if any) will be updated with the value of member new_oid of entry `n+1`.
#
# @param reflog a previously loaded reflog.
#
# @param idx the position of the entry to remove. Should be greater than or
# equal to 0 (zero) and less than `git_reflog_entrycount()`.
#
# @param rewrite_previous_entry 1 to rewrite the history; 0 otherwise.
#
# @return 0 on success, GIT_ENOTFOUND if the entry doesn't exist
# or an error code.
#
git_reflog_drop = CFUNC(ct.c_int,
    ct.POINTER(git_reflog),
    ct.c_size_t,
    ct.c_int)(
    ("git_reflog_drop", dll), (
    (1, "reflog"),
    (1, "idx"),
    (1, "rewrite_previous_entry"),))

# Get the old oid
#
# @param entry a reflog entry
# @return the old oid
#
git_reflog_entry_id_old = CFUNC(ct.POINTER(git_oid),
    ct.POINTER(git_reflog_entry))(
    ("git_reflog_entry_id_old", dll), (
    (1, "entry"),))

# Get the new oid
#
# @param entry a reflog entry
# @return the new oid at this time
#
git_reflog_entry_id_new = CFUNC(ct.POINTER(git_oid),
    ct.POINTER(git_reflog_entry))(
    ("git_reflog_entry_id_new", dll), (
    (1, "entry"),))

# Get the committer of this entry
#
# @param entry a reflog entry
# @return the committer
#
git_reflog_entry_committer = CFUNC(ct.POINTER(git_signature),
    ct.POINTER(git_reflog_entry))(
    ("git_reflog_entry_committer", dll), (
    (1, "entry"),))

# Get the log message
#
# @param entry a reflog entry
# @return the log msg
#
git_reflog_entry_message = CFUNC(ct.c_char_p,
    ct.POINTER(git_reflog_entry))(
    ("git_reflog_entry_message", dll), (
    (1, "entry"),))

# Free the reflog
#
# @param reflog reflog to free
#
git_reflog_free = CFUNC(None,
    ct.POINTER(git_reflog))(
    ("git_reflog_free", dll), (
    (1, "reflog"),))

# GIT_END_DECL
