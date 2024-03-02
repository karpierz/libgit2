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
from ..types  import git_midx_writer

# @file git2/midx.h
# @brief Git multi-pack-index routines
# @defgroup git_midx Git multi-pack-index routines
# @ingroup Git

# GIT_BEGIN_DECL

# Create a new writer for `multi-pack-index` files.
#
# @param out location to store the writer pointer.
# @param pack_dir the directory where the `.pack` and `.idx` files are. The
# `multi-pack-index` file will be written in this directory, too.
# @return 0 or an error code
#
if defined("GIT_EXPERIMENTAL_SHA256"):
    git_midx_writer_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_midx_writer)),
        ct.c_char_p,
        git_oid_t)(
        ("git_midx_writer_new", dll), (
        (1, "out"),
        (1, "pack_dir"),
        (1, "oid_type"),))
else:
    git_midx_writer_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_midx_writer)),
        ct.c_char_p)(
        ("git_midx_writer_new", dll), (
        (1, "out"),
        (1, "pack_dir"),))

# Free the multi-pack-index writer and its resources.
#
# @param w the writer to free. If NULL no action is taken.
#
git_midx_writer_free = CFUNC(None,
    ct.POINTER(git_midx_writer))(
    ("git_midx_writer_free", dll), (
    (1, "w"),))

# Add an `.idx` file to the writer.
#
# @param w the writer
# @param idx_path the path of an `.idx` file.
# @return 0 or an error code
#
git_midx_writer_add = CFUNC(ct.c_int,
    ct.POINTER(git_midx_writer),
    ct.c_char_p)(
    ("git_midx_writer_add", dll), (
    (1, "w"),
    (1, "idx_path"),))

# Write a `multi-pack-index` file to a file.
#
# @param w the writer
# @return 0 or an error code
#
git_midx_writer_commit = CFUNC(ct.c_int,
    ct.POINTER(git_midx_writer))(
    ("git_midx_writer_commit", dll), (
    (1, "w"),))

# Dump the contents of the `multi-pack-index` to an in-memory buffer.
#
# @param midx Buffer where to store the contents of the `multi-pack-index`.
# @param w the writer
# @return 0 or an error code
#
git_midx_writer_dump = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_midx_writer))(
    ("git_midx_writer_dump", dll), (
    (1, "midx"),
    (1, "w"),))

# GIT_END_DECL
