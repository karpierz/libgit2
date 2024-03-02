# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa

# @file git2/types.h
# @brief libgit2 base & compatibility types
# @ingroup Git

# GIT_BEGIN_DECL

# Cross-platform compatibility types for off_t / time_t
#
# NOTE: This needs to be in a public header so that both the library
# implementation and client applications both agree on the same types.
# Otherwise we get undefined behavior.
#
# Use the "best" types that each platform provides. Currently we truncate
# these intermediate representations for compatibility with the git ABI, but
# if and when it changes to support 64 bit types, our code will naturally
# adapt.
# NOTE: These types should match those that are returned by our internal
# stat() functions, for all platforms.

git_off_t = ct.c_int64

# time in seconds from epoch ; __time64_t for _MSC_VER and __MINGW32__
git_time_t = ct.c_int64

# The maximum size of an object
git_object_size_t = ct.c_uint64

# Basic type (loose or packed) of any Git object.
git_object_t = ct.c_int
(   GIT_OBJECT_ANY,        # Object can be any of the following
    GIT_OBJECT_INVALID,    # Object is invalid.
    GIT_OBJECT_COMMIT,     # A commit object.
    GIT_OBJECT_TREE,       # A tree (directory listing) object.
    GIT_OBJECT_BLOB,       # A file revision object.
    GIT_OBJECT_TAG,        # An annotated tag object.
    GIT_OBJECT_OFS_DELTA,  # A delta, base is given by an offset.
    GIT_OBJECT_REF_DELTA,  # A delta, base is given by object id.
) = (-2, -1,  1,  2,  3,  4,  6,  7)

# An open object database handle.
class git_odb(ct.Structure): pass

# A custom backend in an ODB
class git_odb_backend(ct.Structure): pass
#from .sys.odb_backend import git_odb_backend

# An object read from the ODB
class git_odb_object(ct.Structure): pass

# A stream to read/write from the ODB
class git_odb_stream(ct.Structure): pass
#from .odb_backend import git_odb_stream

# A stream to write a packfile to the ODB
# class git_odb_writepack(ct.Structure): pass
from .odb_backend import git_odb_writepack

# a writer for multi-pack-index files.
class git_midx_writer(ct.Structure): pass

# An open refs database handle.
class git_refdb(ct.Structure): pass

# A custom backend for refs
class git_refdb_backend(ct.Structure): pass
# from .sys.refdb_backend import git_refdb_backend

# A git commit-graph
class git_commit_graph(ct.Structure): pass

# a writer for commit-graph files.
class git_commit_graph_writer(ct.Structure): pass

# Representation of an existing git repository,
# including all its object contents
class git_repository(ct.Structure): pass

# Representation of a working tree
class git_worktree(ct.Structure): pass

# Representation of a generic object in a repository
class git_object(ct.Structure): pass

# Representation of an in-progress walk through the commits in a repo
class git_revwalk(ct.Structure): pass

# Parsed representation of a tag object.
class git_tag(ct.Structure): pass

# In-memory representation of a blob object.
class git_blob(ct.Structure): pass

# Parsed representation of a commit object.
class git_commit(ct.Structure): pass

# Representation of each one of the entries in a tree object.
class git_tree_entry(ct.Structure): pass

# Representation of a tree object.
class git_tree(ct.Structure): pass

# Constructor for in-memory trees
class git_treebuilder(ct.Structure): pass

# Memory representation of an index file.
class git_index(ct.Structure): pass

# An iterator for entries in the index.
class git_index_iterator(ct.Structure): pass

# An iterator for conflicts in the index.
class git_index_conflict_iterator(ct.Structure): pass

# Memory representation of a set of config files
class git_config(ct.Structure): pass

# Interface to access a configuration file
class git_config_backend(ct.Structure): pass
# from .sys.config import git_config_backend

# Representation of a reference log entry
class git_reflog_entry(ct.Structure): pass

# Representation of a reference log
class git_reflog(ct.Structure): pass

# Representation of a git note
class git_note(ct.Structure): pass

# Representation of a git packbuilder
class git_packbuilder(ct.Structure): pass

