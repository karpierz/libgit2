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
from ..types  import git_odb_backend

# @file git2/sys/mempack.h
# @brief Custom ODB backend that permits packing objects in-memory
# @defgroup git_backend Git custom backend APIs
# @ingroup Git

# GIT_BEGIN_DECL

# Instantiate a new mempack backend.
#
# The backend must be added to an existing ODB with the highest
# priority.
#
#     git_mempack_new(&mempacker);
#     git_repository_odb(&odb, repository);
#     git_odb_add_backend(odb, mempacker, 999);
#
# Once the backend has been loaded, all writes to the ODB will
# instead be queued in memory, and can be finalized with
# `git_mempack_dump`.
#
# Subsequent reads will also be served from the in-memory store
# to ensure consistency, until the memory store is dumped.
#
# @param out Pointer where to store the ODB backend
# @return 0 on success; error code otherwise
#
git_mempack_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_odb_backend)))(
    ("git_mempack_new", dll), (
    (1, "out"),))

# Dump all the queued in-memory writes to a packfile.
#
# The contents of the packfile will be stored in the given buffer.
# It is the caller's responsibility to ensure that the generated
# packfile is available to the repository (e.g. by writing it
# to disk, or doing something crazy like distributing it across
# several copies of the repository over a network).
#
# Once the generated packfile is available to the repository,
# call `git_mempack_reset` to cleanup the memory store.
#
# Calling `git_mempack_reset` before the packfile has been
# written to disk will result in an inconsistent repository
# (the objects in the memory store won't be accessible).
#
# @param pack Buffer where to store the raw packfile
# @param repo The active repository where the backend is loaded
# @param backend The mempack backend
# @return 0 on success; error code otherwise
#
git_mempack_dump = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_repository),
    ct.POINTER(git_odb_backend))(
    ("git_mempack_dump", dll), (
    (1, "pack"),
    (1, "repo"),
    (1, "backend"),))

# Reset the memory packer by clearing all the queued objects.
#
# This assumes that `git_mempack_dump` has been called before to
# store all the queued objects into a single packfile.
#
# Alternatively, call `reset` without a previous dump to "undo"
# all the recently written objects, giving transaction-like
# semantics to the Git repository.
#
# @param backend The mempack backend
# @return 0 on success; error code otherwise
#
git_mempack_reset = CFUNC(ct.c_int,
    ct.POINTER(git_odb_backend))(
    ("git_mempack_reset", dll), (
    (1, "backend"),))

# GIT_END_DECL
