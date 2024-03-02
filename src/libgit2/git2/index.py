# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common   import *  # noqa
from .oid      import git_oid_t
from .oid      import git_oid
from .strarray import git_strarray
from .types    import git_repository
from .types    import git_tree
from .types    import git_index
from .types    import git_index_iterator
from .types    import git_index_conflict_iterator

# @file git2/index.h
# @brief Git index parsing and manipulation routines
# @defgroup git_index Git index parsing and manipulation routines
# @ingroup Git

# GIT_BEGIN_DECL

# Time structure used in a git index entry
class git_index_time(ct.Structure):
    _fields_ = [
    ("seconds",     ct.c_int32),
    # nsec should not be stored as time_t compatible
    ("nanoseconds", ct.c_uint32),
]

# In-memory representation of a file entry in the index.
#
# This is a public structure that represents a file entry in the index.
# The meaning of the fields corresponds to core Git's documentation (in
# "Documentation/technical/index-format.txt").
#
# The `flags` field consists of a number of bit fields which can be
# accessed via the first set of `GIT_INDEX_ENTRY_...` bitmasks below.
# These flags are all read from and persisted to disk.
#
# The `flags_extended` field also has a number of bit fields which can be
# accessed via the later `GIT_INDEX_ENTRY_...` bitmasks below.  Some of
# these flags are read from and written to disk, but some are set aside
# for in-memory only reference.
#
# Note that the time and size fields are truncated to 32 bits. This
# is enough to detect changes, which is enough for the index to
# function as a cache, but it should not be taken as an authoritative
# source for that data.
#
class git_index_entry(ct.Structure):
    _fields_ = [
    ("ctime", git_index_time),
    ("mtime", git_index_time),

    ("dev",  ct.c_uint32),
    ("ino",  ct.c_uint32),
    ("mode", ct.c_uint32),
    ("uid",  ct.c_uint32),
    ("gid",  ct.c_uint32),
    ("file_size", ct.c_uint32),

    ("id",   git_oid),

    ("flags", ct.c_uint16),
    ("flags_extended", ct.c_uint16),

    ("path", ct.c_char_p),
]

# Bitmasks for on-disk fields of `git_index_entry`'s `flags`
#
# These bitmasks match the four fields in the `git_index_entry` `flags`
# value both in memory and on disk.  You can use them to interpret the
# data in the `flags`.
#
GIT_INDEX_ENTRY_NAMEMASK   = 0x0fff
GIT_INDEX_ENTRY_STAGEMASK  = 0x3000
GIT_INDEX_ENTRY_STAGESHIFT = 12

# Flags for index entries
#
git_index_entry_flag_t = ct.c_int
(   GIT_INDEX_ENTRY_EXTENDED,
    GIT_INDEX_ENTRY_VALID,
) = (0x4000, 0x8000)

def GIT_INDEX_ENTRY_STAGE(entry):
    return ((entry.contents.flags & GIT_INDEX_ENTRY_STAGEMASK)
            >> GIT_INDEX_ENTRY_STAGESHIFT)

def GIT_INDEX_ENTRY_STAGE_SET(entry, S):
    entry.contents.flags = ((entry.contents.flags & ~GIT_INDEX_ENTRY_STAGEMASK) |
                    ((S & 0x03) << GIT_INDEX_ENTRY_STAGESHIFT))