# Time in a signature
class git_time(ct.Structure):
    _fields_ = [
    ("time",   git_time_t),  # time in seconds from epoch
    ("offset", ct.c_int),    # timezone offset, in minutes
    ("sign",   ct.c_byte),   # indicator for questionable '-0000' offsets in signature
]

# An action signature (e.g. for committers, taggers, etc)
class git_signature(ct.Structure):
    _fields_ = [
    ("name",  ct.c_char_p),  # full name of the author
    ("email", ct.c_char_p),  # email of the author
    ("when",  git_time),     # time when the action happened
]

# In-memory representation of a reference.
class git_reference(ct.Structure): pass

# Iterator for references
# class git_reference_iterator(ct.Structure): pass
from .sys.refdb_backend import git_reference_iterator

# Transactional interface to references
class git_transaction(ct.Structure): pass

# Annotated commits, the input to merge and rebase.
class git_annotated_commit(ct.Structure): pass

# Representation of a status collection
class git_status_list(ct.Structure): pass

# Representation of a rebase
class git_rebase(ct.Structure): pass

# Basic type of any Git reference.
git_reference_t = ct.c_int
(   GIT_REFERENCE_INVALID,   # Invalid reference
    GIT_REFERENCE_DIRECT,    # A reference that points at an object id
    GIT_REFERENCE_SYMBOLIC,  # A reference that points at another reference
    GIT_REFERENCE_ALL,
) = (
    0,
    1,
    2,
    1 | 2,  # GIT_REFERENCE_DIRECT | GIT_REFERENCE_SYMBOLIC
)

# Basic type of any Git branch.
git_branch_t = ct.c_int
(   GIT_BRANCH_LOCAL,
    GIT_BRANCH_REMOTE,
    GIT_BRANCH_ALL,
) = (
    1,
    2,
    1 | 2,  # GIT_BRANCH_LOCAL | GIT_BRANCH_REMOTE
)

# Valid modes for index and tree entries.
git_filemode_t = ct.c_int
(   GIT_FILEMODE_UNREADABLE,
    GIT_FILEMODE_TREE,
    GIT_FILEMODE_BLOB,
    GIT_FILEMODE_BLOB_EXECUTABLE,
    GIT_FILEMODE_LINK,
    GIT_FILEMODE_COMMIT,
) = (0o000000, 0o040000, 0o100644,
     0o100755, 0o120000, 0o160000)

# A refspec specifies the mapping between remote and local reference
# names when fetch or pushing.
class git_refspec(ct.Structure): pass

# Git's idea of a remote repository. A remote can be anonymous (in
# which case it does not have backing configuration entries).
class git_remote(ct.Structure): pass

# Interface which represents a transport to communicate with a
# remote.
class git_transport(ct.Structure): pass

# Preparation for a push operation. Can be used to configure what to
# push and the level of parallelism of the packfile builder.
class git_push(ct.Structure): pass

# documentation in the definition
class git_remote_head(ct.Structure): pass
#from .net import git_remote_head

class git_remote_callbacks(ct.Structure): pass
#from .remote import git_remote_callbacks

# Parent type for `git_cert_hostkey` and `git_cert_x509`.
class git_cert(ct.Structure): pass
#from .cert import git_cert

# Opaque structure representing a submodule.
class git_submodule(ct.Structure): pass

