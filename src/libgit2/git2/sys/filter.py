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
from ..types  import git_writestream
from ..filter import git_filter_mode_t
from ..filter import git_filter
from ..filter import git_filter_list

# @file git2/sys/filter.h
# @brief Git filter backend and plugin routines
# @defgroup git_backend Git custom backend APIs
# @ingroup Git

# GIT_BEGIN_DECL

# Look up a filter by name
#
# @param name The name of the filter
# @return Pointer to the filter object or NULL if not found
#
git_filter_lookup = CFUNC(ct.POINTER(git_filter),
    ct.c_char_p)(
    ("git_filter_lookup", dll), (
    (1, "name"),))

GIT_FILTER_CRLF  = b"crlf"
GIT_FILTER_IDENT = b"ident"

# This is priority that the internal CRLF filter will be registered with
#
GIT_FILTER_CRLF_PRIORITY = 0

# This is priority that the internal ident filter will be registered with
#
GIT_FILTER_IDENT_PRIORITY = 100

# This is priority to use with a custom filter to imitate a core Git
# filter driver, so that it will be run last on checkout and first on
# checkin.  You do not have to use this, but it helps compatibility.
#
GIT_FILTER_DRIVER_PRIORITY = 200

# Create a new empty filter list
#
# Normally you won't use this because `git_filter_list_load` will create
# the filter list for you, but you can use this in combination with the
# `git_filter_lookup` and `git_filter_list_push` functions to assemble
# your own chains of filters.
#
git_filter_list_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_filter_list)),
    ct.POINTER(git_repository),
    git_filter_mode_t,
    ct.c_uint32)(
    ("git_filter_list_new", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "mode"),
    (1, "options"),))

# Add a filter to a filter list with the given payload.
#
# Normally you won't have to do this because the filter list is created
# by calling the "check" function on registered filters when the filter
# attributes are set, but this does allow more direct manipulation of
# filter lists when desired.
#
# Note that normally the "check" function can set up a payload for the
# filter.  Using this function, you can either pass in a payload if you
# know the expected payload format, or you can pass NULL.  Some filters
# may fail with a NULL payload.  Good luck!
#
git_filter_list_push = CFUNC(ct.c_int,
    ct.POINTER(git_filter_list),
    ct.POINTER(git_filter),
    ct.c_void_p)(
    ("git_filter_list_push", dll), (
    (1, "fl"),
    (1, "filter"),
    (1, "payload"),))

# Look up how many filters are in the list
#
# We will attempt to apply all of these filters to any data passed in,
# but note that the filter apply action still has the option of skipping
# data that is passed in (for example, the CRLF filter will skip data
# that appears to be binary).
#
# @param fl A filter list
# @return The number of filters in the list
#
git_filter_list_length = CFUNC(ct.c_size_t,
    ct.POINTER(git_filter_list))(
    ("git_filter_list_length", dll), (
    (1, "fl"),))

# A filter source represents a file/blob to be processed
#
class git_filter_source(ct.Structure): pass

# Get the repository that the source data is coming from.
#
git_filter_source_repo = CFUNC(ct.POINTER(git_repository),
    ct.POINTER(git_filter_source))(
    ("git_filter_source_repo", dll), (
    (1, "src"),))

# Get the path that the source data is coming from.
#
git_filter_source_path = CFUNC(ct.c_char_p,
    ct.POINTER(git_filter_source))(
    ("git_filter_source_path", dll), (
    (1, "src"),))

# Get the file mode of the source file
# If the mode is unknown, this will return 0
#
git_filter_source_filemode = CFUNC(ct.c_uint16,
    ct.POINTER(git_filter_source))(
    ("git_filter_source_filemode", dll), (
    (1, "src"),))

# Get the OID of the source
# If the OID is unknown (often the case with GIT_FILTER_CLEAN) then
# this will return NULL.
#
git_filter_source_id = CFUNC(ct.POINTER(git_oid),
    ct.POINTER(git_filter_source))(
    ("git_filter_source_id", dll), (
    (1, "src"),))

# Get the git_filter_mode_t to be used
#
git_filter_source_mode = CFUNC(git_filter_mode_t,
    ct.POINTER(git_filter_source))(
    ("git_filter_source_mode", dll), (
    (1, "src"),))

