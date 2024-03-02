# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .oid    import git_oid
from .types  import git_signature
from .types  import git_repository

# @file git2/blame.h
# @brief Git blame routines
# @defgroup git_blame Git blame routines
# @ingroup Git

# GIT_BEGIN_DECL

# Flags for indicating option behavior for git_blame APIs.
#
git_blame_flag_t = ct.c_int
(
    # Normal blame, the default
    GIT_BLAME_NORMAL,

    # Track lines that have moved within a file (like `git blame -M`).
    #
    # This is not yet implemented and reserved for future use.
    #
    GIT_BLAME_TRACK_COPIES_SAME_FILE,

    # Track lines that have moved across files in the same commit
    # (like `git blame -C`).
    #
    # This is not yet implemented and reserved for future use.
    #
    GIT_BLAME_TRACK_COPIES_SAME_COMMIT_MOVES,

    # Track lines that have been copied from another file that exists
    # in the same commit (like `git blame -CC`).  Implies SAME_FILE.
    #
    # This is not yet implemented and reserved for future use.
    #
    GIT_BLAME_TRACK_COPIES_SAME_COMMIT_COPIES,

    # Track lines that have been copied from another file that exists in
    # *any* commit (like `git blame -CCC`).  Implies SAME_COMMIT_COPIES.
    #
    # This is not yet implemented and reserved for future use.
    #
    GIT_BLAME_TRACK_COPIES_ANY_COMMIT_COPIES,

    # Restrict the search of commits to those reachable following only
    # the first parents.
    #
    GIT_BLAME_FIRST_PARENT,

    # Use mailmap file to map author and committer names and email
    # addresses to canonical real names and email addresses. The
    # mailmap will be read from the working directory, or HEAD in a
    # bare repository.
    #
    GIT_BLAME_USE_MAILMAP,

    # Ignore whitespace differences
    GIT_BLAME_IGNORE_WHITESPACE,

) = (0, 1 << 0, 1 << 1, 1 << 2, 1 << 3, 1 << 4, 1 << 5, 1 << 6)

# Blame options structure
#
# Initialize with `GIT_BLAME_OPTIONS_INIT`. Alternatively, you can
# use `git_blame_options_init`.
#
#
class git_blame_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # A combination of `git_blame_flag_t`
    #
    ("flags", ct.c_uint32),

    # The lower bound on the number of alphanumeric characters that
    # must be detected as moving/copying within a file for it to
    # associate those lines with the parent commit. The default value
    # is 20.
    #
    # This value only takes effect if any of the `GIT_BLAME_TRACK_COPIES_*`
    # flags are specified.
    #
    ("min_match_characters", ct.c_uint16),

    # The id of the newest commit to consider. The default is HEAD.
    #
    ("newest_commit", git_oid),

    # The id of the oldest commit to consider.
    # The default is the first commit encountered with a NULL parent.
    #
    ("oldest_commit", git_oid),

    # The first line in the file to blame.
    # The default is 1 (line numbers start with 1).
    #
    ("min_line", ct.c_size_t),

    # The last line in the file to blame.
    # The default is the last line of the file.
    #
    ("max_line", ct.c_size_t),
]

GIT_BLAME_OPTIONS_VERSION = 1
#define GIT_BLAME_OPTIONS_INIT = { GIT_BLAME_OPTIONS_VERSION }