# Bitmasks for on-disk fields of `git_index_entry`'s `flags_extended`
#
# In memory, the `flags_extended` fields are divided into two parts: the
# fields that are read from and written to disk, and other fields that
# in-memory only and used by libgit2.  Only the flags in
# `GIT_INDEX_ENTRY_EXTENDED_FLAGS` will get saved on-disk.
#
# Thee first three bitmasks match the three fields in the
# `git_index_entry` `flags_extended` value that belong on disk.  You
# can use them to interpret the data in the `flags_extended`.
#
# The rest of the bitmasks match the other fields in the `git_index_entry`
# `flags_extended` value that are only used in-memory by libgit2.
# You can use them to interpret the data in the `flags_extended`.
#
git_index_entry_extended_flag_t = ct.c_int
(   GIT_INDEX_ENTRY_INTENT_TO_ADD,
    GIT_INDEX_ENTRY_SKIP_WORKTREE,

    GIT_INDEX_ENTRY_EXTENDED_FLAGS,

    GIT_INDEX_ENTRY_UPTODATE,
) = (
    1 << 13,
    1 << 14,
    (1 << 13) | (1 << 14),  # GIT_INDEX_ENTRY_INTENT_TO_ADD |
                            # GIT_INDEX_ENTRY_SKIP_WORKTREE
    1 << 2,
)

# Capabilities of system that affect index actions.
git_index_capability_t = ct.c_int
(   GIT_INDEX_CAPABILITY_IGNORE_CASE,
    GIT_INDEX_CAPABILITY_NO_FILEMODE,
    GIT_INDEX_CAPABILITY_NO_SYMLINKS,
    GIT_INDEX_CAPABILITY_FROM_OWNER,
) = (1, 2, 4, -1)

# Callback for APIs that add/remove/update files matching pathspec
git_index_matched_path_cb = GIT_CALLBACK(ct.c_int,
    ct.c_char_p,  # path
    ct.c_char_p,  # matched_pathspec
    ct.c_void_p)  # payload

# Flags for APIs that add files matching pathspec
git_index_add_option_t = ct.c_int
(   GIT_INDEX_ADD_DEFAULT,
    GIT_INDEX_ADD_FORCE,
    GIT_INDEX_ADD_DISABLE_PATHSPEC_MATCH,
    GIT_INDEX_ADD_CHECK_PATHSPEC,
) = (0, 1 << 0, 1 << 1, 1 << 2)

# Git index stage states
git_index_stage_t = ct.c_int
(
    # Match any index stage.
    #
    # Some index APIs take a stage to match; pass this value to match
    # any entry matching the path regardless of stage.
    #
    GIT_INDEX_STAGE_ANY,

    # A normal staged file in the index.
    GIT_INDEX_STAGE_NORMAL,

    # The ancestor side of a conflict.
    GIT_INDEX_STAGE_ANCESTOR,

    # The "ours" side of a conflict.
    GIT_INDEX_STAGE_OURS,

    # The "theirs" side of a conflict.
    GIT_INDEX_STAGE_THEIRS,

) = (-1, 0, 1, 2, 3)

# Create a new bare Git index object as a memory representation
# of the Git index file in 'index_path', without a repository
# to back it.
#
# Since there is no ODB or working directory behind this index,
# any Index methods which rely on these (e.g. index_add_bypath)
# will fail with the GIT_ERROR error code.
#
# If you need to access the index of an actual repository,
# use the `git_repository_index` wrapper.
#
# The index must be freed once it's no longer in use.
#
# @param out the pointer for the new index
# @param index_path the path to the index file in disk
# @return 0 or an error code
#
if defined("GIT_EXPERIMENTAL_SHA256"):
    git_index_open = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_index)),
        ct.c_char_p,
        git_oid_t)(
        ("git_index_open", dll), (
        (1, "out"),
        (1, "index_path"),
        (1, "oid_type"),))
else:
    git_index_open = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_index)),
        ct.c_char_p)(
        ("git_index_open", dll), (
        (1, "out"),
        (1, "index_path"),))
# endif

# Create an in-memory index object.
#
# This index object cannot be read/written to the filesystem,
# but may be used to perform in-memory index operations.
#
# The index must be freed once it's no longer in use.
#
# @param out the pointer for the new index
# @return 0 or an error code
#
if defined("GIT_EXPERIMENTAL_SHA256"):
    git_index_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_index)),
        git_oid_t)(
        ("git_index_new", dll), (
        (1, "out"),
        (1, "oid_type"),))
