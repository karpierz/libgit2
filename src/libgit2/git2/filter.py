# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .oid    import git_oid
from .buffer import git_buf
from .types  import git_repository
from .types  import git_blob
from .types  import git_writestream

# @file git2/filter.h
# @brief Git filter APIs
#
# @ingroup Git

# GIT_BEGIN_DECL

# Filters are applied in one of two directions: smudging - which is
# exporting a file from the Git object database to the working directory,
# and cleaning - which is importing a file from the working directory to
# the Git object database.  These values control which direction of
# change is being applied.
#
git_filter_mode_t = ct.c_int
(   GIT_FILTER_TO_WORKTREE,
    GIT_FILTER_SMUDGE,
    GIT_FILTER_TO_ODB,
    GIT_FILTER_CLEAN,
) = (0,
     0, # == GIT_FILTER_TO_WORKTREE
     1,
     1) # == GIT_FILTER_TO_ODB

# Filter option flags.
#
git_filter_flag_t = ct.c_int
(
    GIT_FILTER_DEFAULT,

    # Don't error for `safecrlf` violations, allow them to continue.
    GIT_FILTER_ALLOW_UNSAFE,

    # Don't load `/etc/gitattributes` (or the system equivalent)
    GIT_FILTER_NO_SYSTEM_ATTRIBUTES,

    # Load attributes from `.gitattributes` in the root of HEAD
    GIT_FILTER_ATTRIBUTES_FROM_HEAD,

    # Load attributes from `.gitattributes` in a given commit.
    # This can only be specified in a `git_filter_options`.
    GIT_FILTER_ATTRIBUTES_FROM_COMMIT,

) = (0, 1 << 0, 1 << 1, 1 << 2, 1 << 3)

# Filtering options
#
class git_filter_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # See `git_filter_flag_t` above
    ("flags", ct.c_uint32),

    *([("reserved",  ct.c_void_p)]
      if defined("GIT_DEPRECATE_HARD") else
      [("commit_id", ct.POINTER(git_oid))]),

    # The commit to load attributes from, when
    # `GIT_FILTER_ATTRIBUTES_FROM_COMMIT` is specified.
    #
    ("attr_commit_id", git_oid),
]

GIT_FILTER_OPTIONS_VERSION = 1
#define GIT_FILTER_OPTIONS_INIT = { GIT_FILTER_OPTIONS_VERSION }

# A filter that can transform file data
#
# This represents a filter that can be used to transform or even replace
# file data.  Libgit2 includes one built in filter and it is possible to
# write your own (see git2/sys/filter.h for information on that).
#
# The two builtin filters are:
#
# * "crlf" which uses the complex rules with the "text", "eol", and
#   "crlf" file attributes to decide how to convert between LF and CRLF
#   line endings
# * "ident" which replaces "$Id$" in a blob with "$Id: <blob OID>$" upon
#   checkout and replaced "$Id: <anything>$" with "$Id$" on checkin.
#
class git_filter(ct.Structure): pass

# List of filters to be applied
#
# This represents a list of filters to be applied to a file / blob.  You
# can build the list with one call, apply it with another, and dispose it
# with a third.  In typical usage, there are not many occasions where a
# git_filter_list is needed directly since the library will generally
# handle conversions for you, but it can be convenient to be able to
# build and apply the list sometimes.
#
class git_filter_list(ct.Structure): pass

# Load the filter list for a given path.
#
# This will return 0 (success) but set the output git_filter_list to NULL
# if no filters are requested for the given file.
#
# @param filters Output newly created git_filter_list (or NULL)
# @param repo Repository object that contains `path`
# @param blob The blob to which the filter will be applied (if known)
# @param path Relative path of the file to be filtered
# @param mode Filtering direction (WT->ODB or ODB->WT)
# @param flags Combination of `git_filter_flag_t` flags
# @return 0 on success (which could still return NULL if no filters are
#         needed for the requested file), <0 on error
#
git_filter_list_load = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_filter_list)),
    ct.POINTER(git_repository),
    ct.POINTER(git_blob),  # can be NULL #
    ct.c_char_p,
    git_filter_mode_t,
    ct.c_uint32)(
    ("git_filter_list_load", dll), (
    (1, "filters"),
    (1, "repo"),
    (1, "blob"),
    (1, "path"),
    (1, "mode"),
    (1, "flags"),))

