# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa
from ..types  import git_repository
from ..types  import git_config
from ..types  import git_odb
from ..types  import git_refdb
from ..types  import git_index

# @file git2/sys/repository.h
# @brief Git repository custom implementation routines
# @defgroup git_backend Git custom backend APIs
# @ingroup Git

# GIT_BEGIN_DECL

# Create a new repository with neither backends nor config object
#
# Note that this is only useful if you wish to associate the repository
# with a non-filesystem-backed object database and config store.
#
# Caveats: since this repository has no physical location, some systems
# can fail to function properly: locations under $GIT_DIR, $GIT_COMMON_DIR,
# or $GIT_INFO_DIR are impacted.
#
# @param out The blank repository
# @return 0 on success, or an error code
#
git_repository_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_repository)))(
    ("git_repository_new", dll), (
    (1, "out"),))

# Reset all the internal state in a repository.
#
# This will free all the mapped memory and internal objects
# of the repository and leave it in a "blank" state.
#
# There's no need to call this function directly unless you're
# trying to aggressively cleanup the repo before its
# deallocation. `git_repository_free` already performs this operation
# before deallocating the repo.
#
# @param repo The repository to clean up
# @return 0 on success, or an error code
#
git_repository__cleanup = CFUNC(ct.c_int,
    ct.POINTER(git_repository))(
    ("git_repository__cleanup", dll), (
    (1, "repo"),))

# Update the filesystem config settings for an open repository
#
# When a repository is initialized, config values are set based on the
# properties of the filesystem that the repository is on, such as
# "core.ignorecase", "core.filemode", "core.symlinks", etc.  If the
# repository is moved to a new filesystem, these properties may no
# longer be correct and API calls may not behave as expected.  This
# call reruns the phase of repository initialization that sets those
# properties to compensate for the current filesystem of the repo.
#
# @param repo A repository object
# @param recurse_submodules Should submodules be updated recursively
# @return 0 on success, < 0 on error
#
git_repository_reinit_filesystem = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.c_int)(
    ("git_repository_reinit_filesystem", dll), (
    (1, "repo"),
    (1, "recurse_submodules"),))

# Set the configuration file for this repository
#
# This configuration file will be used for all configuration
# queries involving this repository.
#
# The repository will keep a reference to the config file;
# the user must still free the config after setting it
# to the repository, or it will leak.
#
# @param repo A repository object
# @param config A Config object
# @return 0 on success, or an error code
#
git_repository_set_config = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_config))(
    ("git_repository_set_config", dll), (
    (1, "repo"),
    (1, "config"),))

# Set the Object Database for this repository
#
# The ODB will be used for all object-related operations
# involving this repository.
#
# The repository will keep a reference to the ODB; the user
# must still free the ODB object after setting it to the
# repository, or it will leak.
#
# @param repo A repository object
# @param odb An ODB object
# @return 0 on success, or an error code
#
git_repository_set_odb = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_odb))(
    ("git_repository_set_odb", dll), (
    (1, "repo"),
    (1, "odb"),))

# Set the Reference Database Backend for this repository
#
# The refdb will be used for all reference related operations
# involving this repository.
#
# The repository will keep a reference to the refdb; the user
# must still free the refdb object after setting it to the
# repository, or it will leak.
#
# @param repo A repository object
# @param refdb An refdb object
# @return 0 on success, or an error code
#
git_repository_set_refdb = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_refdb))(
    ("git_repository_set_refdb", dll), (
    (1, "repo"),
    (1, "refdb"),))

# Set the index file for this repository
#
# This index will be used for all index-related operations
# involving this repository.
#
# The repository will keep a reference to the index file;
# the user must still free the index after setting it
# to the repository, or it will leak.
#
# @param repo A repository object
# @param index An index object
# @return 0 on success, or an error code
#
git_repository_set_index = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_index))(
    ("git_repository_set_index", dll), (
    (1, "repo"),
    (1, "index"),))

# Set a repository to be bare.
#
# Clear the working directory and set core.bare to true.  You may also
# want to call `git_repository_set_index(repo, NULL)` since a bare repo
# typically does not have an index, but this function will not do that
# for you.
#
# @param repo Repo to make bare
# @return 0 on success, <0 on failure
#
git_repository_set_bare = CFUNC(ct.c_int,
    ct.POINTER(git_repository))(
    ("git_repository_set_bare", dll), (
    (1, "repo"),))

# Load and cache all submodules.
#
# Because the `.gitmodules` file is unstructured, loading submodules is an
# O(N) operation.  Any operation (such as `git_rebase_init`) that requires
# accessing all submodules is O(N^2) in the number of submodules, if it
# has to look each one up individually.  This function loads all submodules
# and caches them so that subsequent calls to `git_submodule_lookup` are O(1).
#
# @param repo the repository whose submodules will be cached.
#
git_repository_submodule_cache_all = CFUNC(ct.c_int,
    ct.POINTER(git_repository))(
    ("git_repository_submodule_cache_all", dll), (
    (1, "repo"),))

# Clear the submodule cache.
#
# Clear the submodule cache populated by `git_repository_submodule_cache_all`.
# If there is no cache, do nothing.
#
# The cache incorporates data from the repository's configuration, as well
# as the state of the working tree, the index, and HEAD.  So any time any
# of these has changed, the cache might become invalid.
#
# @param repo the repository whose submodule cache will be cleared
#
git_repository_submodule_cache_clear = CFUNC(ct.c_int,
    ct.POINTER(git_repository))(
    ("git_repository_submodule_cache_clear", dll), (
    (1, "repo"),))

# GIT_END_DECL