else:
    git_index_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_index)))(
        ("git_index_new", dll), (
        (1, "out"),))
# endif

# Free an existing index object.
#
# @param index an existing index object
#
git_index_free = CFUNC(None,
    ct.POINTER(git_index))(
    ("git_index_free", dll), (
    (1, "index"),))

# Get the repository this index relates to
#
# @param index The index
# @return A pointer to the repository
#
git_index_owner = CFUNC(ct.POINTER(git_repository),
    ct.POINTER(git_index))(
    ("git_index_owner", dll), (
    (1, "index"),))

# Read index capabilities flags.
#
# @param index An existing index object
# @return A combination of GIT_INDEX_CAPABILITY values
#
git_index_caps = CFUNC(ct.c_int,
    ct.POINTER(git_index))(
    ("git_index_caps", dll), (
    (1, "index"),))

# Set index capabilities flags.
#
# If you pass `GIT_INDEX_CAPABILITY_FROM_OWNER` for the caps, then
# capabilities will be read from the config of the owner object,
# looking at `core.ignorecase`, `core.filemode`, `core.symlinks`.
#
# @param index An existing index object
# @param caps A combination of GIT_INDEX_CAPABILITY values
# @return 0 on success, -1 on failure
#
git_index_set_caps = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.c_int)(
    ("git_index_set_caps", dll), (
    (1, "index"),
    (1, "caps"),))

# Get index on-disk version.
#
# Valid return values are 2, 3, or 4.  If 3 is returned, an index
# with version 2 may be written instead, if the extension data in
# version 3 is not necessary.
#
# @param index An existing index object
# @return the index version
#
git_index_version = CFUNC(ct.c_uint,
    ct.POINTER(git_index))(
    ("git_index_version", dll), (
    (1, "index"),))

# Set index on-disk version.
#
# Valid values are 2, 3, or 4.  If 2 is given, git_index_write may
# write an index with version 3 instead, if necessary to accurately
# represent the index.
#
# @param index An existing index object
# @param version The new version number
# @return 0 on success, -1 on failure
#
git_index_set_version = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.c_uint)(
    ("git_index_set_version", dll), (
    (1, "index"),
    (1, "version"),))

# Update the contents of an existing index object in memory by reading
# from the hard disk.
#
# If `force` is true, this performs a "hard" read that discards in-memory
# changes and always reloads the on-disk index data.  If there is no
# on-disk version, the index will be cleared.
#
# If `force` is false, this does a "soft" read that reloads the index
# data from disk only if it has changed since the last time it was
# loaded.  Purely in-memory index data will be untouched.  Be aware: if
# there are changes on disk, unwritten in-memory changes are discarded.
#
# @param index an existing index object
# @param force if true, always reload, vs. only read if file has changed
# @return 0 or an error code
#
git_index_read = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.c_int)(
    ("git_index_read", dll), (
    (1, "index"),
    (1, "force"),))

# Write an existing index object from memory back to disk
# using an atomic file lock.
#
# @param index an existing index object
# @return 0 or an error code
#
git_index_write = CFUNC(ct.c_int,
    ct.POINTER(git_index))(
    ("git_index_write", dll), (
    (1, "index"),))

# Get the full path to the index file on disk.
#
# @param index an existing index object
# @return path to index file or NULL for in-memory index
#
git_index_path = CFUNC(ct.c_char_p,
    ct.POINTER(git_index))(
    ("git_index_path", dll), (
    (1, "index"),))

if not defined("GIT_DEPRECATE_HARD"):
    # Get the checksum of the index
    #
    # This checksum is the SHA-1 hash over the index file (except the
    # last 20 bytes which are the checksum itself). In cases where the
    # index does not exist on-disk, it will be zeroed out.
    #
    # @deprecated this function is deprecated with no replacement
    # @param index an existing index object
    # @return a pointer to the checksum of the index
    #
    git_index_checksum = CFUNC(ct.POINTER(git_oid),
        ct.POINTER(git_index))(
        ("git_index_checksum", dll), (
        (1, "index"),))