# Get the combination git_filter_flag_t options to be applied
#
git_filter_source_flags = CFUNC(ct.c_uint32,
    ct.POINTER(git_filter_source))(
    ("git_filter_source_flags", dll), (
    (1, "src"),))

# Initialize callback on filter
#
# Specified as `filter.initialize`, this is an optional callback invoked
# before a filter is first used.  It will be called once at most.
#
# If non-NULL, the filter's `initialize` callback will be invoked right
# before the first use of the filter, so you can defer expensive
# initialization operations (in case libgit2 is being used in a way that
# doesn't need the filter).
#
git_filter_init_fn = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_filter))  # self

# Shutdown callback on filter
#
# Specified as `filter.shutdown`, this is an optional callback invoked
# when the filter is unregistered or when libgit2 is shutting down.  It
# will be called once at most and should release resources as needed.
# This may be called even if the `initialize` callback was not made.
#
# Typically this function will free the `git_filter` object itself.
#
git_filter_shutdown_fn = GIT_CALLBACK(None,
    ct.POINTER(git_filter))  # self

# Callback to decide if a given source needs this filter
#
# Specified as `filter.check`, this is an optional callback that checks
# if filtering is needed for a given source.
#
# It should return 0 if the filter should be applied (i.e. success),
# GIT_PASSTHROUGH if the filter should not be applied, or an error code
# to fail out of the filter processing pipeline and return to the caller.
#
# The `attr_values` will be set to the values of any attributes given in
# the filter definition.  See `git_filter` below for more detail.
#
# The `payload` will be a pointer to a reference payload for the filter.
# This will start as NULL, but `check` can assign to this pointer for
# later use by the `stream` callback.  Note that the value should be heap
# allocated (not stack), so that it doesn't go away before the `stream`
# callback can use it.  If a filter allocates and assigns a value to the
# `payload`, it will need a `cleanup` callback to free the payload.
#
git_filter_check_fn = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_filter),         # self
    ct.POINTER(ct.c_void_p),        # payload # NULL on entry, may be set
    ct.POINTER(git_filter_source),  # src
    ct.POINTER(ct.c_char_p))        # attr_values

if not defined("GIT_DEPRECATE_HARD"):
    # Callback to actually perform the data filtering
    #
    # Specified as `filter.apply`, this is the callback that actually filters
    # data.  If it successfully writes the output, it should return 0.  Like
    # `check`, it can return GIT_PASSTHROUGH to indicate that the filter
    # doesn't want to run.  Other error codes will stop filter processing and
    # return to the caller.
    #
    # The `payload` value will refer to any payload that was set by the
    # `check` callback.  It may be read from or written to as needed.
    #
    # @deprecated use git_filter_stream_fn
    #
    git_filter_apply_fn = GIT_CALLBACK(ct.c_int,
        ct.POINTER(git_filter),         # self
        ct.POINTER(ct.c_void_p),        # payload # may be read and/or set
        ct.POINTER(git_buf),            # to
        ct.POINTER(git_buf),            # from
        ct.POINTER(git_filter_source))  # src
# endif

# Callback to perform the data filtering.
#
# Specified as `filter.stream`, this is a callback that filters data
# in a streaming manner.  This function will provide a
# `git_writestream` that will the original data will be written to;
# with that data, the `git_writestream` will then perform the filter
# translation and stream the filtered data out to the `next` location.
#
git_filter_stream_fn = GIT_CALLBACK(ct.c_int,
    ct.POINTER(ct.POINTER(git_writestream)),  # out
    ct.POINTER(git_filter),                   # self
    ct.POINTER(ct.c_void_p),                  # payload
    ct.POINTER(git_filter_source),            # src
    ct.POINTER(git_writestream))              # next

# Callback to clean up after filtering has been applied
#
# Specified as `filter.cleanup`, this is an optional callback invoked
# after the filter has been applied.  If the `check`, `apply`, or
# `stream` callbacks allocated a `payload` to keep per-source filter
# state, use this callback to free that payload and release resources
# as required.
#
git_filter_cleanup_fn = GIT_CALLBACK(None,
    ct.POINTER(git_filter),  # self
    ct.c_void_p)             # payload

