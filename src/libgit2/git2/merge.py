# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common   import *  # noqa
from .oid      import git_oid
from .oidarray import git_oidarray
from .types    import git_repository
from .types    import git_reference
from .types    import git_commit
from .types    import git_annotated_commit
from .types    import git_index
from .index    import git_index_entry
from .types    import git_tree
from .checkout import git_checkout_options
from .diff     import git_diff_similarity_metric

# @file git2/merge.h
# @brief Git merge routines
# @defgroup git_merge Git merge routines
# @ingroup Git

# GIT_BEGIN_DECL

# The file inputs to `git_merge_file`.  Callers should populate the
# `git_merge_file_input` structure with descriptions of the files in
# each side of the conflict for use in producing the merge file.
#
class git_merge_file_input(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # Pointer to the contents of the file.
    ("ptr", git_buffer_t),

    # Size of the contents pointed to in `ptr`.
    ("size", ct.c_size_t),

    # File name of the conflicted file, or `NULL` to not merge the path.
    ("path", ct.c_char_p),

    # File mode of the conflicted file, or `0` to not merge the mode.
    ("mode", ct.c_uint),
]

GIT_MERGE_FILE_INPUT_VERSION = 1
#GIT_MERGE_FILE_INPUT_INIT = { GIT_MERGE_FILE_INPUT_VERSION }