# endif

# Read a tree into the index file with stats
#
# The current index contents will be replaced by the specified tree.
#
# @param index an existing index object
# @param tree tree to read
# @return 0 or an error code
#
git_index_read_tree = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.POINTER(git_tree))(
    ("git_index_read_tree", dll), (
    (1, "index"),
    (1, "tree"),))

# Write the index as a tree
#
# This method will scan the index and write a representation
# of its current state back to disk; it recursively creates
# tree objects for each of the subtrees stored in the index,
# but only returns the OID of the root tree. This is the OID
# that can be used e.g. to create a commit.
#
# The index instance cannot be bare, and needs to be associated
# to an existing repository.
#
# The index must not contain any file in conflict.
#
# @param out Pointer where to store the OID of the written tree
# @param index Index to write
# @return 0 on success, GIT_EUNMERGED when the index is not clean
# or an error code
#
git_index_write_tree = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_index))(
    ("git_index_write_tree", dll), (
    (1, "out"),
    (1, "index"),))

# Write the index as a tree to the given repository
#
# This method will do the same as `git_index_write_tree`, but
# letting the user choose the repository where the tree will
# be written.
#
# The index must not contain any file in conflict.
#
# @param out Pointer where to store OID of the written tree
# @param index Index to write
# @param repo Repository where to write the tree
# @return 0 on success, GIT_EUNMERGED when the index is not clean
# or an error code
#
git_index_write_tree_to = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_index),
    ct.POINTER(git_repository))(
    ("git_index_write_tree_to", dll), (
    (1, "out"),
    (1, "index"),
    (1, "repo"),))

# @name Raw Index Entry Functions
#
# These functions work on index entries, and allow for raw manipulation
# of the entries.
#

# Index entry manipulation

# Get the count of entries currently in the index
#
# @param index an existing index object
# @return integer of count of current entries
#
git_index_entrycount = CFUNC(ct.c_size_t,
    ct.POINTER(git_index))(
    ("git_index_entrycount", dll), (
    (1, "index"),))

# Clear the contents (all the entries) of an index object.
#
# This clears the index object in memory; changes must be explicitly
# written to disk for them to take effect persistently.
#
# @param index an existing index object
# @return 0 on success, error code < 0 on failure
#
git_index_clear = CFUNC(ct.c_int,
    ct.POINTER(git_index))(
    ("git_index_clear", dll), (
    (1, "index"),))

# Get a pointer to one of the entries in the index
#
# The entry is not modifiable and should not be freed.  Because the
# `git_index_entry` struct is a publicly defined struct, you should
# be able to make your own permanent copy of the data if necessary.
#
# @param index an existing index object
# @param n the position of the entry
# @return a pointer to the entry; NULL if out of bounds
#
git_index_get_byindex = CFUNC(ct.POINTER(git_index_entry),
    ct.POINTER(git_index),
    ct.c_size_t)(
    ("git_index_get_byindex", dll), (
    (1, "index"),
    (1, "n"),))

# Get a pointer to one of the entries in the index
#
# The entry is not modifiable and should not be freed.  Because the
# `git_index_entry` struct is a publicly defined struct, you should
# be able to make your own permanent copy of the data if necessary.
#
# @param index an existing index object
# @param path path to search
# @param stage stage to search
# @return a pointer to the entry; NULL if it was not found
#
git_index_get_bypath = CFUNC(ct.POINTER(git_index_entry),
    ct.POINTER(git_index),
    ct.c_char_p,
    ct.c_int)(
    ("git_index_get_bypath", dll), (
    (1, "index"),
    (1, "path"),
    (1, "stage"),))

