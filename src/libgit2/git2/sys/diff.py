# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa
from ..diff   import git_diff
from ..diff   import git_diff_delta
from ..diff   import git_diff_hunk
from ..diff   import git_diff_line
from ..types  import git_status_list

# @file git2/sys/diff.h
# @brief Low-level Git diff utilities
# @ingroup Git

# GIT_BEGIN_DECL

# Diff print callback that writes to a git_buf.
#
# This function is provided not for you to call it directly, but instead
# so you can use it as a function pointer to the `git_diff_print` or
# `git_patch_print` APIs.  When using those APIs, you specify a callback
# to actually handle the diff and/or patch data.
#
# Use this callback to easily write that data to a `git_buf` buffer.  You
# must pass a `ct.POINTER(git_buf) ` value as the payload to the `git_diff_print`
# and/or `git_patch_print` function.  The data will be appended to the
# buffer (after any existing content).
#
git_diff_print_callback__to_buf = CFUNC(ct.c_int,
    ct.POINTER(git_diff_delta),
    ct.POINTER(git_diff_hunk),
    ct.POINTER(git_diff_line),
    ct.c_void_p)(  # payload must be a `ct.POINTER(git_buf)`
    ("git_diff_print_callback__to_buf", dll), (
    (1, "delta"),
    (1, "hunk"),
    (1, "line"),
    (1, "payload"),))

# Diff print callback that writes to stdio FILE handle.
#
# This function is provided not for you to call it directly, but instead
# so you can use it as a function pointer to the `git_diff_print` or
# `git_patch_print` APIs.  When using those APIs, you specify a callback
# to actually handle the diff and/or patch data.
#
# Use this callback to easily write that data to a stdio FILE handle.  You
# must pass a `FILE *` value (such as `stdout` or `stderr` or the return
# value from `fopen()`) as the payload to the `git_diff_print`
# and/or `git_patch_print` function.  If you pass NULL, this will write
# data to `stdout`.
#
git_diff_print_callback__to_file_handle = CFUNC(ct.c_int,
    ct.POINTER(git_diff_delta),
    ct.POINTER(git_diff_hunk),
    ct.POINTER(git_diff_line) ,
    ct.c_void_p)(  # payload must be a `FILE *`
    ("git_diff_print_callback__to_file_handle", dll), (
    (1, "delta"),
    (1, "hunk"),
    (1, "line"),
    (1, "payload"),))

# Performance data from diffing
#
class git_diff_perfdata(ct.Structure):
    _fields_ = [
    ("version",          ct.c_uint),
    ("stat_calls",       ct.c_size_t),  # Number of stat() calls performed
    ("oid_calculations", ct.c_size_t),  # Number of ID calculations
]

GIT_DIFF_PERFDATA_VERSION = 1
#define GIT_DIFF_PERFDATA_INIT {GIT_DIFF_PERFDATA_VERSION,0,0}

# Get performance data for a diff object.
#
# @param out Structure to be filled with diff performance data
# @param diff Diff to read performance data from
# @return 0 for success, <0 for error
#
git_diff_get_perfdata = CFUNC(ct.c_int,
    ct.POINTER(git_diff_perfdata),
    ct.POINTER(git_diff))(
    ("git_diff_get_perfdata", dll), (
    (1, "out"),
    (1, "diff"),))

# Get performance data for diffs from a git_status_list
#
git_status_list_get_perfdata = CFUNC(ct.c_int,
    ct.POINTER(git_diff_perfdata),
    ct.POINTER(git_status_list))(
    ("git_status_list_get_perfdata", dll), (
    (1, "out"),
    (1, "status"),))

# GIT_END_DECL