# Initializes a `git_merge_file_input` with default values. Equivalent to
# creating an instance with GIT_MERGE_FILE_INPUT_INIT.
#
# @param opts the `git_merge_file_input` instance to initialize.
# @param version the version of the struct; you should pass
#        `GIT_MERGE_FILE_INPUT_VERSION` here.
# @return Zero on success; -1 on failure.
#
git_merge_file_input_init = CFUNC(ct.c_int,
    ct.POINTER(git_merge_file_input),
    ct.c_uint)(
    ("git_merge_file_input_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Flags for `git_merge` options.  A combination of these flags can be
# passed in via the `flags` value in the `git_merge_options`.
#
git_merge_flag_t = ct.c_int
(
    # Detect renames that occur between the common ancestor and the "ours"
    # side or the common ancestor and the "theirs" side.  This will enable
    # the ability to merge between a modified and renamed file.
    #
    GIT_MERGE_FIND_RENAMES,

    # If a conflict occurs, exit immediately instead of attempting to
    # continue resolving conflicts.  The merge operation will fail with
    # GIT_EMERGECONFLICT and no index will be returned.
    #
    GIT_MERGE_FAIL_ON_CONFLICT,

    # Do not write the REUC extension on the generated index
    #
    GIT_MERGE_SKIP_REUC,

    # If the commits being merged have multiple merge bases, do not build
    # a recursive merge base (by merging the multiple merge bases),
    # instead simply use the first base.  This flag provides a similar
    # merge base to `git-merge-resolve`.
    #
    GIT_MERGE_NO_RECURSIVE,

    # Treat this merge as if it is to produce the virtual base
    # of a recursive merge.  This will ensure that there are
    # no conflicts, any conflicting regions will keep conflict
    # markers in the merge result.
    #
    GIT_MERGE_VIRTUAL_BASE,

) = (1 << 0, 1 << 1, 1 << 2, 1 << 3, 1 << 4)

# Merge file favor options for `git_merge_options` instruct the file-level
# merging functionality how to deal with conflicting regions of the files.
#
git_merge_file_favor_t = ct.c_int
(
    # When a region of a file is changed in both branches, a conflict
    # will be recorded in the index so that `git_checkout` can produce
    # a merge file with conflict markers in the working directory.
    # This is the default.
    #
    GIT_MERGE_FILE_FAVOR_NORMAL,

    # When a region of a file is changed in both branches, the file
    # created in the index will contain the "ours" side of any conflicting
    # region.  The index will not record a conflict.
    #
    GIT_MERGE_FILE_FAVOR_OURS,

    # When a region of a file is changed in both branches, the file
    # created in the index will contain the "theirs" side of any conflicting
    # region.  The index will not record a conflict.
    #
    GIT_MERGE_FILE_FAVOR_THEIRS,

    # When a region of a file is changed in both branches, the file
    # created in the index will contain each unique line from each side,
    # which has the result of combining both files.  The index will not
    # record a conflict.
    #
    GIT_MERGE_FILE_FAVOR_UNION,

) = (0, 1, 2, 3)

# File merging flags
#
git_merge_file_flag_t = ct.c_int
(
    # Defaults
    GIT_MERGE_FILE_DEFAULT,

    # Create standard conflicted merge files
    GIT_MERGE_FILE_STYLE_MERGE,

    # Create diff3-style files
    GIT_MERGE_FILE_STYLE_DIFF3,

    # Condense non-alphanumeric regions for simplified diff file
    GIT_MERGE_FILE_SIMPLIFY_ALNUM,

    # Ignore all whitespace
    GIT_MERGE_FILE_IGNORE_WHITESPACE,

    # Ignore changes in amount of whitespace
    GIT_MERGE_FILE_IGNORE_WHITESPACE_CHANGE,

    # Ignore whitespace at end of line
    GIT_MERGE_FILE_IGNORE_WHITESPACE_EOL,

    # Use the "patience diff" algorithm
    GIT_MERGE_FILE_DIFF_PATIENCE,

    # Take extra time to find minimal diff
    GIT_MERGE_FILE_DIFF_MINIMAL,

    # Create zdiff3 ("zealous diff3")-style files
    GIT_MERGE_FILE_STYLE_ZDIFF3,

    # Do not produce file conflicts when common regions have
    # changed; keep the conflict markers in the file and accept
    # that as the merge result.
    #
    GIT_MERGE_FILE_ACCEPT_CONFLICTS,

) = (0, 1 << 0, 1 << 1, 1 << 2, 1 << 3, 1 << 4,
     1 << 5, 1 << 6, 1 << 7, 1 << 8, 1 << 9)

GIT_MERGE_CONFLICT_MARKER_SIZE  = 7

# Options for merging a file
#
class git_merge_file_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # Label for the ancestor file side of the conflict which will be prepended
    # to labels in diff3-format merge files.
    #
    ("ancestor_label", ct.c_char_p),

    # Label for our file side of the conflict which will be prepended
    # to labels in merge files.
    #
    ("our_label", ct.c_char_p),

    # Label for their file side of the conflict which will be prepended
    # to labels in merge files.
    #
    ("their_label", ct.c_char_p),

    # The file to favor in region conflicts.
    ("favor", git_merge_file_favor_t),

    # see `git_merge_file_flag_t` above
    ("flags", ct.c_uint32),

    # The size of conflict markers (eg, "<<<<<<<").
    #  Default is GIT_MERGE_CONFLICT_MARKER_SIZE.
    ("marker_size", ct.c_ushort),
]

GIT_MERGE_FILE_OPTIONS_VERSION = 1
#define GIT_MERGE_FILE_OPTIONS_INIT = { GIT_MERGE_FILE_OPTIONS_VERSION }

# Initialize git_merge_file_options structure
#
# Initializes a `git_merge_file_options` with default values. Equivalent to
# creating an instance with `GIT_MERGE_FILE_OPTIONS_INIT`.
#
# @param opts The `git_merge_file_options` struct to initialize.
# @param version The struct version; pass `GIT_MERGE_FILE_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_merge_file_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_merge_file_options),
    ct.c_uint)(
    ("git_merge_file_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Information about file-level merging
#
class git_merge_file_result(ct.Structure):
    _fields_ = [

    # True if the output was automerged, false if the output contains
    # conflict markers.
    #
    ("automergeable", ct.c_uint),

    # The path that the resultant merge file should use, or NULL if a
    # filename conflict would occur.
    #
    ("path", ct.c_char_p),

    # The mode that the resultant merge file should use.
    ("mode", ct.c_uint),

    # The contents of the merge.
    ("ptr", git_buffer_t),

    # The length of the merge contents.
    ("len", ct.c_size_t),
]

# Merging options
#
class git_merge_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # See `git_merge_flag_t` above
    ("flags", ct.c_uint32),

    # Similarity to consider a file renamed (default 50).  If
    # `GIT_MERGE_FIND_RENAMES` is enabled, added files will be compared
    # with deleted files to determine their similarity.  Files that are
    # more similar than the rename threshold (percentage-wise) will be
    # treated as a rename.
    #
    ("rename_threshold", ct.c_uint),

    # Maximum similarity sources to examine for renames (default 200).
    # If the number of rename candidates (add / delete pairs) is greater
    # than this value, inexact rename detection is aborted.
    #
    # This setting overrides the `merge.renameLimit` configuration value.
    #
    ("target_limit", ct.c_uint),

    # Pluggable similarity metric; pass NULL to use internal metric
    ("metric", ct.POINTER(git_diff_similarity_metric)),

    # Maximum number of times to merge common ancestors to build a
    # virtual merge base when faced with criss-cross merges.  When this
    # limit is reached, the next ancestor will simply be used instead of
    # attempting to merge it.  The default is unlimited.
    #
    ("recursion_limit", ct.c_uint),

    # Default merge driver to be used when both sides of a merge have
    # changed.  The default is the `text` driver.
    #
    ("default_driver", ct.c_char_p),

    # Flags for handling conflicting content, to be used with the standard
    # (`text`) merge driver.
    #
    ("file_favor", git_merge_file_favor_t),

    # see `git_merge_file_flag_t` above
    ("file_flags", ct.c_uint32),
]

GIT_MERGE_OPTIONS_VERSION = 1
#define GIT_MERGE_OPTIONS_INIT = { GIT_MERGE_OPTIONS_VERSION, GIT_MERGE_FIND_RENAMES }

# Initialize git_merge_options structure
#
# Initializes a `git_merge_options` with default values. Equivalent to
# creating an instance with `GIT_MERGE_OPTIONS_INIT`.
#
# @param opts The `git_merge_options` struct to initialize.
# @param version The struct version; pass `GIT_MERGE_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_merge_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_merge_options),
    ct.c_uint)(
    ("git_merge_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# The results of `git_merge_analysis` indicate the merge opportunities.
#
git_merge_analysis_t = ct.c_int
(
    # No merge is possible.  (Unused.)
    GIT_MERGE_ANALYSIS_NONE,

    # A "normal" merge; both HEAD and the given merge input have diverged
    # from their common ancestor.  The divergent commits must be merged.
    #
    GIT_MERGE_ANALYSIS_NORMAL,

    # All given merge inputs are reachable from HEAD, meaning the
    # repository is up-to-date and no merge needs to be performed.
    #
    GIT_MERGE_ANALYSIS_UP_TO_DATE,

    # The given merge input is a fast-forward from HEAD and no merge
    # needs to be performed.  Instead, the client can check out the
    # given merge input.
    #
    GIT_MERGE_ANALYSIS_FASTFORWARD,

    # The HEAD of the current repository is "unborn" and does not point to
    # a valid commit.  No merge can be performed, but the caller may wish
    # to simply set HEAD to the target commit(s).
    #
    GIT_MERGE_ANALYSIS_UNBORN,

) = (0, 1 << 0, 1 << 1, 1 << 2, 1 << 3)

# The user's stated preference for merges.
#
git_merge_preference_t = ct.c_int
(
    # No configuration was found that suggests a preferred behavior for
    # merge.
    #
    GIT_MERGE_PREFERENCE_NONE,

    # There is a `merge.ff=false` configuration setting, suggesting that
    # the user does not want to allow a fast-forward merge.
    #
    GIT_MERGE_PREFERENCE_NO_FASTFORWARD,

    # There is a `merge.ff=only` configuration setting, suggesting that
    # the user only wants fast-forward merges.
    #
    GIT_MERGE_PREFERENCE_FASTFORWARD_ONLY,

) = (0, 1 << 0, 1 << 1)

# Analyzes the given branch(es) and determines the opportunities for
# merging them into the HEAD of the repository.
#
# @param analysis_out analysis enumeration that the result is written into
# @param preference_out One of the `git_merge_preference_t` flag.
# @param repo the repository to merge
# @param their_heads the heads to merge into
# @param their_heads_len the number of heads to merge
# @return 0 on success or error code
#
git_merge_analysis = CFUNC(ct.c_int,
    ct.POINTER(git_merge_analysis_t),
    ct.POINTER(git_merge_preference_t),
    ct.POINTER(git_repository),
    ct.POINTER(ct.POINTER(git_annotated_commit)),
    ct.c_size_t)(
    ("git_merge_analysis", dll), (
    (1, "analysis_out"),
    (1, "preference_out"),
    (1, "repo"),
    (1, "their_heads"),
    (1, "their_heads_len"),))

# Analyzes the given branch(es) and determines the opportunities for
# merging them into a reference.
#
# @param analysis_out analysis enumeration that the result is written into
# @param preference_out One of the `git_merge_preference_t` flag.
# @param repo the repository to merge
# @param our_ref the reference to perform the analysis from
# @param their_heads the heads to merge into
# @param their_heads_len the number of heads to merge
# @return 0 on success or error code
#
git_merge_analysis_for_ref = CFUNC(ct.c_int,
    ct.POINTER(git_merge_analysis_t),
    ct.POINTER(git_merge_preference_t),
    ct.POINTER(git_repository),
    ct.POINTER(git_reference),
    ct.POINTER(ct.POINTER(git_annotated_commit)),
    ct.c_size_t)(
    ("git_merge_analysis_for_ref", dll), (
    (1, "analysis_out"),
    (1, "preference_out"),
    (1, "repo"),
    (1, "our_ref"),
    (1, "their_heads"),
    (1, "their_heads_len"),))

# Find a merge base between two commits
#
# @param out the OID of a merge base between 'one' and 'two'
# @param repo the repository where the commits exist
# @param one one of the commits
# @param two the other commit
# @return 0 on success, GIT_ENOTFOUND if not found or error code
#
git_merge_base = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.POINTER(git_oid),
    ct.POINTER(git_oid))(
    ("git_merge_base", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "one"),
    (1, "two"),))