# Remove an entry from the index
#
# @param index an existing index object
# @param path path to search
# @param stage stage to search
# @return 0 or an error code
#
git_index_remove = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.c_char_p,
    ct.c_int)(
    ("git_index_remove", dll), (
    (1, "index"),
    (1, "path"),
    (1, "stage"),))

# Remove all entries from the index under a given directory
#
# @param index an existing index object
# @param dir container directory path
# @param stage stage to search
# @return 0 or an error code
#
git_index_remove_directory = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.c_char_p,
    ct.c_int)(
    ("git_index_remove_directory", dll), (
    (1, "index"),
    (1, "dir"),
    (1, "stage"),))

# Add or update an index entry from an in-memory struct
#
# If a previous index entry exists that has the same path and stage
# as the given 'source_entry', it will be replaced.  Otherwise, the
# 'source_entry' will be added.
#
# A full copy (including the 'path' string) of the given
# 'source_entry' will be inserted on the index.
#
# @param index an existing index object
# @param source_entry new entry object
# @return 0 or an error code
#
git_index_add = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.POINTER(git_index_entry))(
    ("git_index_add", dll), (
    (1, "index"),
    (1, "source_entry"),))

# Return the stage number from a git index entry
#
# This entry is calculated from the entry's flag attribute like this:
#
#    (entry->flags & GIT_INDEX_ENTRY_STAGEMASK) >> GIT_INDEX_ENTRY_STAGESHIFT
#
# @param entry The entry
# @return the stage number
#
git_index_entry_stage = CFUNC(ct.c_int,
    ct.POINTER(git_index_entry))(
    ("git_index_entry_stage", dll), (
    (1, "entry"),))

# Return whether the given index entry is a conflict (has a high stage
# entry).  This is simply shorthand for `git_index_entry_stage > 0`.
#
# @param entry The entry
# @return 1 if the entry is a conflict entry, 0 otherwise
#
git_index_entry_is_conflict = CFUNC(ct.c_int,
    ct.POINTER(git_index_entry))(
    ("git_index_entry_is_conflict", dll), (
    (1, "entry"),))

# @name Index Entry Iteration Functions
#
# These functions provide an iterator for index entries.
#

# Create an iterator that will return every entry contained in the
# index at the time of creation.  Entries are returned in order,
# sorted by path.  This iterator is backed by a snapshot that allows
# callers to modify the index while iterating without affecting the
# iterator.
#
# @param iterator_out The newly created iterator
# @param index The index to iterate
# @return 0 or an error code.
#
git_index_iterator_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_index_iterator)),
    ct.POINTER(git_index))(
    ("git_index_iterator_new", dll), (
    (1, "iterator_out"),
    (1, "index"),))

# Return the next index entry in-order from the iterator.
#
# @param out Pointer to store the index entry in
# @param iterator The iterator
# @return 0, GIT_ITEROVER on iteration completion or an error code
#
git_index_iterator_next = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_index_entry)),
    ct.POINTER(git_index_iterator))(
    ("git_index_iterator_next", dll), (
    (1, "out"),
    (1, "iterator"),))

# Free the index iterator
#
# @param iterator The iterator to free
#
git_index_iterator_free = CFUNC(None,
    ct.POINTER(git_index_iterator))(
    ("git_index_iterator_free", dll), (
    (1, "iterator"),))

# @name Workdir Index Entry Functions
#
# These functions work on index entries specifically in the working
# directory (ie, stage 0).
#

# Add or update an index entry from a file on disk
#
# The file `path` must be relative to the repository's
# working folder and must be readable.
#
# This method will fail in bare index instances.
#
# This forces the file to be added to the index, not looking
# at gitignore rules.  Those rules can be evaluated through
# the git_status APIs (in status.h) before calling this.
#
# If this file currently is the result of a merge conflict, this
# file will no longer be marked as conflicting.  The data about
# the conflict will be moved to the "resolve undo" (REUC) section.
#
# @param index an existing index object
# @param path filename to add
# @return 0 or an error code
#
git_index_add_bypath = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.c_char_p)(
    ("git_index_add_bypath", dll), (
    (1, "index"),
    (1, "path"),))

