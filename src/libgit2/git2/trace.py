# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa

# @file git2/trace.h
# @brief Git tracing configuration routines
# @defgroup git_trace Git tracing configuration routines
# @ingroup Git

# GIT_BEGIN_DECL

# Available tracing levels.  When tracing is set to a particular level,
# callers will be provided tracing at the given level and all lower levels.
#
git_trace_level_t = ct.c_int
(   # No tracing will be performed.
    GIT_TRACE_NONE,
    # Severe errors that may impact the program's execution
    GIT_TRACE_FATAL,
    # Errors that do not impact the program's execution
    GIT_TRACE_ERROR,
    # Warnings that suggest abnormal data
    GIT_TRACE_WARN,
    # Informational messages about program execution
    GIT_TRACE_INFO,
    # Detailed data that allows for debugging
    GIT_TRACE_DEBUG,
    # Exceptionally detailed debugging data
    GIT_TRACE_TRACE,
) = (0, 1, 2, 3, 4, 5, 6)

# An instance for a tracing function
#
git_trace_cb = GIT_CALLBACK(None,
    git_trace_level_t,  # level
    ct.c_char_p)        # msg

# Sets the system tracing configuration to the specified level with the
# specified callback.  When system events occur at a level equal to, or
# lower than, the given level they will be reported to the given callback.
#
# @param level Level to set tracing to
# @param cb Function to call with trace data
# @return 0 or an error code
#
git_trace_set = CFUNC(ct.c_int,
    git_trace_level_t,
    git_trace_cb)(
    ("git_trace_set", dll), (
    (1, "level"),
    (1, "cb"),))

# GIT_END_DECL