# Find merge bases between two commits
#
# @param out array in which to store the resulting ids
# @param repo the repository where the commits exist
# @param one one of the commits
# @param two the other commit
# @return 0 on success, GIT_ENOTFOUND if not found or error code
#
git_merge_bases = CFUNC(ct.c_int,
    ct.POINTER(git_oidarray),
    ct.POINTER(git_repository),
    ct.POINTER(git_oid),
    ct.POINTER(git_oid))(
    ("git_merge_bases", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "one"),
    (1, "two"),))

# Find a merge base given a list of commits
#
# @param out the OID of a merge base considering all the commits
# @param repo the repository where the commits exist
# @param length The number of commits in the provided `input_array`
# @param input_array oids of the commits
# @return Zero on success; GIT_ENOTFOUND or -1 on failure.
#
git_merge_base_many = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.c_size_t,
    ct.POINTER(git_oid))(  # const git_oid[]
    ("git_merge_base_many", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "length"),
    (1, "input_array"),))

# Find all merge bases given a list of commits
#
# @param out array in which to store the resulting ids
# @param repo the repository where the commits exist
# @param length The number of commits in the provided `input_array`
# @param input_array oids of the commits
# @return Zero on success; GIT_ENOTFOUND or -1 on failure.
#
git_merge_bases_many = CFUNC(ct.c_int,
    ct.POINTER(git_oidarray),
    ct.POINTER(git_repository),
    ct.c_size_t,
    ct.POINTER(git_oid))(  # const git_oid[]
    ("git_merge_bases_many", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "length"),
    (1, "input_array"),))