# Add or update an index entry from a buffer in memory
#
# This method will create a blob in the repository that owns the
# index and then add the index entry to the index.  The `path` of the
# entry represents the position of the blob relative to the
# repository's root folder.
#
# If a previous index entry exists that has the same path as the
# given 'entry', it will be replaced.  Otherwise, the 'entry' will be
# added.
#
# This forces the file to be added to the index, not looking
# at gitignore rules.  Those rules can be evaluated through
# the git_status APIs (in status.h) before calling this.
#
# If this file currently is the result of a merge conflict, this
# file will no longer be marked as conflicting.  The data about
# the conflict will be moved to the "resolve undo" (REUC) section.
#
# @param index an existing index object
# @param entry filename to add
# @param buffer data to be written into the blob
# @param len length of the data
# @return 0 or an error code
#
git_index_add_from_buffer = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.POINTER(git_index_entry),
    ct.c_void_p,
    ct.c_size_t)(
    ("git_index_add_from_buffer", dll), (
    (1, "index"),
    (1, "entry"),
    (1, "buffer"),
    (1, "len"),))

# Remove an index entry corresponding to a file on disk
#
# The file `path` must be relative to the repository's
# working folder.  It may exist.
#
# If this file currently is the result of a merge conflict, this
# file will no longer be marked as conflicting.  The data about
# the conflict will be moved to the "resolve undo" (REUC) section.
#
# @param index an existing index object
# @param path filename to remove
# @return 0 or an error code
#
git_index_remove_bypath = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.c_char_p)(
    ("git_index_remove_bypath", dll), (
    (1, "index"),
    (1, "path"),))

# Add or update index entries matching files in the working directory.
#
# This method will fail in bare index instances.
#
# The `pathspec` is a list of file names or shell glob patterns that will
# be matched against files in the repository's working directory.  Each
# file that matches will be added to the index (either updating an
# existing entry or adding a new entry).  You can disable glob expansion
# and force exact matching with the `GIT_INDEX_ADD_DISABLE_PATHSPEC_MATCH`
# flag.
#
# Files that are ignored will be skipped (unlike `git_index_add_bypath`).
# If a file is already tracked in the index, then it#will* be updated
# even if it is ignored.  Pass the `GIT_INDEX_ADD_FORCE` flag to skip
# the checking of ignore rules.
#
# To emulate `git add -A` and generate an error if the pathspec contains
# the exact path of an ignored file (when not using FORCE), add the
# `GIT_INDEX_ADD_CHECK_PATHSPEC` flag.  This checks that each entry
# in the `pathspec` that is an exact match to a filename on disk is
# either not ignored or already in the index.  If this check fails, the
# function will return GIT_EINVALIDSPEC.
#
# To emulate `git add -A` with the "dry-run" option, just use a callback
# function that always returns a positive value.  See below for details.
#
# If any files are currently the result of a merge conflict, those files
# will no longer be marked as conflicting.  The data about the conflicts
# will be moved to the "resolve undo" (REUC) section.
#
# If you provide a callback function, it will be invoked on each matching
# item in the working directory immediately#before* it is added to /
# updated in the index.  Returning zero will add the item to the index,
# greater than zero will skip the item, and less than zero will abort the
# scan and return that value to the caller.
#
# @param index an existing index object
# @param pathspec array of path patterns
# @param flags combination of git_index_add_option_t flags
# @param callback notification callback for each added/updated path (also
#                 gets index of matching pathspec entry); can be NULL;
#                 return 0 to add, >0 to skip, <0 to abort scan.
# @param payload payload passed through to callback function
# @return 0 on success, negative callback return value, or error code
#
git_index_add_all = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.POINTER(git_strarray),
    ct.c_uint,
    git_index_matched_path_cb,
    ct.c_void_p)(
    ("git_index_add_all", dll), (
    (1, "index"),
    (1, "pathspec"),
    (1, "flags"),
    (1, "callback"),
    (1, "payload"),))