# Initialize git_blame_options structure
#
# Initializes a `git_blame_options` with default values. Equivalent to creating
# an instance with GIT_BLAME_OPTIONS_INIT.
#
# @param opts The `git_blame_options` struct to initialize.
# @param version The struct version; pass `GIT_BLAME_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_blame_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_blame_options),
    ct.c_uint)(
    ("git_blame_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Structure that represents a blame hunk.
#
class git_blame_hunk(ct.Structure):
    _fields_ = [

    # The number of lines in this hunk.
    #
    ("lines_in_hunk", ct.c_size_t),

    # The OID of the commit where this line was last changed.
    #
    ("final_commit_id", git_oid),

    # The 1-based line number where this hunk begins, in the final version
    # of the file.
    #
    ("final_start_line_number", ct.c_size_t),

    # The author of `final_commit_id`. If `GIT_BLAME_USE_MAILMAP` has been
    # specified, it will contain the canonical real name and email address.
    #
    ("final_signature", ct.POINTER(git_signature)),

    # The OID of the commit where this hunk was found.
    # This will usually be the same as `final_commit_id`, except when
    # `GIT_BLAME_TRACK_COPIES_ANY_COMMIT_COPIES` has been specified.
    #
    ("orig_commit_id", git_oid),

    # The path to the file where this hunk originated, as of the commit
    # specified by `orig_commit_id`.
    #
    ("orig_path", ct.c_char_p),

    # The 1-based line number where this hunk begins in the file named by
    # `orig_path` in the commit specified by `orig_commit_id`.
    #
    ("orig_start_line_number", ct.c_size_t),

    # The author of `orig_commit_id`. If `GIT_BLAME_USE_MAILMAP` has been
    # specified, it will contain the canonical real name and email address.
    #
    ("orig_signature", ct.POINTER(git_signature)),

    # The 1 iff the hunk has been tracked to a boundary commit (the root,
    # or the commit specified in git_blame_options.oldest_commit)
    #
    ("boundary", ct.c_byte),
]

# Opaque structure to hold blame results
class git_blame(ct.Structure): pass

# Gets the number of hunks that exist in the blame structure.
#
# @param blame The blame structure to query.
# @return The number of hunks.
#
git_blame_get_hunk_count = CFUNC(ct.c_uint32,
    ct.POINTER(git_blame))(
    ("git_blame_get_hunk_count", dll), (
    (1, "blame"),))

# Gets the blame hunk at the given index.
#
# @param blame the blame structure to query
# @param index index of the hunk to retrieve
# @return the hunk at the given index, or NULL on error
#
git_blame_get_hunk_byindex = CFUNC(ct.POINTER(git_blame_hunk),
    ct.POINTER(git_blame),
    ct.c_uint32)(
    ("git_blame_get_hunk_byindex", dll), (
    (1, "blame"),
    (1, "index"),))

# Gets the hunk that relates to the given line number in the newest commit.
#
# @param blame the blame structure to query
# @param lineno the (1-based) line number to find a hunk for
# @return the hunk that contains the given line, or NULL on error
#
git_blame_get_hunk_byline = CFUNC(ct.POINTER(git_blame_hunk),
    ct.POINTER(git_blame),
    ct.c_size_t)(
    ("git_blame_get_hunk_byline", dll), (
    (1, "blame"),
    (1, "lineno"),))

# Get the blame for a single file.
#
# @param out pointer that will receive the blame object
# @param repo repository whose history is to be walked
# @param path path to file to consider
# @param options options for the blame operation.  If NULL, this is treated as
#                though GIT_BLAME_OPTIONS_INIT were passed.
# @return 0 on success, or an error code. (use git_error_last for information
#         about the error.)
#
git_blame_file = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_blame)),
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.POINTER(git_blame_options))(
    ("git_blame_file", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "path"),
    (1, "options"),))

# Get blame data for a file that has been modified in memory. The `reference`
# parameter is a pre-calculated blame for the in-odb history of the file. This
# means that once a file blame is completed (which can be expensive), updating
# the buffer blame is very fast.
#
# Lines that differ between the buffer and the committed version are marked as
# having a zero OID for their final_commit_id.
#
# @param out pointer that will receive the resulting blame data
# @param reference cached blame from the history of the file (usually the output
#                  from git_blame_file)
# @param buffer the (possibly) modified contents of the file
# @param buffer_len number of valid bytes in the buffer
# @return 0 on success, or an error code. (use git_error_last for information
#         about the error)
#
git_blame_buffer = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_blame)),
    ct.POINTER(git_blame),
    git_buffer_t,
    ct.c_size_t)(
    ("git_blame_buffer", dll), (
    (1, "out"),
    (1, "reference"),
    (1, "buffer"),
    (1, "buffer_len"),))

# Free memory allocated by git_blame_file or git_blame_buffer.
#
# @param blame the blame structure to free
#
git_blame_free = CFUNC(None,
    ct.POINTER(git_blame))(
    ("git_blame_free", dll), (
    (1, "blame"),))

# GIT_END_DECL