# Find a merge base in preparation for an octopus merge
#
# @param out the OID of a merge base considering all the commits
# @param repo the repository where the commits exist
# @param length The number of commits in the provided `input_array`
# @param input_array oids of the commits
# @return Zero on success; GIT_ENOTFOUND or -1 on failure.
#
git_merge_base_octopus = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.c_size_t,
    ct.POINTER(git_oid))(  # const git_oid[]
    ("git_merge_base_octopus", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "length"),
    (1, "input_array"),))

# Merge two files as they exist in the in-memory data structures, using
# the given common ancestor as the baseline, producing a
# `git_merge_file_result` that reflects the merge result.  The
# `git_merge_file_result` must be freed with `git_merge_file_result_free`.
#
# Note that this function does not reference a repository and any
# configuration must be passed as `git_merge_file_options`.
#
# @param out The git_merge_file_result to be filled in
# @param ancestor The contents of the ancestor file
# @param ours The contents of the file in "our" side
# @param theirs The contents of the file in "their" side
# @param opts The merge file options or `NULL` for defaults
# @return 0 on success or error code
#
git_merge_file = CFUNC(ct.c_int,
    ct.POINTER(git_merge_file_result),
    ct.POINTER(git_merge_file_input),
    ct.POINTER(git_merge_file_input),
    ct.POINTER(git_merge_file_input),
    ct.POINTER(git_merge_file_options))(
    ("git_merge_file", dll), (
    (1, "out"),
    (1, "ancestor"),
    (1, "ours"),
    (1, "theirs"),
    (1, "opts"),))