# Remove all matching index entries.
#
# If you provide a callback function, it will be invoked on each matching
# item in the index immediately#before* it is removed.  Return 0 to
# remove the item, > 0 to skip the item, and < 0 to abort the scan.
#
# @param index An existing index object
# @param pathspec array of path patterns
# @param callback notification callback for each removed path (also
#                 gets index of matching pathspec entry); can be NULL;
#                 return 0 to add, >0 to skip, <0 to abort scan.
# @param payload payload passed through to callback function
# @return 0 on success, negative callback return value, or error code
#
git_index_remove_all = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.POINTER(git_strarray),
    git_index_matched_path_cb,
    ct.c_void_p)(
    ("git_index_remove_all", dll), (
    (1, "index"),
    (1, "pathspec"),
    (1, "callback"),
    (1, "payload"),))

# Update all index entries to match the working directory
#
# This method will fail in bare index instances.
#
# This scans the existing index entries and synchronizes them with the
# working directory, deleting them if the corresponding working directory
# file no longer exists otherwise updating the information (including
# adding the latest version of file to the ODB if needed).
#
# If you provide a callback function, it will be invoked on each matching
# item in the index immediately#before* it is updated (either refreshed
# or removed depending on working directory state).  Return 0 to proceed
# with updating the item, > 0 to skip the item, and < 0 to abort the scan.
#
# @param index An existing index object
# @param pathspec array of path patterns
# @param callback notification callback for each updated path (also
#                 gets index of matching pathspec entry); can be NULL;
#                 return 0 to add, >0 to skip, <0 to abort scan.
# @param payload payload passed through to callback function
# @return 0 on success, negative callback return value, or error code
#
git_index_update_all = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.POINTER(git_strarray),
    git_index_matched_path_cb,
    ct.c_void_p)(
    ("git_index_update_all", dll), (
    (1, "index"),
    (1, "pathspec"),
    (1, "callback"),
    (1, "payload"),))

# Find the first position of any entries which point to given
# path in the Git index.
#
# @param at_pos the address to which the position of the index entry is written (optional)
# @param index an existing index object
# @param path path to search
# @return 0 or an error code
#
git_index_find = CFUNC(ct.c_int,
    ct.POINTER(ct.c_size_t),
    ct.POINTER(git_index),
    ct.c_char_p)(
    ("git_index_find", dll), (
    (1, "at_pos"),
    (1, "index"),
    (1, "path"),))

# Find the first position of any entries matching a prefix. To find the first position
# of a path inside a given folder, suffix the prefix with a '/'.
#
# @param at_pos the address to which the position of the index entry is written (optional)
# @param index an existing index object
# @param prefix the prefix to search for
# @return 0 or an error code
#
git_index_find_prefix = CFUNC(ct.c_int,
    ct.POINTER(ct.c_size_t),
    ct.POINTER(git_index),
    ct.c_char_p)(
    ("git_index_find_prefix", dll), (
    (1, "at_pos"),
    (1, "index"),
    (1, "prefix"),))

# @name Conflict Index Entry Functions
#
# These functions work on conflict index entries specifically (ie, stages 1-3)
#

# Add or update index entries to represent a conflict.  Any staged
# entries that exist at the given paths will be removed.
#
# The entries are the entries from the tree included in the merge.  Any
# entry may be null to indicate that that file was not present in the
# trees during the merge.  For example, ancestor_entry may be NULL to
# indicate that a file was added in both branches and must be resolved.
#
# @param index an existing index object
# @param ancestor_entry the entry data for the ancestor of the conflict
# @param our_entry the entry data for our side of the merge conflict
# @param their_entry the entry data for their side of the merge conflict
# @return 0 or an error code
#
git_index_conflict_add = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.POINTER(git_index_entry),
    ct.POINTER(git_index_entry),
    ct.POINTER(git_index_entry))(
    ("git_index_conflict_add", dll), (
    (1, "index"),
    (1, "ancestor_entry"),
    (1, "our_entry"),
    (1, "their_entry"),))

