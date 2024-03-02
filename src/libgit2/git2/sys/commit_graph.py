# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa
from ..oid    import git_oid_t
from ..buffer import git_buf
from ..types  import git_repository
from ..types  import git_commit_graph
from ..types  import git_commit_graph_writer
from ..types  import git_revwalk

# @file git2/sys/commit_graph.h
# @brief Git commit-graph
# @defgroup git_commit_graph Git commit-graph APIs
# @ingroup Git

# GIT_BEGIN_DECL

# Opens a `git_commit_graph` from a path to an objects directory.
#
# This finds, opens, and validates the `commit-graph` file.
#
# @param cgraph_out the `git_commit_graph` struct to initialize.
# @param objects_dir the path to a git objects directory.
# @return Zero on success; -1 on failure.
#
if defined("GIT_EXPERIMENTAL_SHA256"):
    git_commit_graph_open = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_commit_graph)),
        ct.c_char_p,
        git_oid_t)(
        ("git_commit_graph_open", dll), (
        (1, "cgraph_out"),
        (1, "objects_dir"),
        (1, "oid_type"),))
else:
    git_commit_graph_open = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_commit_graph)),
        ct.c_char_p)(
        ("git_commit_graph_open", dll), (
        (1, "cgraph_out"),
        (1, "objects_dir"),))
# endif

# Frees commit-graph data. This should only be called when memory allocated
# using `git_commit_graph_open` is not returned to libgit2 because it was not
# associated with the ODB through a successful call to
# `git_odb_set_commit_graph`.
#
# @param cgraph the commit-graph object to free. If NULL, no action is taken.
#
git_commit_graph_free = CFUNC(None,
    ct.POINTER(git_commit_graph))(
    ("git_commit_graph_free", dll), (
    (1, "cgraph"),))

# Create a new writer for `commit-graph` files.
#
# @param out Location to store the writer pointer.
# @param objects_info_dir The `objects/info` directory.
# The `commit-graph` file will be written in this directory.
# @return 0 or an error code
#
if defined("GIT_EXPERIMENTAL_SHA256"):
    git_commit_graph_writer_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_commit_graph_writer)),
        ct.c_char_p,
        git_oid_t)(
        ("git_commit_graph_writer_new", dll), (
        (1, "out"),
        (1, "objects_info_dir"),
        (1, "oid_type"),))
else:
    git_commit_graph_writer_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_commit_graph_writer)),
        ct.c_char_p)(
        ("git_commit_graph_writer_new", dll), (
        (1, "out"),
        (1, "objects_info_dir"),))
# endif

# Free the commit-graph writer and its resources.
#
# @param w The writer to free. If NULL no action is taken.
#
git_commit_graph_writer_free = CFUNC(None,
    ct.POINTER(git_commit_graph_writer))(
    ("git_commit_graph_writer_free", dll), (
    (1, "w"),))

# Add an `.idx` file (associated to a packfile) to the writer.
#
# @param w The writer.
# @param repo The repository that owns the `.idx` file.
# @param idx_path The path of an `.idx` file.
# @return 0 or an error code
#
git_commit_graph_writer_add_index_file = CFUNC(ct.c_int,
    ct.POINTER(git_commit_graph_writer),
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_commit_graph_writer_add_index_file", dll), (
    (1, "w"),
    (1, "repo"),
    (1, "idx_path"),))

# Add a revwalk to the writer. This will add all the commits from the revwalk
# to the commit-graph.
#
# @param w The writer.
# @param walk The git_revwalk.
# @return 0 or an error code
#
git_commit_graph_writer_add_revwalk = CFUNC(ct.c_int,
    ct.POINTER(git_commit_graph_writer),
    ct.POINTER(git_revwalk))(
    ("git_commit_graph_writer_add_revwalk", dll), (
    (1, "w"),
    (1, "walk"),))

# The strategy to use when adding a new set of commits to a pre-existing
# commit-graph chain.
#
git_commit_graph_split_strategy_t = ct.c_int
(   # Do not split commit-graph files. The other split strategy-related option
    # fields are ignored.
    #
    GIT_COMMIT_GRAPH_SPLIT_STRATEGY_SINGLE_FILE,
) = (0,)

# Options structure for
# `git_commit_graph_writer_commit`/`git_commit_graph_writer_dump`.
#
# Initialize with `GIT_COMMIT_GRAPH_WRITER_OPTIONS_INIT`. Alternatively, you
# can use `git_commit_graph_writer_options_init`.
#
class git_commit_graph_writer_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # The strategy to use when adding new commits to a pre-existing commit-graph
    # chain.
    #
    ("split_strategy", git_commit_graph_split_strategy_t),

    # The number of commits in level N is less than X times the number of
    # commits in level N + 1. Default is 2.
    #
    ("size_multiple", ct.c_float),

    # The number of commits in level N + 1 is more than C commits.
    # Default is 64000.
    #
    ("max_commits", ct.c_size_t),
]

GIT_COMMIT_GRAPH_WRITER_OPTIONS_VERSION = 1
#define GIT_COMMIT_GRAPH_WRITER_OPTIONS_INIT = { GIT_COMMIT_GRAPH_WRITER_OPTIONS_VERSION }

# Initialize git_commit_graph_writer_options structure
#
# Initializes a `git_commit_graph_writer_options` with default values. Equivalent to
# creating an instance with `GIT_COMMIT_GRAPH_WRITER_OPTIONS_INIT`.
#
# @param opts The `git_commit_graph_writer_options` struct to initialize.
# @param version The struct version; pass `GIT_COMMIT_GRAPH_WRITER_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_commit_graph_writer_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_commit_graph_writer_options),
    ct.c_uint)(
    ("", dll), (
    (1, "opts"),
    (1, "version"),))

# Write a `commit-graph` file to a file.
#
# @param w The writer
# @param opts Pointer to git_commit_graph_writer_options struct.
# @return 0 or an error code
#
git_commit_graph_writer_commit = CFUNC(ct.c_int,
    ct.POINTER(git_commit_graph_writer),
    ct.POINTER(git_commit_graph_writer_options))(
    ("git_commit_graph_writer_commit", dll), (
    (1, "w"),
    (1, "opts"),))

# Dump the contents of the `commit-graph` to an in-memory buffer.
#
# @param buffer Buffer where to store the contents of the `commit-graph`.
# @param w The writer.
# @param opts Pointer to git_commit_graph_writer_options struct.
# @return 0 or an error code
#
git_commit_graph_writer_dump = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_commit_graph_writer),
    ct.POINTER(git_commit_graph_writer_options))(
    ("git_commit_graph_writer_dump", dll), (
    (1, "buffer"),
    (1, "w"),
    (1, "opts"),))

# GIT_END_DECL