# Merge two files as they exist in the index, using the given common
# ancestor as the baseline, producing a `git_merge_file_result` that
# reflects the merge result.  The `git_merge_file_result` must be freed with
# `git_merge_file_result_free`.
#
# @param out The git_merge_file_result to be filled in
# @param repo The repository
# @param ancestor The index entry for the ancestor file (stage level 1)
# @param ours The index entry for our file (stage level 2)
# @param theirs The index entry for their file (stage level 3)
# @param opts The merge file options or NULL
# @return 0 on success or error code
#
git_merge_file_from_index = CFUNC(ct.c_int,
    ct.POINTER(git_merge_file_result),
    ct.POINTER(git_repository),
    ct.POINTER(git_index_entry),
    ct.POINTER(git_index_entry),
    ct.POINTER(git_index_entry),
    ct.POINTER(git_merge_file_options))(
    ("git_merge_file_from_index", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "ancestor"),
    (1, "ours"),
    (1, "theirs"),
    (1, "opts"),))

# Frees a `git_merge_file_result`.
#
# @param result The result to free or `NULL`
#
git_merge_file_result_free = CFUNC(None,
    ct.POINTER(git_merge_file_result))(
    ("git_merge_file_result_free", dll), (
    (1, "result"),))

# Merge two trees, producing a `git_index` that reflects the result of
# the merge.  The index may be written as-is to the working directory
# or checked out.  If the index is to be converted to a tree, the caller
# should resolve any conflicts that arose as part of the merge.
#
# The returned index must be freed explicitly with `git_index_free`.
#
# @param out pointer to store the index result in
# @param repo repository that contains the given trees
# @param ancestor_tree the common ancestor between the trees (or null if none)
# @param our_tree the tree that reflects the destination tree
# @param their_tree the tree to merge in to `our_tree`
# @param opts the merge tree options (or null for defaults)
# @return 0 on success or error code
#
git_merge_trees = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_index)),
    ct.POINTER(git_repository),
    ct.POINTER(git_tree),
    ct.POINTER(git_tree),
    ct.POINTER(git_tree),
    ct.POINTER(git_merge_options))(
    ("git_merge_trees", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "ancestor_tree"),
    (1, "our_tree"),
    (1, "their_tree"),
    (1, "opts"),))

# Merge two commits, producing a `git_index` that reflects the result of
# the merge.  The index may be written as-is to the working directory
# or checked out.  If the index is to be converted to a tree, the caller
# should resolve any conflicts that arose as part of the merge.
#
# The returned index must be freed explicitly with `git_index_free`.
#
# @param out pointer to store the index result in
# @param repo repository that contains the given trees
# @param our_commit the commit that reflects the destination tree
# @param their_commit the commit to merge in to `our_commit`
# @param opts the merge tree options (or null for defaults)
# @return 0 on success or error code
#
git_merge_commits = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_index)),
    ct.POINTER(git_repository),
    ct.POINTER(git_commit),
    ct.POINTER(git_commit),
    ct.POINTER(git_merge_options))(
    ("git_merge_commits", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "our_commit"),
    (1, "their_commit"),
    (1, "opts"),))

# Merges the given commit(s) into HEAD, writing the results into the working
# directory.  Any changes are staged for commit and any conflicts are written
# to the index.  Callers should inspect the repository's index after this
# completes, resolve any conflicts and prepare a commit.
#
# For compatibility with git, the repository is put into a merging
# state. Once the commit is done (or if the user wishes to abort),
# you should clear this state by calling
# `git_repository_state_cleanup()`.
#
# @param repo the repository to merge
# @param their_heads the heads to merge into
# @param their_heads_len the number of heads to merge
# @param merge_opts merge options
# @param checkout_opts checkout options
# @return 0 on success or error code
#
git_merge = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(ct.POINTER(git_annotated_commit)),
    ct.c_size_t,
    ct.POINTER(git_merge_options),
    ct.POINTER(git_checkout_options))(
    ("git_merge", dll), (
    (1, "repo"),
    (1, "their_heads"),
    (1, "their_heads_len"),
    (1, "merge_opts"),
    (1, "checkout_opts"),))

# GIT_END_DECL