# Get the index entries that represent a conflict of a single file.
#
# The entries are not modifiable and should not be freed.  Because the
# `git_index_entry` struct is a publicly defined struct, you should
# be able to make your own permanent copy of the data if necessary.
#
# @param ancestor_out Pointer to store the ancestor entry
# @param our_out Pointer to store the our entry
# @param their_out Pointer to store the their entry
# @param index an existing index object
# @param path path to search
# @return 0 or an error code
#
git_index_conflict_get = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_index_entry)),
    ct.POINTER(ct.POINTER(git_index_entry)),
    ct.POINTER(ct.POINTER(git_index_entry)),
    ct.POINTER(git_index),
    ct.c_char_p)(
    ("git_index_conflict_get", dll), (
    (1, "ancestor_out"),
    (1, "our_out"),
    (1, "their_out"),
    (1, "index"),
    (1, "path"),))

# Removes the index entries that represent a conflict of a single file.
#
# @param index an existing index object
# @param path path to remove conflicts for
# @return 0 or an error code
#
git_index_conflict_remove = CFUNC(ct.c_int,
    ct.POINTER(git_index),
    ct.c_char_p)(
    ("git_index_conflict_remove", dll), (
    (1, "index"),
    (1, "path"),))

# Remove all conflicts in the index (entries with a stage greater than 0).
#
# @param index an existing index object
# @return 0 or an error code
#
git_index_conflict_cleanup = CFUNC(ct.c_int,
    ct.POINTER(git_index))(
    ("git_index_conflict_cleanup", dll), (
    (1, "index"),))

# Determine if the index contains entries representing file conflicts.
#
# @param index An existing index object.
# @return 1 if at least one conflict is found, 0 otherwise.
#
git_index_has_conflicts = CFUNC(ct.c_int,
    ct.POINTER(git_index))(
    ("git_index_has_conflicts", dll), (
    (1, "index"),))

# Create an iterator for the conflicts in the index.
#
# The index must not be modified while iterating; the results are undefined.
#
# @param iterator_out The newly created conflict iterator
# @param index The index to scan
# @return 0 or an error code
#
git_index_conflict_iterator_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_index_conflict_iterator)),
    ct.POINTER(git_index))(
    ("git_index_conflict_iterator_new", dll), (
    (1, "iterator_out"),
    (1, "index"),))

# Returns the current conflict (ancestor, ours and theirs entry) and
# advance the iterator internally to the next value.
#
# @param ancestor_out Pointer to store the ancestor side of the conflict
# @param our_out Pointer to store our side of the conflict
# @param their_out Pointer to store their side of the conflict
# @param iterator The conflict iterator.
# @return 0 (no error), GIT_ITEROVER (iteration is done) or an error code
#         (negative value)
#
git_index_conflict_next = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_index_entry)),
    ct.POINTER(ct.POINTER(git_index_entry)),
    ct.POINTER(ct.POINTER(git_index_entry)),
    ct.POINTER(git_index_conflict_iterator))(
    ("git_index_conflict_next", dll), (
    (1, "ancestor_out"),
    (1, "our_out"),
    (1, "their_out"),
    (1, "iterator"),))

# Frees a `git_index_conflict_iterator`.
#
# @param iterator pointer to the iterator
#
git_index_conflict_iterator_free = CFUNC(None,
    ct.POINTER(git_index_conflict_iterator))(
    ("git_index_conflict_iterator_free", dll), (
    (1, "iterator"),))

# GIT_END_DECL