# Load the filter list for a given path.
#
# This will return 0 (success) but set the output git_filter_list to NULL
# if no filters are requested for the given file.
#
# @param filters Output newly created git_filter_list (or NULL)
# @param repo Repository object that contains `path`
# @param blob The blob to which the filter will be applied (if known)
# @param path Relative path of the file to be filtered
# @param mode Filtering direction (WT->ODB or ODB->WT)
# @param opts The `git_filter_options` to use when loading filters
# @return 0 on success (which could still return NULL if no filters are
#         needed for the requested file), <0 on error
#
git_filter_list_load_ext = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_filter_list)),
    ct.POINTER(git_repository),
    ct.POINTER(git_blob),
    ct.c_char_p,
    git_filter_mode_t,
    ct.POINTER(git_filter_options))(
    ("git_filter_list_load_ext", dll), (
    (1, "filters"),
    (1, "repo"),
    (1, "blob"),
    (1, "path"),
    (1, "mode"),
    (1, "opts"),))

# Query the filter list to see if a given filter (by name) will run.
# The built-in filters "crlf" and "ident" can be queried, otherwise this
# is the name of the filter specified by the filter attribute.
#
# This will return 0 if the given filter is not in the list, or 1 if
# the filter will be applied.
#
# @param filters A loaded git_filter_list (or NULL)
# @param name The name of the filter to query
# @return 1 if the filter is in the list, 0 otherwise
#
git_filter_list_contains = CFUNC(ct.c_int,
    ct.POINTER(git_filter_list),
    ct.c_char_p)(
    ("git_filter_list_contains", dll), (
    (1, "filters"),
    (1, "name"),))

# Apply filter list to a data buffer.
#
# @param out Buffer to store the result of the filtering
# @param filters A loaded git_filter_list (or NULL)
# @param in Buffer containing the data to filter
# @param in_len The length of the input buffer
# @return 0 on success, an error code otherwise
#
git_filter_list_apply_to_buffer = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_filter_list),
    git_buffer_t,
    ct.c_size_t)(
    ("git_filter_list_apply_to_buffer", dll), (
    (1, "out"),
    (1, "filters"),
    (1, "in"),
    (1, "in_len"),))

# Apply a filter list to the contents of a file on disk
#
# @param out buffer into which to store the filtered file
# @param filters the list of filters to apply
# @param repo the repository in which to perform the filtering
# @param path the path of the file to filter, a relative path will be
# taken as relative to the workdir
# @return 0 or an error code.
#
git_filter_list_apply_to_file = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_filter_list),
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_filter_list_apply_to_file", dll), (
    (1, "out"),
    (1, "filters"),
    (1, "repo"),
    (1, "path"),))

# Apply a filter list to the contents of a blob
#
# @param out buffer into which to store the filtered file
# @param filters the list of filters to apply
# @param blob the blob to filter
# @return 0 or an error code.
#
git_filter_list_apply_to_blob = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_filter_list),
    ct.POINTER(git_blob))(
    ("git_filter_list_apply_to_blob", dll), (
    (1, "out"),
    (1, "filters"),
    (1, "blob"),))

# Apply a filter list to an arbitrary buffer as a stream
#
# @param filters the list of filters to apply
# @param buffer the buffer to filter
# @param len the size of the buffer
# @param target the stream into which the data will be written
# @return 0 or an error code.
#
git_filter_list_stream_buffer = CFUNC(ct.c_int,
    ct.POINTER(git_filter_list),
    git_buffer_t,
    ct.c_size_t,
    ct.POINTER(git_writestream))(
    ("git_filter_list_stream_buffer", dll), (
    (1, "filters"),
    (1, "buffer"),
    (1, "len"),
    (1, "target"),))

# Apply a filter list to a file as a stream
#
# @param filters the list of filters to apply
# @param repo the repository in which to perform the filtering
# @param path the path of the file to filter, a relative path will be
# taken as relative to the workdir
# @param target the stream into which the data will be written
# @return 0 or an error code.
#
git_filter_list_stream_file = CFUNC(ct.c_int,
    ct.POINTER(git_filter_list),
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.POINTER(git_writestream))(
    ("git_filter_list_stream_file", dll), (
    (1, "filters"),
    (1, "repo"),
    (1, "path"),
    (1, "target"),))

# Apply a filter list to a blob as a stream
#
# @param filters the list of filters to apply
# @param blob the blob to filter
# @param target the stream into which the data will be written
# @return 0 or an error code.
#
git_filter_list_stream_blob = CFUNC(ct.c_int,
    ct.POINTER(git_filter_list),
    ct.POINTER(git_blob),
    ct.POINTER(git_writestream))(
    ("git_filter_list_stream_blob", dll), (
    (1, "filters"),
    (1, "blob"),
    (1, "target"),))

# Free a git_filter_list
#
# @param filters A git_filter_list created by `git_filter_list_load`
#
git_filter_list_free = CFUNC(None,
    ct.POINTER(git_filter_list))(
    ("git_filter_list_free", dll), (
    (1, "filters"),))

# GIT_END_DECL
