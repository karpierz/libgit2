# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common   import *  # noqa
from .strarray import git_strarray
from .types    import git_repository
from .diff     import git_diff
from .diff     import git_diff_delta
from .types    import git_index
from .types    import git_tree

# GIT_BEGIN_DECL

# Compiled pathspec
#
class git_pathspec(ct.Structure): pass

# List of filenames matching a pathspec
#
class git_pathspec_match_list(ct.Structure): pass

# Options controlling how pathspec match should be executed
#
git_pathspec_flag_t = ct.c_int
(
    GIT_PATHSPEC_DEFAULT,

    # GIT_PATHSPEC_IGNORE_CASE forces match to ignore case; otherwise
    # match will use native case sensitivity of platform filesystem
    #
    GIT_PATHSPEC_IGNORE_CASE,

    # GIT_PATHSPEC_USE_CASE forces case sensitive match; otherwise
    # match will use native case sensitivity of platform filesystem
    #
    GIT_PATHSPEC_USE_CASE,

    # GIT_PATHSPEC_NO_GLOB disables glob patterns and just uses simple
    # string comparison for matching
    #
    GIT_PATHSPEC_NO_GLOB,

    # GIT_PATHSPEC_NO_MATCH_ERROR means the match functions return error
    # code GIT_ENOTFOUND if no matches are found; otherwise no matches is
    # still success (return 0) but `git_pathspec_match_list_entrycount`
    # will indicate 0 matches.
    #
    GIT_PATHSPEC_NO_MATCH_ERROR,

    # GIT_PATHSPEC_FIND_FAILURES means that the `git_pathspec_match_list`
    # should track which patterns matched which files so that at the end of
    # the match we can identify patterns that did not match any files.
    #
    GIT_PATHSPEC_FIND_FAILURES,

    # GIT_PATHSPEC_FAILURES_ONLY means that the `git_pathspec_match_list`
    # does not need to keep the actual matching filenames.  Use this to
    # just test if there were any matches at all or in combination with
    # GIT_PATHSPEC_FIND_FAILURES to validate a pathspec.
    #
    GIT_PATHSPEC_FAILURES_ONLY,

) = (0, 1 << 0, 1 << 1, 1 << 2, 1 << 3, 1 << 4, 1 << 5)

# Compile a pathspec
#
# @param out Output of the compiled pathspec
# @param pathspec A git_strarray of the paths to match
# @return 0 on success, <0 on failure
#
git_pathspec_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_pathspec)),
    ct.POINTER(git_strarray))(
    ("git_pathspec_new", dll), (
    (1, "out"),
    (1, "pathspec"),))

# Free a pathspec
#
# @param ps The compiled pathspec
#
git_pathspec_free = CFUNC(None,
    ct.POINTER(git_pathspec))(
    ("git_pathspec_free", dll), (
    (1, "ps"),))

# Try to match a path against a pathspec
#
# Unlike most of the other pathspec matching functions, this will not
# fall back on the native case-sensitivity for your platform.  You must
# explicitly pass flags to control case sensitivity or else this will
# fall back on being case sensitive.
#
# @param ps The compiled pathspec
# @param flags Combination of git_pathspec_flag_t options to control match
# @param path The pathname to attempt to match
# @return 1 is path matches spec, 0 if it does not
#
git_pathspec_matches_path = CFUNC(ct.c_int,
    ct.POINTER(git_pathspec),
    ct.c_uint32,
    ct.c_char_p)(
    ("git_pathspec_matches_path", dll), (
    (1, "ps"),
    (1, "flags"),
    (1, "path"),))

# Match a pathspec against the working directory of a repository.
#
# This matches the pathspec against the current files in the working
# directory of the repository.  It is an error to invoke this on a bare
# repo.  This handles git ignores (i.e. ignored files will not be
# considered to match the `pathspec` unless the file is tracked in the
# index).
#
# If `out` is not NULL, this returns a `git_patchspec_match_list`.  That
# contains the list of all matched filenames (unless you pass the
# `GIT_PATHSPEC_FAILURES_ONLY` flag) and may also contain the list of
# pathspecs with no match (if you used the `GIT_PATHSPEC_FIND_FAILURES`
# flag).  You must call `git_pathspec_match_list_free()` on this object.
#
# @param out Output list of matches; pass NULL to just get return value
# @param repo The repository in which to match; bare repo is an error
# @param flags Combination of git_pathspec_flag_t options to control match
# @param ps Pathspec to be matched
# @return 0 on success, -1 on error, GIT_ENOTFOUND if no matches and
#         the GIT_PATHSPEC_NO_MATCH_ERROR flag was given
#
git_pathspec_match_workdir = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_pathspec_match_list)),
    ct.POINTER(git_repository),
    ct.c_uint32,
    ct.POINTER(git_pathspec))(
    ("git_pathspec_match_workdir", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "flags"),
    (1, "ps"),))

# Match a pathspec against entries in an index.
#
# This matches the pathspec against the files in the repository index.
#
# NOTE: At the moment, the case sensitivity of this match is controlled
# by the current case-sensitivity of the index object itself and the
# USE_CASE and IGNORE_CASE flags will have no effect.  This behavior will
# be corrected in a future release.
#
# If `out` is not NULL, this returns a `git_patchspec_match_list`.  That
# contains the list of all matched filenames (unless you pass the
# `GIT_PATHSPEC_FAILURES_ONLY` flag) and may also contain the list of
# pathspecs with no match (if you used the `GIT_PATHSPEC_FIND_FAILURES`
# flag).  You must call `git_pathspec_match_list_free()` on this object.
#
# @param out Output list of matches; pass NULL to just get return value
# @param index The index to match against
# @param flags Combination of git_pathspec_flag_t options to control match
# @param ps Pathspec to be matched
# @return 0 on success, -1 on error, GIT_ENOTFOUND if no matches and
#         the GIT_PATHSPEC_NO_MATCH_ERROR flag is used
#
git_pathspec_match_index = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_pathspec_match_list)),
    ct.POINTER(git_index),
    ct.c_uint32,
    ct.POINTER(git_pathspec))(
    ("git_pathspec_match_index", dll), (
    (1, "out"),
    (1, "index"),
    (1, "flags"),
    (1, "ps"),))

