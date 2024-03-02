# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa
from ..buffer import git_buf
from ..types  import git_repository
from ..index  import git_index_entry
from ..merge  import git_merge_file_options

# @file git2/sys/merge.h
# @brief Git merge driver backend and plugin routines
# @defgroup git_merge Git merge driver APIs
# @ingroup Git

# GIT_BEGIN_DECL

class git_merge_driver(ct.Structure): pass

# Look up a merge driver by name
#
# @param name The name of the merge driver
# @return Pointer to the merge driver object or NULL if not found
#
git_merge_driver_lookup = CFUNC(ct.POINTER(git_merge_driver),
    ct.c_char_p)(
    ("git_merge_driver_lookup", dll), (
    (1, "name"),))

GIT_MERGE_DRIVER_TEXT   = b"text"
GIT_MERGE_DRIVER_BINARY = b"binary"
GIT_MERGE_DRIVER_UNION  = b"union"

# A merge driver source represents the file to be merged
#
class git_merge_driver_source(ct.Structure): pass

# Get the repository that the source data is coming from.
git_merge_driver_source_repo = CFUNC(ct.POINTER(git_repository),
    ct.POINTER(git_merge_driver_source))(
    ("git_merge_driver_source_repo", dll), (
    (1, "src"),))

# Gets the ancestor of the file to merge.
git_merge_driver_source_ancestor = CFUNC(ct.POINTER(git_index_entry),
    ct.POINTER(git_merge_driver_source))(
    ("git_merge_driver_source_ancestor", dll), (
    (1, "src"),))

# Gets the ours side of the file to merge.
git_merge_driver_source_ours = CFUNC(ct.POINTER(git_index_entry),
    ct.POINTER(git_merge_driver_source))(
    ("git_merge_driver_source_ours", dll), (
    (1, "src"),))

# Gets the theirs side of the file to merge.
git_merge_driver_source_theirs = CFUNC(ct.POINTER(git_index_entry),
    ct.POINTER(git_merge_driver_source))(
    ("git_merge_driver_source_theirs", dll), (
    (1, "src"),))

# Gets the merge file options that the merge was invoked with
git_merge_driver_source_file_options = CFUNC(ct.POINTER(git_merge_file_options),
    ct.POINTER(git_merge_driver_source))(
    ("git_merge_driver_source_file_options", dll), (
    (1, "src"),))

# Initialize callback on merge driver
#
# Specified as `driver.initialize`, this is an optional callback invoked
# before a merge driver is first used.  It will be called once at most
# per library lifetime.
#
# If non-NULL, the merge driver's `initialize` callback will be invoked
# right before the first use of the driver, so you can defer expensive
# initialization operations (in case libgit2 is being used in a way that
# doesn't need the merge driver).
#
git_merge_driver_init_fn = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_merge_driver))  # self

# Shutdown callback on merge driver
#
# Specified as `driver.shutdown`, this is an optional callback invoked
# when the merge driver is unregistered or when libgit2 is shutting down.
# It will be called once at most and should release resources as needed.
# This may be called even if the `initialize` callback was not made.
#
# Typically this function will free the `git_merge_driver` object itself.
#
git_merge_driver_shutdown_fn = GIT_CALLBACK(None,
    ct.POINTER(git_merge_driver))  # self

# Callback to perform the merge.
#
# Specified as `driver.apply`, this is the callback that actually does the
# merge.  If it can successfully perform a merge, it should populate
# `path_out` with a pointer to the filename to accept, `mode_out` with
# the resultant mode, and `merged_out` with the buffer of the merged file
# and then return 0.  If the driver returns `GIT_PASSTHROUGH`, then the
# default merge driver should instead be run.  It can also return
# `GIT_EMERGECONFLICT` if the driver is not able to produce a merge result,
# and the file will remain conflicted.  Any other errors will fail and
# return to the caller.
#
# The `filter_name` contains the name of the filter that was invoked, as
# specified by the file's attributes.
#
# The `src` contains the data about the file to be merged.
#
git_merge_driver_apply_fn = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_merge_driver),         # self
    ct.POINTER(ct.c_char_p),              # path_out
    ct.POINTER(ct.c_uint32),              # mode_out
    ct.POINTER(git_buf),                  # merged_out
    ct.c_char_p,                          # filter_name
    ct.POINTER(git_merge_driver_source))  # src

# Merge driver structure used to register custom merge drivers.
#
# To associate extra data with a driver, allocate extra data and put the
# `git_merge_driver` struct at the start of your data buffer, then cast
# the `self` pointer to your larger structure when your callback is invoked.
#
class git_merge_driver(ct.Structure):
    _fields_ = [
    # The `version` should be set to `GIT_MERGE_DRIVER_VERSION`.
    ("version", ct.c_uint),

    # Called when the merge driver is first used for any file.
    ("initialize", git_merge_driver_init_fn),

    # Called when the merge driver is unregistered from the system.
    ("shutdown", git_merge_driver_shutdown_fn),

    # Called to merge the contents of a conflict.  If this function
    # returns `GIT_PASSTHROUGH` then the default (`text`) merge driver
    # will instead be invoked.  If this function returns
    # `GIT_EMERGECONFLICT` then the file will remain conflicted.
    #
    ("apply", git_merge_driver_apply_fn),
]

GIT_MERGE_DRIVER_VERSION = 1

# Register a merge driver under a given name.
#
# As mentioned elsewhere, the initialize callback will not be invoked
# immediately.  It is deferred until the driver is used in some way.
#
# Currently the merge driver registry is not thread safe, so any
# registering or deregistering of merge drivers must be done outside of
# any possible usage of the drivers (i.e. during application setup or
# shutdown).
#
# @param name The name of this driver to match an attribute.  Attempting
#          to register with an in-use name will return GIT_EEXISTS.
# @param driver The merge driver definition.  This pointer will be stored
#          as is by libgit2 so it must be a durable allocation (either
#          static or on the heap).
# @return 0 on successful registry, error code <0 on failure
#
git_merge_driver_register = CFUNC(ct.c_int,
    ct.c_char_p,
    ct.POINTER(git_merge_driver))(
    ("git_merge_driver_register", dll), (
    (1, "name"),
    (1, "driver"),))

# Remove the merge driver with the given name.
#
# Attempting to remove the builtin libgit2 merge drivers is not permitted
# and will return an error.
#
# Currently the merge driver registry is not thread safe, so any
# registering or deregistering of drivers must be done outside of any
# possible usage of the drivers (i.e. during application setup or shutdown).
#
# @param name The name under which the merge driver was registered
# @return 0 on success, error code <0 on failure
#
git_merge_driver_unregister = CFUNC(ct.c_int,
    ct.c_char_p)(
    ("git_merge_driver_unregister", dll), (
    (1, "name"),))

# GIT_END_DECL