# Submodule update values
#
# These values represent settings for the `submodule.$name.update`
# configuration value which says how to handle `git submodule update` for
# this submodule.  The value is usually set in the ".gitmodules" file and
# copied to ".git/config" when the submodule is initialized.
#
# You can override this setting on a per-submodule basis with
# `git_submodule_set_update()` and write the changed value to disk using
# `git_submodule_save()`.  If you have overwritten the value, you can
# revert it by passing `GIT_SUBMODULE_UPDATE_RESET` to the set function.
#
# The values are:
#
# - GIT_SUBMODULE_UPDATE_CHECKOUT: the default; when a submodule is
#   updated, checkout the new detached HEAD to the submodule directory.
# - GIT_SUBMODULE_UPDATE_REBASE: update by rebasing the current checked
#   out branch onto the commit from the superproject.
# - GIT_SUBMODULE_UPDATE_MERGE: update by merging the commit in the
#   superproject into the current checkout out branch of the submodule.
# - GIT_SUBMODULE_UPDATE_NONE: do not update this submodule even when
#   the commit in the superproject is updated.
# - GIT_SUBMODULE_UPDATE_DEFAULT: not used except as static initializer
#   when we don't want any particular update rule to be specified.
#
git_submodule_update_t = ct.c_int
(   GIT_SUBMODULE_UPDATE_CHECKOUT,
    GIT_SUBMODULE_UPDATE_REBASE,
    GIT_SUBMODULE_UPDATE_MERGE,
    GIT_SUBMODULE_UPDATE_NONE,
    GIT_SUBMODULE_UPDATE_DEFAULT,
) = (1, 2, 3, 4, 0)

# Submodule ignore values
#
# These values represent settings for the `submodule.$name.ignore`
# configuration value which says how deeply to look at the working
# directory when getting submodule status.
#
# You can override this value in memory on a per-submodule basis with
# `git_submodule_set_ignore()` and can write the changed value to disk
# with `git_submodule_save()`.  If you have overwritten the value, you
# can revert to the on disk value by using `GIT_SUBMODULE_IGNORE_RESET`.
#
# The values are:
#
# - GIT_SUBMODULE_IGNORE_UNSPECIFIED: use the submodule's configuration
# - GIT_SUBMODULE_IGNORE_NONE: don't ignore any change - i.e. even an
#   untracked file, will mark the submodule as dirty.  Ignored files are
#   still ignored, of course.
# - GIT_SUBMODULE_IGNORE_UNTRACKED: ignore untracked files; only changes
#   to tracked files, or the index or the HEAD commit will matter.
# - GIT_SUBMODULE_IGNORE_DIRTY: ignore changes in the working directory,
#   only considering changes if the HEAD of submodule has moved from the
#   value in the superproject.
# - GIT_SUBMODULE_IGNORE_ALL: never check if the submodule is dirty
# - GIT_SUBMODULE_IGNORE_DEFAULT: not used except as static initializer
#   when we don't want any particular ignore rule to be specified.
#
git_submodule_ignore_t = ct.c_int
(   GIT_SUBMODULE_IGNORE_UNSPECIFIED,  # use the submodule's configuration
    GIT_SUBMODULE_IGNORE_NONE,         # any change or untracked == dirty
    GIT_SUBMODULE_IGNORE_UNTRACKED,    # dirty if tracked files change
    GIT_SUBMODULE_IGNORE_DIRTY,        # only dirty if HEAD moved
    GIT_SUBMODULE_IGNORE_ALL,          # never dirty
) = (-1, 1, 2, 3, 4)

# Options for submodule recurse.
#
# Represent the value of `submodule.$name.fetchRecurseSubmodules`
#
# * GIT_SUBMODULE_RECURSE_NO       - do no recurse into submodules
# * GIT_SUBMODULE_RECURSE_YES      - recurse into submodules
# * GIT_SUBMODULE_RECURSE_ONDEMAND - recurse into submodules only when
#                                    commit not already in local clone
git_submodule_recurse_t = ct.c_int
(   GIT_SUBMODULE_RECURSE_NO,
    GIT_SUBMODULE_RECURSE_YES,
    GIT_SUBMODULE_RECURSE_ONDEMAND,
) = (0, 1, 2)

# A type to write in a streaming fashion, for example, for filters.
class git_writestream(ct.Structure): pass
git_writestream._fields_ = [
    ("write", GIT_CALLBACK(ct.c_int,
                  ct.POINTER(git_writestream),    # stream
                  git_buffer_t,                   # buffer
                  ct.c_size_t)),                  # len
    ("close", GIT_CALLBACK(ct.c_int,
                  ct.POINTER(git_writestream))),  # stream
    ("free",  GIT_CALLBACK(None,
                  ct.POINTER(git_writestream))),  # stream
]

# Representation of .mailmap file state.
class git_mailmap(ct.Structure): pass

# GIT_END_DECL