# Filter structure used to register custom filters.
#
# To associate extra data with a filter, allocate extra data and put the
# `git_filter` struct at the start of your data buffer, then cast the
# `self` pointer to your larger structure when your callback is invoked.
#
class git_filter(ct.Structure):
    _fields_ = [
    # The `version` field should be set to `GIT_FILTER_VERSION`.
    ("version", ct.c_uint),

    # A whitespace-separated list of attribute names to check for this
    # filter (e.g. "eol crlf text").  If the attribute name is bare, it
    # will be simply loaded and passed to the `check` callback.  If it
    # has a value (i.e. "name=value"), the attribute must match that
    # value for the filter to be applied.  The value may be a wildcard
    # (eg, "name=*"), in which case the filter will be invoked for any
    # value for the given attribute name.  See the attribute parameter
    # of the `check` callback for the attribute value that was specified.
    #
    ("attributes", ct.c_char_p),

    # Called when the filter is first used for any file.
    ("initialize", git_filter_init_fn),

    # Called when the filter is removed or unregistered from the system.
    ("shutdown", git_filter_shutdown_fn),

    # Called to determine whether the filter should be invoked for a
    # given file.  If this function returns `GIT_PASSTHROUGH` then the
    # `stream` or `apply` functions will not be invoked and the
    # contents will be passed through unmodified.
    #
    ("check", git_filter_check_fn),

    *([("reserved", ct.c_void_p)]
      if defined("GIT_DEPRECATE_HARD") else
      # Provided for backward compatibility; this will apply the
      # filter to the given contents in a `git_buf`.  Callers should
      # provide a `stream` function instead.
      #
      [("apply", git_filter_apply_fn)]),

    # Called to apply the filter, this function will provide a
    # `git_writestream` that will the original data will be
    # written to; with that data, the `git_writestream` will then
    # perform the filter translation and stream the filtered data
    # out to the `next` location.
    #
    ("stream", git_filter_stream_fn),

    # Called when the system is done filtering for a file.
    ("cleanup", git_filter_cleanup_fn),
]

GIT_FILTER_VERSION = 1
#define GIT_FILTER_INIT = {GIT_FILTER_VERSION}

# Initializes a `git_filter` with default values. Equivalent to
# creating an instance with GIT_FILTER_INIT.
#
# @param filter the `git_filter` struct to initialize.
# @param version Version the struct; pass `GIT_FILTER_VERSION`
# @return Zero on success; -1 on failure.
#
git_filter_init = CFUNC(ct.c_int,
    ct.POINTER(git_filter),
    ct.c_uint)(
    ("git_filter_init", dll), (
    (1, "filter"),
    (1, "version"),))

# Register a filter under a given name with a given priority.
#
# As mentioned elsewhere, the initialize callback will not be invoked
# immediately.  It is deferred until the filter is used in some way.
#
# A filter's attribute checks and `check` and `stream` (or `apply`)
# callbacks will be issued in order of `priority` on smudge (to
# workdir), and in reverse order of `priority` on clean (to odb).
#
# Two filters are preregistered with libgit2:
# - GIT_FILTER_CRLF with priority 0
# - GIT_FILTER_IDENT with priority 100
#
# Currently the filter registry is not thread safe, so any registering or
# deregistering of filters must be done outside of any possible usage of
# the filters (i.e. during application setup or shutdown).
#
# @param name A name by which the filter can be referenced.  Attempting
#          to register with an in-use name will return GIT_EEXISTS.
# @param filter The filter definition.  This pointer will be stored as is
#          by libgit2 so it must be a durable allocation (either static
#          or on the heap).
# @param priority The priority for filter application
# @return 0 on successful registry, error code <0 on failure
#
git_filter_register = CFUNC(ct.c_int,
    ct.c_char_p,
    ct.POINTER(git_filter),
    ct.c_int)(
    ("git_filter_register", dll), (
    (1, "name"),
    (1, "filter"),
    (1, "priority"),))

# Remove the filter with the given name
#
# Attempting to remove the builtin libgit2 filters is not permitted and
# will return an error.
#
# Currently the filter registry is not thread safe, so any registering or
# deregistering of filters must be done outside of any possible usage of
# the filters (i.e. during application setup or shutdown).
#
# @param name The name under which the filter was registered
# @return 0 on success, error code <0 on failure
#
git_filter_unregister = CFUNC(ct.c_int,
    ct.c_char_p)(
    ("git_filter_unregister", dll), (
    (1, "name"),))

# GIT_END_DECL