# Match a pathspec against files in a tree.
#
# This matches the pathspec against the files in the given tree.
#
# If `out` is not NULL, this returns a `git_patchspec_match_list`.  That
# contains the list of all matched filenames (unless you pass the
# `GIT_PATHSPEC_FAILURES_ONLY` flag) and may also contain the list of
# pathspecs with no match (if you used the `GIT_PATHSPEC_FIND_FAILURES`
# flag).  You must call `git_pathspec_match_list_free()` on this object.
#
# @param out Output list of matches; pass NULL to just get return value
# @param tree The root-level tree to match against
# @param flags Combination of git_pathspec_flag_t options to control match
# @param ps Pathspec to be matched
# @return 0 on success, -1 on error, GIT_ENOTFOUND if no matches and
#         the GIT_PATHSPEC_NO_MATCH_ERROR flag is used
#
git_pathspec_match_tree = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_pathspec_match_list)),
    ct.POINTER(git_tree),
    ct.c_uint32,
    ct.POINTER(git_pathspec))(
    ("git_pathspec_match_tree", dll), (
    (1, "out"),
    (1, "tree"),
    (1, "flags"),
    (1, "ps"),))

# Match a pathspec against files in a diff list.
#
# This matches the pathspec against the files in the given diff list.
#
# If `out` is not NULL, this returns a `git_patchspec_match_list`.  That
# contains the list of all matched filenames (unless you pass the
# `GIT_PATHSPEC_FAILURES_ONLY` flag) and may also contain the list of
# pathspecs with no match (if you used the `GIT_PATHSPEC_FIND_FAILURES`
# flag).  You must call `git_pathspec_match_list_free()` on this object.
#
# @param out Output list of matches; pass NULL to just get return value
# @param diff A generated diff list
# @param flags Combination of git_pathspec_flag_t options to control match
# @param ps Pathspec to be matched
# @return 0 on success, -1 on error, GIT_ENOTFOUND if no matches and
#         the GIT_PATHSPEC_NO_MATCH_ERROR flag is used
#
git_pathspec_match_diff = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_pathspec_match_list)),
    ct.POINTER(git_diff),
    ct.c_uint32,
    ct.POINTER(git_pathspec))(
    ("git_pathspec_match_diff", dll), (
    (1, "out"),
    (1, "diff"),
    (1, "flags"),
    (1, "ps"),))

# Free memory associates with a git_pathspec_match_list
#
# @param m The git_pathspec_match_list to be freed
#
git_pathspec_match_list_free = CFUNC(None,
    ct.POINTER(git_pathspec_match_list))(
    ("git_pathspec_match_list_free", dll), (
    (1, "m"),))

# Get the number of items in a match list.
#
# @param m The git_pathspec_match_list object
# @return Number of items in match list
#
git_pathspec_match_list_entrycount = CFUNC(ct.c_size_t,
    ct.POINTER(git_pathspec_match_list))(
    ("git_pathspec_match_list_entrycount", dll), (
    (1, "m"),))

# Get a matching filename by position.
#
# This routine cannot be used if the match list was generated by
# `git_pathspec_match_diff`.  If so, it will always return NULL.
#
# @param m The git_pathspec_match_list object
# @param pos The index into the list
# @return The filename of the match
#
git_pathspec_match_list_entry = CFUNC(ct.c_char_p,
    ct.POINTER(git_pathspec_match_list),
    ct.c_size_t)(
    ("git_pathspec_match_list_entry", dll), (
    (1, "m"),
    (1, "pos"),))

# Get a matching diff delta by position.
#
# This routine can only be used if the match list was generated by
# `git_pathspec_match_diff`.  Otherwise it will always return NULL.
#
# @param m The git_pathspec_match_list object
# @param pos The index into the list
# @return The filename of the match
#
git_pathspec_match_list_diff_entry = CFUNC(ct.POINTER(git_diff_delta),
    ct.POINTER(git_pathspec_match_list),
    ct.c_size_t)(
    ("git_pathspec_match_list_diff_entry", dll), (
    (1, "m"),
    (1, "pos"),))

# Get the number of pathspec items that did not match.
#
# This will be zero unless you passed GIT_PATHSPEC_FIND_FAILURES when
# generating the git_pathspec_match_list.
#
# @param m The git_pathspec_match_list object
# @return Number of items in original pathspec that had no matches
#
git_pathspec_match_list_failed_entrycount = CFUNC(ct.c_size_t,
    ct.POINTER(git_pathspec_match_list))(
    ("git_pathspec_match_list_failed_entrycount", dll), (
    (1, "m"),))

# Get an original pathspec string that had no matches.
#
# This will be return NULL for positions out of range.
#
# @param m The git_pathspec_match_list object
# @param pos The index into the failed items
# @return The pathspec pattern that didn't match anything
#
git_pathspec_match_list_failed_entry = CFUNC(ct.c_char_p,
    ct.POINTER(git_pathspec_match_list),
    ct.c_size_t)(
    ("git_pathspec_match_list_failed_entry", dll), (
    (1, "m"),
    (1, "pos"),))

# GIT_END_DECL
