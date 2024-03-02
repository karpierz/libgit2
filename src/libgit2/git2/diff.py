# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common   import *  # noqa
from .buffer   import git_buf
from .strarray import git_strarray
from .oid      import git_oid_t
from .oid      import git_oid
from .types    import git_off_t
from .types    import git_object_size_t
from .types    import git_repository
from .types    import git_blob
from .types    import git_index
from .types    import git_tree
from .types    import git_submodule_ignore_t

# @file git2/diff.h
# @brief Git tree and file differencing routines.
# @ingroup Git

# GIT_BEGIN_DECL

# Flags for diff options.  A combination of these flags can be passed
# in via the `flags` value in the `git_diff_options`.
#
git_diff_option_t = ct.c_int
(
    # Normal diff, the default
    GIT_DIFF_NORMAL,

    # Options controlling which files will be in the diff
    #

    # Reverse the sides of the diff
    GIT_DIFF_REVERSE,

    # Include ignored files in the diff
    GIT_DIFF_INCLUDE_IGNORED,

    # Even with GIT_DIFF_INCLUDE_IGNORED, an entire ignored directory
    #  will be marked with only a single entry in the diff; this flag
    #  adds all files under the directory as IGNORED entries, too.
    #
    GIT_DIFF_RECURSE_IGNORED_DIRS,

    # Include untracked files in the diff
    GIT_DIFF_INCLUDE_UNTRACKED,

    # Even with GIT_DIFF_INCLUDE_UNTRACKED, an entire untracked
    #  directory will be marked with only a single entry in the diff
    #  (a la what core Git does in `git status`); this flag adds *all*
    #  files under untracked directories as UNTRACKED entries, too.
    #
    GIT_DIFF_RECURSE_UNTRACKED_DIRS,

    # Include unmodified files in the diff
    GIT_DIFF_INCLUDE_UNMODIFIED,

    # Normally, a type change between files will be converted into a
    #  DELETED record for the old and an ADDED record for the new; this
    #  options enabled the generation of TYPECHANGE delta records.
    #
    GIT_DIFF_INCLUDE_TYPECHANGE,

    # Even with GIT_DIFF_INCLUDE_TYPECHANGE, blob->tree changes still
    #  generally show as a DELETED blob.  This flag tries to correctly
    #  label blob->tree transitions as TYPECHANGE records with new_file's
    #  mode set to tree.  Note: the tree SHA will not be available.
    #
    GIT_DIFF_INCLUDE_TYPECHANGE_TREES,

    # Ignore file mode changes
    GIT_DIFF_IGNORE_FILEMODE,

    # Treat all submodules as unmodified
    GIT_DIFF_IGNORE_SUBMODULES,

    # Use case insensitive filename comparisons
    GIT_DIFF_IGNORE_CASE,

    # May be combined with `GIT_DIFF_IGNORE_CASE` to specify that a file
    #  that has changed case will be returned as an add/delete pair.
    #
    GIT_DIFF_INCLUDE_CASECHANGE,

    # If the pathspec is set in the diff options, this flags indicates
    #  that the paths will be treated as literal paths instead of
    #  fnmatch patterns.  Each path in the list must either be a full
    #  path to a file or a directory.  (A trailing slash indicates that
    #  the path will _only_ match a directory).  If a directory is
    #  specified, all children will be included.
    #
    GIT_DIFF_DISABLE_PATHSPEC_MATCH,

    # Disable updating of the `binary` flag in delta records.  This is
    #  useful when iterating over a diff if you don't need hunk and data
    #  callbacks and want to avoid having to load file completely.
    #
    GIT_DIFF_SKIP_BINARY_CHECK,

    # When diff finds an untracked directory, to match the behavior of
    #  core Git, it scans the contents for IGNORED and UNTRACKED files.
    #  If *all* contents are IGNORED, then the directory is IGNORED; if
    #  any contents are not IGNORED, then the directory is UNTRACKED.
    #  This is extra work that may not matter in many cases.  This flag
    #  turns off that scan and immediately labels an untracked directory
    #  as UNTRACKED (changing the behavior to not match core Git).
    #
    GIT_DIFF_ENABLE_FAST_UNTRACKED_DIRS,

    # When diff finds a file in the working directory with stat
    # information different from the index, but the OID ends up being the
    # same, write the correct stat information into the index.  Note:
    # without this flag, diff will always leave the index untouched.
    #
    GIT_DIFF_UPDATE_INDEX,

    # Include unreadable files in the diff
    GIT_DIFF_INCLUDE_UNREADABLE,

    # Include unreadable files in the diff
    GIT_DIFF_INCLUDE_UNREADABLE_AS_UNTRACKED,

    # Options controlling how output will be generated
    #

    # Use a heuristic that takes indentation and whitespace into account
    # which generally can produce better diffs when dealing with ambiguous
    # diff hunks.
    #
    GIT_DIFF_INDENT_HEURISTIC,

    # Ignore blank lines
    GIT_DIFF_IGNORE_BLANK_LINES,

    # Treat all files as text, disabling binary attributes & detection
    GIT_DIFF_FORCE_TEXT,
    # Treat all files as binary, disabling text diffs
    GIT_DIFF_FORCE_BINARY,

    # Ignore all whitespace
    GIT_DIFF_IGNORE_WHITESPACE,
    # Ignore changes in amount of whitespace
    GIT_DIFF_IGNORE_WHITESPACE_CHANGE,
    # Ignore whitespace at end of line
    GIT_DIFF_IGNORE_WHITESPACE_EOL,

    # When generating patch text, include the content of untracked
    #  files.  This automatically turns on GIT_DIFF_INCLUDE_UNTRACKED but
    #  it does not turn on GIT_DIFF_RECURSE_UNTRACKED_DIRS.  Add that
    #  flag if you want the content of every single UNTRACKED file.
    #
    GIT_DIFF_SHOW_UNTRACKED_CONTENT,

    # When generating output, include the names of unmodified files if
    #  they are included in the git_diff.  Normally these are skipped in
    #  the formats that list files (e.g. name-only, name-status, raw).
    #  Even with this, these will not be included in patch format.
    #
    GIT_DIFF_SHOW_UNMODIFIED,

    # Use the "patience diff" algorithm
    GIT_DIFF_PATIENCE,
    # Take extra time to find minimal diff
    GIT_DIFF_MINIMAL,

    # Include the necessary deflate / delta information so that `git-apply`
    #  can apply given diff information to binary files.
    #
    GIT_DIFF_SHOW_BINARY,

) = (0,       1 << 0,  1 << 1,  1 << 2,  1 << 3,  1 << 4,  1 << 5,  1 << 6,  1 << 7,
     1 << 8,  1 << 9,  1 << 10, 1 << 11, 1 << 12, 1 << 13, 1 << 14, 1 << 15, 1 << 16,
     1 << 17, 1 << 18, 1 << 19, 1 << 20, 1 << 21, 1 << 22, 1 << 23, 1 << 24, 1 << 25,
     1 << 26, 1 << 28, 1 << 29, 1 << 30)

# The diff object that contains all individual file deltas.
#
# A `diff` represents the cumulative list of differences between two
# snapshots of a repository (possibly filtered by a set of file name
# patterns).
#
# Calculating diffs is generally done in two phases: building a list of
# diffs then traversing it. This makes is easier to share logic across
# the various types of diffs (tree vs tree, workdir vs index, etc.), and
# also allows you to insert optional diff post-processing phases,
# such as rename detection, in between the steps. When you are done with
# a diff object, it must be freed.
#
# This is an opaque structure which will be allocated by one of the diff
# generator functions below (such as `git_diff_tree_to_tree`). You are
# responsible for releasing the object memory when done, using the
# `git_diff_free()` function.
#
class git_diff(ct.Structure): pass

# Flags for the delta object and the file objects on each side.
#
# These flags are used for both the `flags` value of the `git_diff_delta`
# and the flags for the `git_diff_file` objects representing the old and
# new sides of the delta.  Values outside of this public range should be
# considered reserved for internal or future use.
#
git_diff_flag_t = ct.c_int
(   GIT_DIFF_FLAG_BINARY,      # file(s) treated as binary data
    GIT_DIFF_FLAG_NOT_BINARY,  # file(s) treated as text data
    GIT_DIFF_FLAG_VALID_ID,    # `id` value is known correct
    GIT_DIFF_FLAG_EXISTS,      # file exists at this side of the delta
    GIT_DIFF_FLAG_VALID_SIZE,  # file size value is known correct
) = (1 << 0, 1 << 1, 1 << 2, 1 << 3, 1 << 4)

# What type of change is described by a git_diff_delta?
#
# `GIT_DELTA_RENAMED` and `GIT_DELTA_COPIED` will only show up if you run
# `git_diff_find_similar()` on the diff object.
#
# `GIT_DELTA_TYPECHANGE` only shows up given `GIT_DIFF_INCLUDE_TYPECHANGE`
# in the option flags (otherwise type changes will be split into ADDED /
# DELETED pairs).
#
git_delta_t = ct.c_int
(   GIT_DELTA_UNMODIFIED,  # no changes
    GIT_DELTA_ADDED,       # entry does not exist in old version
    GIT_DELTA_DELETED,     # entry does not exist in new version
    GIT_DELTA_MODIFIED,    # entry content changed between old and new
    GIT_DELTA_RENAMED,     # entry was renamed between old and new
    GIT_DELTA_COPIED,      # entry was copied from another old entry
    GIT_DELTA_IGNORED,     # entry is ignored item in workdir
    GIT_DELTA_UNTRACKED,   # entry is untracked item in workdir
    GIT_DELTA_TYPECHANGE,  # type of entry changed between old and new
    GIT_DELTA_UNREADABLE,  # entry is unreadable
    GIT_DELTA_CONFLICTED,  # entry in the index is conflicted
) = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

# Description of one side of a delta.
#
# Although this is called a "file", it could represent a file, a symbolic
# link, a submodule commit id, or even a tree (although that only if you
# are tracking type changes or ignored/untracked directories).
#
class git_diff_file(ct.Structure):
    _fields_ = [
    # The `git_oid` of the item.  If the entry represents an
    # absent side of a diff (e.g. the `old_file` of a `GIT_DELTA_ADDED` delta),
    # then the oid will be zeroes.
    #
    ("id", git_oid),

    # The NUL-terminated path to the entry relative to the working
    # directory of the repository.
    #
    ("path", ct.c_char_p),

    # The size of the entry in bytes.
    #
    ("size", git_object_size_t),

    # A combination of the `git_diff_flag_t` types
    #
    ("flags", ct.c_uint32),

    # Roughly, the stat() `st_mode` value for the item.  This will
    # be restricted to one of the `git_filemode_t` values.
    #
    ("mode", ct.c_uint16),

    # Represents the known length of the `id` field, when
    # converted to a hex string.  It is generally `GIT_OID_SHA1_HEXSIZE`, unless this
    # delta was created from reading a patch file, in which case it may be
    # abbreviated to something reasonable, like 7 characters.
    #
    ("id_abbrev", ct.c_uint16),
]

# Description of changes to one entry.
#
# A `delta` is a file pair with an old and new revision.  The old version
# may be absent if the file was just created and the new version may be
# absent if the file was deleted.  A diff is mostly just a list of deltas.
#
# When iterating over a diff, this will be passed to most callbacks and
# you can use the contents to understand exactly what has changed.
#
# The `old_file` represents the "from" side of the diff and the `new_file`
# represents to "to" side of the diff.  What those means depend on the
# function that was used to generate the diff and will be documented below.
# You can also use the `GIT_DIFF_REVERSE` flag to flip it around.
#
# Although the two sides of the delta are named "old_file" and "new_file",
# they actually may correspond to entries that represent a file, a symbolic
# link, a submodule commit id, or even a tree (if you are tracking type
# changes or ignored/untracked directories).
#
# Under some circumstances, in the name of efficiency, not all fields will
# be filled in, but we generally try to fill in as much as possible.  One
# example is that the "flags" field may not have either the `BINARY` or the
# `NOT_BINARY` flag set to avoid examining file contents if you do not pass
# in hunk and/or line callbacks to the diff foreach iteration function.  It
# will just use the git attributes for those files.
#
# The similarity score is zero unless you call `git_diff_find_similar()`
# which does a similarity analysis of files in the diff.  Use that
# function to do rename and copy detection, and to split heavily modified
# files in add/delete pairs.  After that call, deltas with a status of
# GIT_DELTA_RENAMED or GIT_DELTA_COPIED will have a similarity score
# between 0 and 100 indicating how similar the old and new sides are.
#
# If you ask `git_diff_find_similar` to find heavily modified files to
# break, but to not#actually* break the records, then GIT_DELTA_MODIFIED
# records may have a non-zero similarity score if the self-similarity is
# below the split threshold.  To display this value like core Git, invert
# the score (a la `printf("M%03d", 100 - delta->similarity)`).
#
class git_diff_delta(ct.Structure):
    _fields_ = [
    ("status",     git_delta_t),
    ("flags",      ct.c_uint32),  # git_diff_flag_t values
    ("similarity", ct.c_uint16),  # for RENAMED and COPIED, value 0-100
    ("nfiles",     ct.c_uint16),  # number of files in this delta
    ("old_file",   git_diff_file),
    ("new_file",   git_diff_file),
]

# Diff notification callback function.
#
# The callback will be called for each file, just before the `git_diff_delta`
# gets inserted into the diff.
#
# When the callback:
# - returns < 0, the diff process will be aborted.
# - returns > 0, the delta will not be inserted into the diff, but the
#      diff process continues.
# - returns 0, the delta is inserted into the diff, and the diff process
#      continues.
#
git_diff_notify_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_diff),        # diff_so_far
    ct.POINTER(git_diff_delta),  # delta_to_add
    ct.c_char_p,                 # matched_pathspec
    ct.c_void_p)                 # payload

# Diff progress callback.
#
# Called before each file comparison.
#
# @param diff_so_far The diff being generated.
# @param old_path The path to the old file or NULL.
# @param new_path The path to the new file or NULL.
# @return Non-zero to abort the diff.
#
git_diff_progress_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_diff),  # diff_so_far
    ct.c_char_p,           # old_path
    ct.c_char_p,           # new_path
    ct.c_void_p)           # payload

# Structure describing options about how the diff should be executed.
#
# Setting all values of the structure to zero will yield the default
# values.  Similarly, passing NULL for the options structure will
# give the defaults.  The default values are marked below.
#
#
class git_diff_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),      # version for the struct

    # A combination of `git_diff_option_t` values above.
    # Defaults to GIT_DIFF_NORMAL
    #
    ("flags", ct.c_uint32),

    # options controlling which files are in the diff
    #

    # Overrides the submodule ignore setting for all submodules in the diff.
    ("ignore_submodules", git_submodule_ignore_t),

    # An array of paths / fnmatch patterns to constrain diff.
    # All paths are included by default.
    #
    ("pathspec", git_strarray),

    # An optional callback function, notifying the consumer of changes to
    # the diff as new deltas are added.
    #
    ("notify_cb", git_diff_notify_cb),

    # An optional callback function, notifying the consumer of which files
    # are being examined as the diff is generated.
    #
    ("progress_cb", git_diff_progress_cb),

    # The payload to pass to the callback functions.
    ("payload", ct.c_void_p),

    # options controlling how to diff text is generated

    # The number of unchanged lines that define the boundary of a hunk
    # (and to display before and after). Defaults to 3.
    #
    ("context_lines", ct.c_uint32),

    # The maximum number of unchanged lines between hunk boundaries before
    # the hunks will be merged into one. Defaults to 0.
    #
    ("interhunk_lines", ct.c_uint32),

    # The object ID type to emit in diffs; this is used by functions
    # that operate without a repository - namely `git_diff_buffers`,
    # or `git_diff_blobs` and `git_diff_blob_to_buffer` when one blob
    # is `NULL`.
    #
    # This may be omitted (set to `0`). If a repository is available,
    # the object ID format of the repository will be used. If no
    # repository is available then the default is `GIT_OID_SHA`.
    #
    # If this is specified and a repository is available, then the
    # specified `oid_type` must match the repository's object ID
    # format.
    #
    ("oid_type", git_oid_t),

    # The abbreviation length to use when formatting object ids.
    # Defaults to the value of 'core.abbrev' from the config, or 7 if unset.
    #
    ("id_abbrev", ct.c_uint16),

    # A size (in bytes) above which a blob will be marked as binary
    # automatically; pass a negative value to disable.
    # Defaults to 512MB.
    #
    ("max_size", git_off_t),

    # The virtual "directory" prefix for old file names in hunk headers.
    # Default is "a".
    #
    ("old_prefix", ct.c_char_p),

    # The virtual "directory" prefix for new file names in hunk headers.
    # Defaults to "b".
    #
    ("new_prefix", ct.c_char_p),
]

# The current version of the diff options structure
GIT_DIFF_OPTIONS_VERSION = 1
# Stack initializer for diff options.  Alternatively use
# `git_diff_options_init` programmatic initialization.
#
#GIT_DIFF_OPTIONS_INIT = { GIT_DIFF_OPTIONS_VERSION,
#                          0,
#                          GIT_SUBMODULE_IGNORE_UNSPECIFIED,
#                          { NULL,0 }, NULL, NULL, NULL, 3 }

# Initialize git_diff_options structure
#
# Initializes a `git_diff_options` with default values. Equivalent to creating
# an instance with GIT_DIFF_OPTIONS_INIT.
#
# @param opts The `git_diff_options` struct to initialize.
# @param version The struct version; pass `GIT_DIFF_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_diff_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_diff_options),
    ct.c_uint)(
    ("git_diff_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# When iterating over a diff, callback that will be made per file.
#
# @param delta A pointer to the delta data for the file
# @param progress Goes from 0 to 1 over the diff
# @param payload User-specified pointer from foreach function
#
git_diff_file_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_diff_delta),  # delta
    ct.c_float,                  # progress
    ct.c_void_p)                 # payload

GIT_DIFF_HUNK_HEADER_SIZE = 128

# When producing a binary diff, the binary data returned will be
# either the deflated full ("literal") contents of the file, or
# the deflated binary delta between the two sides (whichever is
# smaller).
#
git_diff_binary_t = ct.c_int
(
    # There is no binary delta.
    GIT_DIFF_BINARY_NONE,

    # The binary data is the literal contents of the file.
    GIT_DIFF_BINARY_LITERAL,

    # The binary data is the delta from one side to the other.
    GIT_DIFF_BINARY_DELTA,

) = range(0, 3)

# The contents of one of the files in a binary diff.
class git_diff_binary_file(ct.Structure):
    _fields_ = [
    # The type of binary data for this file.
    ("type", git_diff_binary_t),

    # The binary data, deflated.
    ("data", git_buffer_t),

    # The length of the binary data.
    ("datalen", ct.c_size_t),

    # The length of the binary data after inflation.
    ("inflatedlen", ct.c_size_t),
]

# Structure describing the binary contents of a diff.
#
# A `binary` file / delta is a file (or pair) for which no text diffs
# should be generated. A diff can contain delta entries that are
# binary, but no diff content will be output for those files. There is
# a base heuristic for binary detection and you can further tune the
# behavior with git attributes or diff flags and option settings.
#
class git_diff_binary(ct.Structure):
    _fields_ = [
    # Whether there is data in this binary structure or not.
    #
    # If this is `1`, then this was produced and included binary content.
    # If this is `0` then this was generated knowing only that a binary
    # file changed but without providing the data, probably from a patch
    # that said `Binary files a/file.txt and b/file.txt differ`.
    #
    ("contains_data", ct.c_uint),
    ("old_file",      git_diff_binary_file),  # The contents of the old file.
    ("new_file",      git_diff_binary_file),  # The contents of the new file.
]

# When iterating over a diff, callback that will be made for
# binary content within the diff.
#
git_diff_binary_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_diff_delta),   # delta
    ct.POINTER(git_diff_binary),  # binary
    ct.c_void_p)                  # payload

# Structure describing a hunk of a diff.
#
# A `hunk` is a span of modified lines in a delta along with some stable
# surrounding context. You can configure the amount of context and other
# properties of how hunks are generated. Each hunk also comes with a
# header that described where it starts and ends in both the old and new
# versions in the delta.
#
class git_diff_hunk(ct.Structure):
    _fields_ = [
    ("old_start",  ct.c_int),     # Starting line number in old_file
    ("old_lines",  ct.c_int),     # Number of lines in old_file
    ("new_start",  ct.c_int),     # Starting line number in new_file
    ("new_lines",  ct.c_int),     # Number of lines in new_file
    ("header_len", ct.c_size_t),  # Number of bytes in header text
    ("header", (ct.c_char * GIT_DIFF_HUNK_HEADER_SIZE)),  # Header text, NUL-byte terminated
]

# When iterating over a diff, callback that will be made per hunk.
#
git_diff_hunk_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_diff_delta),  # delta
    ct.POINTER(git_diff_hunk),   # hunk
    ct.c_void_p)                 # payload

# Line origin constants.
#
# These values describe where a line came from and will be passed to
# the git_diff_line_cb when iterating over a diff.  There are some
# special origin constants at the end that are used for the text
# output callbacks to demarcate lines that are actually part of
# the file or hunk headers.
#
git_diff_line_t = ct.c_char
(
    # These values will be sent to `git_diff_line_cb` along with the line
    GIT_DIFF_LINE_CONTEXT ,
    GIT_DIFF_LINE_ADDITION,
    GIT_DIFF_LINE_DELETION,

    GIT_DIFF_LINE_CONTEXT_EOFNL, # Both files have no LF at end
    GIT_DIFF_LINE_ADD_EOFNL,     # Old has no LF at end, new does
    GIT_DIFF_LINE_DEL_EOFNL,     # Old has LF at end, new does not

    # The following values will only be sent to a `git_diff_line_cb` when
    # the content of a diff is being formatted through `git_diff_print`.
    #
    GIT_DIFF_LINE_FILE_HDR,
    GIT_DIFF_LINE_HUNK_HDR,
    GIT_DIFF_LINE_BINARY,        # For "Binary files x and y differ"

) = (' ', '+', '-', '=', '>', '<', 'F', 'H', 'B')

# Structure describing a line (or data span) of a diff.
#
# A `line` is a range of characters inside a hunk.  It could be a context
# line (i.e. in both old and new versions), an added line (i.e. only in
# the new version), or a removed line (i.e. only in the old version).
# Unfortunately, we don't know anything about the encoding of data in the
# file being diffed, so we cannot tell you much about the line content.
# Line data will not be NUL-byte terminated, however, because it will be
# just a span of bytes inside the larger file.
#
class git_diff_line(ct.Structure):
    _fields_ = [
    ("origin",         ct.c_char),     # A git_diff_line_t value
    ("old_lineno",     ct.c_int),      # Line number in old file or -1 for added line
    ("new_lineno",     ct.c_int),      # Line number in new file or -1 for deleted line
    ("num_lines",      ct.c_int),      # Number of newline characters in content
    ("content_len",    ct.c_size_t),   # Number of bytes of data
    ("content_offset", git_off_t),     # Offset in the original file to the content
    ("content",        git_buffer_t),  # Pointer to diff text, not NUL-byte terminated
]

# When iterating over a diff, callback that will be made per text diff
# line. In this context, the provided range will be NULL.
#
# When printing a diff, callback that will be made to output each line
# of text.  This uses some extra GIT_DIFF_LINE_... constants for output
# of lines of file and hunk headers.
#
git_diff_line_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_diff_delta),  # delta   # delta that contains this data
    ct.POINTER(git_diff_hunk),   # hunk    # hunk containing this data
    ct.POINTER(git_diff_line),   # line    # line data
    ct.c_void_p)                 # payload # user reference data

# Flags to control the behavior of diff rename/copy detection.
#
git_diff_find_t = ct.c_int
(
    # Obey `diff.renames`. Overridden by any other GIT_DIFF_FIND_... flag.
    GIT_DIFF_FIND_BY_CONFIG,

    # Look for renames? (`--find-renames`)
    GIT_DIFF_FIND_RENAMES,

    # Consider old side of MODIFIED for renames? (`--break-rewrites=N`)
    GIT_DIFF_FIND_RENAMES_FROM_REWRITES,

    # Look for copies? (a la `--find-copies`).
    GIT_DIFF_FIND_COPIES,

    # Consider UNMODIFIED as copy sources? (`--find-copies-harder`).
    #
    # For this to work correctly, use GIT_DIFF_INCLUDE_UNMODIFIED when
    # the initial `git_diff` is being generated.
    #
    GIT_DIFF_FIND_COPIES_FROM_UNMODIFIED,

    # Mark significant rewrites for split (`--break-rewrites=/M`)
    GIT_DIFF_FIND_REWRITES,
    # Actually split large rewrites into delete/add pairs
    GIT_DIFF_BREAK_REWRITES,
    # Mark rewrites for split and break into delete/add pairs
    GIT_DIFF_FIND_AND_BREAK_REWRITES,

    # Find renames/copies for UNTRACKED items in working directory.
    #
    # For this to work correctly, use GIT_DIFF_INCLUDE_UNTRACKED when the
    # initial `git_diff` is being generated (and obviously the diff must
    # be against the working directory for this to make sense).
    #
    GIT_DIFF_FIND_FOR_UNTRACKED,

    # Turn on all finding features.
    GIT_DIFF_FIND_ALL,

    # Measure similarity ignoring leading whitespace (default)
    GIT_DIFF_FIND_IGNORE_LEADING_WHITESPACE,
    # Measure similarity ignoring all whitespace
    GIT_DIFF_FIND_IGNORE_WHITESPACE,
    # Measure similarity including all data
    GIT_DIFF_FIND_DONT_IGNORE_WHITESPACE,
    # Measure similarity only by comparing SHAs (fast and cheap)
    GIT_DIFF_FIND_EXACT_MATCH_ONLY,

    # Do not break rewrites unless they contribute to a rename.
    #
    # Normally, GIT_DIFF_FIND_AND_BREAK_REWRITES will measure the self-
    # similarity of modified files and split the ones that have changed a
    # lot into a DELETE / ADD pair.  Then the sides of that pair will be
    # considered candidates for rename and copy detection.
    #
    # If you add this flag in and the split pair is *not* used for an
    # actual rename or copy, then the modified record will be restored to
    # a regular MODIFIED record instead of being split.
    #
    GIT_DIFF_BREAK_REWRITES_FOR_RENAMES_ONLY,

    # Remove any UNMODIFIED deltas after find_similar is done.
    #
    # Using GIT_DIFF_FIND_COPIES_FROM_UNMODIFIED to emulate the
    # --find-copies-harder behavior requires building a diff with the
    # GIT_DIFF_INCLUDE_UNMODIFIED flag.  If you do not want UNMODIFIED
    # records in the final result, pass this flag to have them removed.
    #
    GIT_DIFF_FIND_REMOVE_UNMODIFIED,

) = (0, 1 << 0, 1 << 1, 1 << 2, 1 << 3, 1 << 4, 1 << 5,
     (1 << 4) | (1 << 5),  # GIT_DIFF_FIND_REWRITES | GIT_DIFF_BREAK_REWRITES
     1 << 6, 0x0ff, 0, 1 << 12, 1 << 13, 1 << 14, 1 << 15, 1 << 16)

# Pluggable similarity metric
#
class git_diff_similarity_metric(ct.Structure):
    _fields_ = [
    ("file_signature",   GIT_CALLBACK(ct.c_int,
                             ct.POINTER(ct.c_void_p),    # out
                             ct.POINTER(git_diff_file),  # file
                             ct.c_char_p,                # fullpath
                             ct.c_void_p)),              # payload
    ("buffer_signature", GIT_CALLBACK(ct.c_int,
                             ct.POINTER(ct.c_void_p),    # out
                             ct.POINTER(git_diff_file),  # file
                             git_buffer_t,               # buf
                             ct.c_size_t,                # buflen
                             ct.c_void_p)),              # payload
    ("free_signature",   GIT_CALLBACK(None,
                             ct.c_void_p,                # sig
                             ct.c_void_p)),              # payload
    ("similarity",       GIT_CALLBACK(ct.c_int,
                             ct.POINTER(ct.c_int),       # score
                             ct.c_void_p,                # siga
                             ct.c_void_p,                # sigb
                             ct.c_void_p)),              # payload
    ("payload",          ct.c_void_p),
]

# Control behavior of rename and copy detection
#
# These options mostly mimic parameters that can be passed to git-diff.
#
class git_diff_find_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # Combination of git_diff_find_t values (default GIT_DIFF_FIND_BY_CONFIG).
    # NOTE: if you don't explicitly set this, `diff.renames` could be set
    # to false, resulting in `git_diff_find_similar` doing nothing.
    #
    ("flags", ct.c_uint32),

    # Threshold above which similar files will be considered renames.
    # This is equivalent to the -M option. Defaults to 50.
    #
    ("rename_threshold", ct.c_uint16),

    # Threshold below which similar files will be eligible to be a rename source.
    # This is equivalent to the first part of the -B option. Defaults to 50.
    #
    ("rename_from_rewrite_threshold", ct.c_uint16),

    # Threshold above which similar files will be considered copies.
    # This is equivalent to the -C option. Defaults to 50.
    #
    ("copy_threshold", ct.c_uint16),

    # Threshold below which similar files will be split into a delete/add pair.
    # This is equivalent to the last part of the -B option. Defaults to 60.
    #
    ("break_rewrite_threshold", ct.c_uint16),

    # Maximum number of matches to consider for a particular file.
    #
    # This is a little different from the `-l` option from Git because we
    # will still process up to this many matches before abandoning the search.
    # Defaults to 1000.
    #
    ("rename_limit", ct.c_size_t),

    # The `metric` option allows you to plug in a custom similarity metric.
    #
    # Set it to NULL to use the default internal metric.
    #
    # The default metric is based on sampling hashes of ranges of data in
    # the file, which is a pretty good similarity approximation that should
    # work fairly well for both text and binary data while still being
    # pretty fast with a fixed memory overhead.
    #
    ("metric", ct.POINTER(git_diff_similarity_metric)),
]

GIT_DIFF_FIND_OPTIONS_VERSION = 1
#GIT_DIFF_FIND_OPTIONS_INIT = { GIT_DIFF_FIND_OPTIONS_VERSION }

# Initialize git_diff_find_options structure
#
# Initializes a `git_diff_find_options` with default values. Equivalent to creating
# an instance with GIT_DIFF_FIND_OPTIONS_INIT.
#
# @param opts The `git_diff_find_options` struct to initialize.
# @param version The struct version; pass `GIT_DIFF_FIND_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_diff_find_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_diff_find_options),
    ct.c_uint)(
    ("git_diff_find_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# @name Diff Generator Functions
#
# These are the functions you would use to create (or destroy) a
# git_diff from various objects in a repository.
#

# Deallocate a diff.
#
# @param diff The previously created diff; cannot be used after free.
#
git_diff_free = CFUNC(None,
    ct.POINTER(git_diff))(
    ("git_diff_free", dll), (
    (1, "diff"),))

# Create a diff with the difference between two tree objects.
#
# This is equivalent to `git diff <old-tree> <new-tree>`
#
# The first tree will be used for the "old_file" side of the delta and the
# second tree will be used for the "new_file" side of the delta.  You can
# pass NULL to indicate an empty tree, although it is an error to pass
# NULL for both the `old_tree` and `new_tree`.
#
# @param diff Output pointer to a git_diff pointer to be allocated.
# @param repo The repository containing the trees.
# @param old_tree A git_tree object to diff from, or NULL for empty tree.
# @param new_tree A git_tree object to diff to, or NULL for empty tree.
# @param opts Structure with options to influence diff or NULL for defaults.
# @return 0 or an error code.
#
git_diff_tree_to_tree = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_diff)),
    ct.POINTER(git_repository),
    ct.POINTER(git_tree),
    ct.POINTER(git_tree),
    ct.POINTER(git_diff_options))(
    ("git_diff_tree_to_tree", dll), (
    (1, "diff"),
    (1, "repo"),
    (1, "old_tree"),
    (1, "new_tree"),
    (1, "opts"),))

# Create a diff between a tree and repository index.
#
# This is equivalent to `git diff --cached <treeish>` or if you pass
# the HEAD tree, then like `git diff --cached`.
#
# The tree you pass will be used for the "old_file" side of the delta, and
# the index will be used for the "new_file" side of the delta.
#
# If you pass NULL for the index, then the existing index of the `repo`
# will be used.  In this case, the index will be refreshed from disk
# (if it has changed) before the diff is generated.
#
# @param diff Output pointer to a git_diff pointer to be allocated.
# @param repo The repository containing the tree and index.
# @param old_tree A git_tree object to diff from, or NULL for empty tree.
# @param index The index to diff with; repo index used if NULL.
# @param opts Structure with options to influence diff or NULL for defaults.
# @return 0 or an error code.
#
git_diff_tree_to_index = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_diff)),
    ct.POINTER(git_repository),
    ct.POINTER(git_tree),
    ct.POINTER(git_index),
    ct.POINTER(git_diff_options))(
    ("git_diff_tree_to_index", dll), (
    (1, "diff"),
    (1, "repo"),
    (1, "old_tree"),
    (1, "index"),
    (1, "opts"),))

# Create a diff between the repository index and the workdir directory.
#
# This matches the `git diff` command.  See the note below on
# `git_diff_tree_to_workdir` for a discussion of the difference between
# `git diff` and `git diff HEAD` and how to emulate a `git diff <treeish>`
# using libgit2.
#
# The index will be used for the "old_file" side of the delta, and the
# working directory will be used for the "new_file" side of the delta.
#
# If you pass NULL for the index, then the existing index of the `repo`
# will be used.  In this case, the index will be refreshed from disk
# (if it has changed) before the diff is generated.
#
# @param diff Output pointer to a git_diff pointer to be allocated.
# @param repo The repository.
# @param index The index to diff from; repo index used if NULL.
# @param opts Structure with options to influence diff or NULL for defaults.
# @return 0 or an error code.
#
git_diff_index_to_workdir = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_diff)),
    ct.POINTER(git_repository),
    ct.POINTER(git_index),
    ct.POINTER(git_diff_options))(
    ("git_diff_index_to_workdir", dll), (
    (1, "diff"),
    (1, "repo"),
    (1, "index"),
    (1, "opts"),))

# Create a diff between a tree and the working directory.
#
# The tree you provide will be used for the "old_file" side of the delta,
# and the working directory will be used for the "new_file" side.
#
# This is not the same as `git diff <treeish>` or `git diff-index
# <treeish>`.  Those commands use information from the index, whereas this
# function strictly returns the differences between the tree and the files
# in the working directory, regardless of the state of the index.  Use
# `git_diff_tree_to_workdir_with_index` to emulate those commands.
#
# To see difference between this and `git_diff_tree_to_workdir_with_index`,
# consider the example of a staged file deletion where the file has then
# been put back into the working dir and further modified.  The
# tree-to-workdir diff for that file is 'modified', but `git diff` would
# show status 'deleted' since there is a staged delete.
#
# @param diff A pointer to a git_diff pointer that will be allocated.
# @param repo The repository containing the tree.
# @param old_tree A git_tree object to diff from, or NULL for empty tree.
# @param opts Structure with options to influence diff or NULL for defaults.
# @return 0 or an error code.
#
git_diff_tree_to_workdir = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_diff)),
    ct.POINTER(git_repository),
    ct.POINTER(git_tree),
    ct.POINTER(git_diff_options))(
    ("git_diff_tree_to_workdir", dll), (
    (1, "diff"),
    (1, "repo"),
    (1, "old_tree"),
    (1, "opts"),))

# Create a diff between a tree and the working directory using index data
# to account for staged deletes, tracked files, etc.
#
# This emulates `git diff <tree>` by diffing the tree to the index and
# the index to the working directory and blending the results into a
# single diff that includes staged deleted, etc.
#
# @param diff A pointer to a git_diff pointer that will be allocated.
# @param repo The repository containing the tree.
# @param old_tree A git_tree object to diff from, or NULL for empty tree.
# @param opts Structure with options to influence diff or NULL for defaults.
# @return 0 or an error code.
#
git_diff_tree_to_workdir_with_index = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_diff)),
    ct.POINTER(git_repository),
    ct.POINTER(git_tree),
    ct.POINTER(git_diff_options))(
    ("git_diff_tree_to_workdir_with_index", dll), (
    (1, "diff"),
    (1, "repo"),
    (1, "old_tree"),
    (1, "opts"),))

# Create a diff with the difference between two index objects.
#
# The first index will be used for the "old_file" side of the delta and the
# second index will be used for the "new_file" side of the delta.
#
# @param diff Output pointer to a git_diff pointer to be allocated.
# @param repo The repository containing the indexes.
# @param old_index A git_index object to diff from.
# @param new_index A git_index object to diff to.
# @param opts Structure with options to influence diff or NULL for defaults.
# @return 0 or an error code.
#
git_diff_index_to_index = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_diff)),
    ct.POINTER(git_repository),
    ct.POINTER(git_index),
    ct.POINTER(git_index),
    ct.POINTER(git_diff_options))(
    ("git_diff_index_to_index", dll), (
    (1, "diff"),
    (1, "repo"),
    (1, "old_index"),
    (1, "new_index"),
    (1, "opts"),))

# Merge one diff into another.
#
# This merges items from the "from" list into the "onto" list.  The
# resulting diff will have all items that appear in either list.
# If an item appears in both lists, then it will be "merged" to appear
# as if the old version was from the "onto" list and the new version
# is from the "from" list (with the exception that if the item has a
# pending DELETE in the middle, then it will show as deleted).
#
# @param onto Diff to merge into.
# @param from Diff to merge.
# @return 0 or an error code.
#
git_diff_merge = CFUNC(ct.c_int,
    ct.POINTER(git_diff),
    ct.POINTER(git_diff))(
    ("git_diff_merge", dll), (
    (1, "onto"),
    (1, "from"),))

# Transform a diff marking file renames, copies, etc.
#
# This modifies a diff in place, replacing old entries that look
# like renames or copies with new entries reflecting those changes.
# This also will, if requested, break modified files into add/remove
# pairs if the amount of change is above a threshold.
#
# @param diff diff to run detection algorithms on
# @param options Control how detection should be run, NULL for defaults
# @return 0 on success, -1 on failure
#
git_diff_find_similar = CFUNC(ct.c_int,
    ct.POINTER(git_diff),
    ct.POINTER(git_diff_find_options))(
    ("git_diff_find_similar", dll), (
    (1, "diff"),
    (1, "options"),))

# @name Diff Processor Functions
#
# These are the functions you apply to a diff to process it
# or read it in some way.
#

# Query how many diff records are there in a diff.
#
# @param diff A git_diff generated by one of the above functions
# @return Count of number of deltas in the list
#
git_diff_num_deltas = CFUNC(ct.c_size_t,
    ct.POINTER(git_diff))(
    ("git_diff_num_deltas", dll), (
    (1, "diff"),))

# Query how many diff deltas are there in a diff filtered by type.
#
# This works just like `git_diff_num_deltas()` with an extra parameter
# that is a `git_delta_t` and returns just the count of how many deltas
# match that particular type.
#
# @param diff A git_diff generated by one of the above functions
# @param type A git_delta_t value to filter the count
# @return Count of number of deltas matching delta_t type
#
git_diff_num_deltas_of_type = CFUNC(ct.c_size_t,
    ct.POINTER(git_diff),
    git_delta_t)(
    ("git_diff_num_deltas_of_type", dll), (
    (1, "diff"),
    (1, "type"),))

# Return the diff delta for an entry in the diff list.
#
# The `git_diff_delta` pointer points to internal data and you do not
# have to release it when you are done with it.  It will go away when
# the# `git_diff` (or any associated `git_patch`) goes away.
#
# Note that the flags on the delta related to whether it has binary
# content or not may not be set if there are no attributes set for the
# file and there has been no reason to load the file data at this point.
# For now, if you need those flags to be up to date, your only option is
# to either use `git_diff_foreach` or create a `git_patch`.
#
# @param diff Diff list object
# @param idx Index into diff list
# @return Pointer to git_diff_delta (or NULL if `idx` out of range)
#
git_diff_get_delta = CFUNC(ct.POINTER(git_diff_delta),
    ct.POINTER(git_diff),
    ct.c_size_t)(
    ("git_diff_get_delta", dll), (
    (1, "diff"),
    (1, "idx"),))

# Check if deltas are sorted case sensitively or insensitively.
#
# @param diff diff to check
# @return 0 if case sensitive, 1 if case is ignored
#
git_diff_is_sorted_icase = CFUNC(ct.c_int,
    ct.POINTER(git_diff))(
    ("git_diff_is_sorted_icase", dll), (
    (1, "diff"),))

# Loop over all deltas in a diff issuing callbacks.
#
# This will iterate through all of the files described in a diff.  You
# should provide a file callback to learn about each file.
#
# The "hunk" and "line" callbacks are optional, and the text diff of the
# files will only be calculated if they are not NULL.  Of course, these
# callbacks will not be invoked for binary files on the diff or for
# files whose only changed is a file mode change.
#
# Returning a non-zero value from any of the callbacks will terminate
# the iteration and return the value to the user.
#
# @param diff A git_diff generated by one of the above functions.
# @param file_cb Callback function to make per file in the diff.
# @param binary_cb Optional callback to make for binary files.
# @param hunk_cb Optional callback to make per hunk of text diff.  This
#                callback is called to describe a range of lines in the
#                diff.  It will not be issued for binary files.
# @param line_cb Optional callback to make per line of diff text.  This
#                same callback will be made for context lines, added, and
#                removed lines, and even for a deleted trailing newline.
# @param payload Reference pointer that will be passed to your callbacks.
# @return 0 on success, non-zero callback return value, or error code
#
git_diff_foreach = CFUNC(ct.c_int,
    ct.POINTER(git_diff),
    git_diff_file_cb,
    git_diff_binary_cb,
    git_diff_hunk_cb,
    git_diff_line_cb,
    ct.c_void_p)(
    ("git_diff_foreach", dll), (
    (1, "diff"),
    (1, "file_cb"),
    (1, "binary_cb"),
    (1, "hunk_cb"),
    (1, "line_cb"),
    (1, "payload"),))

# Look up the single character abbreviation for a delta status code.
#
# When you run `git diff --name-status` it uses single letter codes in
# the output such as 'A' for added, 'D' for deleted, 'M' for modified,
# etc.  This function converts a git_delta_t value into these letters for
# your own purposes.  GIT_DELTA_UNTRACKED will return a space (i.e. ' ').
#
# @param status The git_delta_t value to look up
# @return The single character label for that code
#
git_diff_status_char = CFUNC(ct.c_char,
    git_delta_t)(
    ("git_diff_status_char", dll), (
    (1, "status"),))

# Possible output formats for diff data
#
git_diff_format_t = ct.c_int
(   GIT_DIFF_FORMAT_PATCH,         # full git diff
    GIT_DIFF_FORMAT_PATCH_HEADER,  # just the file headers of patch
    GIT_DIFF_FORMAT_RAW,           # like git diff --raw
    GIT_DIFF_FORMAT_NAME_ONLY,     # like git diff --name-only
    GIT_DIFF_FORMAT_NAME_STATUS,   # like git diff --name-status
    GIT_DIFF_FORMAT_PATCH_ID,      # git diff as used by git patch-id
) = (1, 2, 3, 4, 5, 6)

# Iterate over a diff generating formatted text output.
#
# Returning a non-zero value from the callbacks will terminate the
# iteration and return the non-zero value to the caller.
#
# @param diff A git_diff generated by one of the above functions.
# @param format A git_diff_format_t value to pick the text format.
# @param print_cb Callback to make per line of diff text.
# @param payload Reference pointer that will be passed to your callback.
# @return 0 on success, non-zero callback return value, or error code
#
git_diff_print = CFUNC(ct.c_int,
    ct.POINTER(git_diff),
    git_diff_format_t,
    git_diff_line_cb,
    ct.c_void_p)(
    ("git_diff_print", dll), (
    (1, "diff"),
    (1, "format"),
    (1, "print_cb"),
    (1, "payload"),))

# Produce the complete formatted text output from a diff into a
# buffer.
#
# @param out A pointer to a user-allocated git_buf that will
#            contain the diff text
# @param diff A git_diff generated by one of the above functions.
# @param format A git_diff_format_t value to pick the text format.
# @return 0 on success or error code
#
git_diff_to_buf = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_diff),
    git_diff_format_t)(
    ("git_diff_to_buf", dll), (
    (1, "out"),
    (1, "diff"),
    (1, "format"),))

# Low-level file comparison, invoking callbacks per difference.
#

# Directly run a diff on two blobs.
#
# Compared to a file, a blob lacks some contextual information. As such,
# the `git_diff_file` given to the callback will have some fake data; i.e.
# `mode` will be 0 and `path` will be NULL.
#
# NULL is allowed for either `old_blob` or `new_blob` and will be treated
# as an empty blob, with the `oid` set to NULL in the `git_diff_file` data.
# Passing NULL for both blobs is a noop; no callbacks will be made at all.
#
# We do run a binary content check on the blob content and if either blob
# looks like binary data, the `git_diff_delta` binary attribute will be set
# to 1 and no call to the hunk_cb nor line_cb will be made (unless you pass
# `GIT_DIFF_FORCE_TEXT` of course).
#
# @param old_blob Blob for old side of diff, or NULL for empty blob
# @param old_as_path Treat old blob as if it had this filename; can be NULL
# @param new_blob Blob for new side of diff, or NULL for empty blob
# @param new_as_path Treat new blob as if it had this filename; can be NULL
# @param options Options for diff, or NULL for default options
# @param file_cb Callback for "file"; made once if there is a diff; can be NULL
# @param binary_cb Callback for binary files; can be NULL
# @param hunk_cb Callback for each hunk in diff; can be NULL
# @param line_cb Callback for each line in diff; can be NULL
# @param payload Payload passed to each callback function
# @return 0 on success, non-zero callback return value, or error code
#
git_diff_blobs = CFUNC(ct.c_int,
    ct.POINTER(git_blob),
    ct.c_char_p,
    ct.POINTER(git_blob),
    ct.c_char_p,
    ct.POINTER(git_diff_options),
    git_diff_file_cb,
    git_diff_binary_cb,
    git_diff_hunk_cb,
    git_diff_line_cb,
    ct.c_void_p)(
    ("git_diff_blobs", dll), (
    (1, "old_blob"),
    (1, "old_as_path"),
    (1, "new_blob"),
    (1, "new_as_path"),
    (1, "options"),
    (1, "file_cb"),
    (1, "binary_cb"),
    (1, "hunk_cb"),
    (1, "line_cb"),
    (1, "payload"),))

# Directly run a diff between a blob and a buffer.
#
# As with `git_diff_blobs`, comparing a blob and buffer lacks some context,
# so the `git_diff_file` parameters to the callbacks will be faked a la the
# rules for `git_diff_blobs()`.
#
# Passing NULL for `old_blob` will be treated as an empty blob (i.e. the
# `file_cb` will be invoked with GIT_DELTA_ADDED and the diff will be the
# entire content of the buffer added).  Passing NULL to the buffer will do
# the reverse, with GIT_DELTA_REMOVED and blob content removed.
#
# @param old_blob Blob for old side of diff, or NULL for empty blob
# @param old_as_path Treat old blob as if it had this filename; can be NULL
# @param buffer Raw data for new side of diff, or NULL for empty
# @param buffer_len Length of raw data for new side of diff
# @param buffer_as_path Treat buffer as if it had this filename; can be NULL
# @param options Options for diff, or NULL for default options
# @param file_cb Callback for "file"; made once if there is a diff; can be NULL
# @param binary_cb Callback for binary files; can be NULL
# @param hunk_cb Callback for each hunk in diff; can be NULL
# @param line_cb Callback for each line in diff; can be NULL
# @param payload Payload passed to each callback function
# @return 0 on success, non-zero callback return value, or error code
#
git_diff_blob_to_buffer = CFUNC(ct.c_int,
    ct.POINTER(git_blob),
    ct.c_char_p,
    git_buffer_t,
    ct.c_size_t,
    ct.c_char_p,
    ct.POINTER(git_diff_options),
    git_diff_file_cb,
    git_diff_binary_cb,
    git_diff_hunk_cb,
    git_diff_line_cb,
    ct.c_void_p)(
    ("git_diff_blob_to_buffer", dll), (
    (1, "old_blob"),
    (1, "old_as_path"),
    (1, "buffer"),
    (1, "buffer_len"),
    (1, "buffer_as_path"),
    (1, "options"),
    (1, "file_cb"),
    (1, "binary_cb"),
    (1, "hunk_cb"),
    (1, "line_cb"),
    (1, "payload"),))

# Directly run a diff between two buffers.
#
# Even more than with `git_diff_blobs`, comparing two buffer lacks
# context, so the `git_diff_file` parameters to the callbacks will be
# faked a la the rules for `git_diff_blobs()`.
#
# @param old_buffer Raw data for old side of diff, or NULL for empty
# @param old_len Length of the raw data for old side of the diff
# @param old_as_path Treat old buffer as if it had this filename; can be NULL
# @param new_buffer Raw data for new side of diff, or NULL for empty
# @param new_len Length of raw data for new side of diff
# @param new_as_path Treat buffer as if it had this filename; can be NULL
# @param options Options for diff, or NULL for default options
# @param file_cb Callback for "file"; made once if there is a diff; can be NULL
# @param binary_cb Callback for binary files; can be NULL
# @param hunk_cb Callback for each hunk in diff; can be NULL
# @param line_cb Callback for each line in diff; can be NULL
# @param payload Payload passed to each callback function
# @return 0 on success, non-zero callback return value, or error code
#
git_diff_buffers = CFUNC(ct.c_int,
    ct.c_void_p,
    ct.c_size_t,
    ct.c_char_p,
    ct.c_void_p,
    ct.c_size_t,
    ct.c_char_p,
    ct.POINTER(git_diff_options),
    git_diff_file_cb,
    git_diff_binary_cb,
    git_diff_hunk_cb,
    git_diff_line_cb,
    ct.c_void_p)(
    ("git_diff_buffers", dll), (
    (1, "old_buffer"),
    (1, "old_len"),
    (1, "old_as_path"),
    (1, "new_buffer"),
    (1, "new_len"),
    (1, "new_as_path"),
    (1, "options"),
    (1, "file_cb"),
    (1, "binary_cb"),
    (1, "hunk_cb"),
    (1, "line_cb"),
    (1, "payload"),))

# Patch file parsing.
#

# Options for parsing a diff / patch file.
#
class git_diff_parse_options(ct.Structure):
    _fields_ = [
    ("version",  ct.c_uint),
    ("oid_type", git_oid_t),
]

# The current version of the diff parse options structure
GIT_DIFF_PARSE_OPTIONS_VERSION = 1

# Stack initializer for diff parse options.  Alternatively use
# `git_diff_parse_options_init` programmatic initialization.
#
#define GIT_DIFF_PARSE_OPTIONS_INIT = { GIT_DIFF_PARSE_OPTIONS_VERSION, GIT_OID_DEFAULT }

# Read the contents of a git patch file into a `git_diff` object.
#
# The diff object produced is similar to the one that would be
# produced if you actually produced it computationally by comparing
# two trees, however there may be subtle differences.  For example,
# a patch file likely contains abbreviated object IDs, so the
# object IDs in a `git_diff_delta` produced by this function will
# also be abbreviated.
#
# This function will only read patch files created by a git
# implementation, it will not read unified diffs produced by
# the `diff` program, nor any other types of patch files.
#
# @param out A pointer to a git_diff pointer that will be allocated.
# @param content The contents of a patch file
# @param content_len The length of the patch file contents
# @return 0 or an error code
#
if defined("GIT_EXPERIMENTAL_SHA256"):
    git_diff_from_buffer = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_diff)),
        git_buffer_t,
        ct.c_size_t,
        ct.POINTER(git_diff_parse_options))(
        ("git_diff_from_buffer", dll), (
        (1, "out"),
        (1, "content"),
        (1, "content_len"),
        (1, "opts"),))
else:
    git_diff_from_buffer = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_diff)),
        git_buffer_t,
        ct.c_size_t)(
        ("git_diff_from_buffer", dll), (
        (1, "out"),
        (1, "content"),
        (1, "content_len"),))

# This is an opaque structure which is allocated by `git_diff_get_stats`.
# You are responsible for releasing the object memory when done, using the
# `git_diff_stats_free()` function.
#
class git_diff_stats(ct.Structure): pass

# Formatting options for diff stats
#
git_diff_stats_format_t = ct.c_int
(
    # No stats
    GIT_DIFF_STATS_NONE,

    # Full statistics, equivalent of `--stat`
    GIT_DIFF_STATS_FULL,

    # Short statistics, equivalent of `--shortstat`
    GIT_DIFF_STATS_SHORT,

    # Number statistics, equivalent of `--numstat`
    GIT_DIFF_STATS_NUMBER,

    # Extended header information such as creations, renames and
    # mode changes, equivalent of `--summary`
    GIT_DIFF_STATS_INCLUDE_SUMMARY,

) = (0, 1 << 0, 1 << 1, 1 << 2, 1 << 3)

# Accumulate diff statistics for all patches.
#
# @param out Structure containing the diff statistics.
# @param diff A git_diff generated by one of the above functions.
# @return 0 on success; non-zero on error
#
git_diff_get_stats = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_diff_stats)),
    ct.POINTER(git_diff))(
    ("git_diff_get_stats", dll), (
    (1, "out"),
    (1, "diff"),))

# Get the total number of files changed in a diff
#
# @param stats A `git_diff_stats` generated by one of the above functions.
# @return total number of files changed in the diff
#
git_diff_stats_files_changed = CFUNC(ct.c_size_t,
    ct.POINTER(git_diff_stats))(
    ("git_diff_stats_files_changed", dll), (
    (1, "stats"),))

# Get the total number of insertions in a diff
#
# @param stats A `git_diff_stats` generated by one of the above functions.
# @return total number of insertions in the diff
#
git_diff_stats_insertions = CFUNC(ct.c_size_t,
    ct.POINTER(git_diff_stats))(
    ("git_diff_stats_insertions", dll), (
    (1, "stats"),))

# Get the total number of deletions in a diff
#
# @param stats A `git_diff_stats` generated by one of the above functions.
# @return total number of deletions in the diff
#
git_diff_stats_deletions = CFUNC(ct.c_size_t,
    ct.POINTER(git_diff_stats))(
    ("git_diff_stats_deletions", dll), (
    (1, "stats"),))

# Print diff statistics to a `git_buf`.
#
# @param out buffer to store the formatted diff statistics in.
# @param stats A `git_diff_stats` generated by one of the above functions.
# @param format Formatting option.
# @param width Target width for output (only affects GIT_DIFF_STATS_FULL)
# @return 0 on success; non-zero on error
#
git_diff_stats_to_buf = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_diff_stats),
    git_diff_stats_format_t,
    ct.c_size_t)(
    ("git_diff_stats_to_buf", dll), (
    (1, "out"),
    (1, "stats"),
    (1, "format"),
    (1, "width"),))

# Deallocate a `git_diff_stats`.
#
# @param stats The previously created statistics object;
# cannot be used after free.
#
git_diff_stats_free = CFUNC(None,
    ct.POINTER(git_diff_stats))(
    ("git_diff_stats_free", dll), (
    (1, "stats"),))

# Patch ID options structure
#
# Initialize with `GIT_PATCHID_OPTIONS_INIT`. Alternatively, you can
# use `git_diff_patchid_options_init`.
#
#
class git_diff_patchid_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),
]

GIT_DIFF_PATCHID_OPTIONS_VERSION = 1
#GIT_DIFF_PATCHID_OPTIONS_INIT = { GIT_DIFF_PATCHID_OPTIONS_VERSION }

# Initialize git_diff_patchid_options structure
#
# Initializes a `git_diff_patchid_options` with default values. Equivalent to
# creating an instance with `GIT_DIFF_PATCHID_OPTIONS_INIT`.
#
# @param opts The `git_diff_patchid_options` struct to initialize.
# @param version The struct version; pass `GIT_DIFF_PATCHID_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_diff_patchid_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_diff_patchid_options),
    ct.c_uint)(
    ("git_diff_patchid_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Calculate the patch ID for the given patch.
#
# Calculate a stable patch ID for the given patch by summing the
# hash of the file diffs, ignoring whitespace and line numbers.
# This can be used to derive whether two diffs are the same with
# a high probability.
#
# Currently, this function only calculates stable patch IDs, as
# defined in git-patch-id(1), and should in fact generate the
# same IDs as the upstream git project does.
#
# @param out Pointer where the calculated patch ID should be stored
# @param diff The diff to calculate the ID for
# @param opts Options for how to calculate the patch ID. This is
#  intended for future changes, as currently no options are
#  available.
# @return 0 on success, an error code otherwise.
#
git_diff_patchid = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_diff),
    ct.POINTER(git_diff_patchid_options))(
    ("git_diff_patchid", dll), (
    (1, "out"),
    (1, "diff"),
    (1, "opts"),))

# GIT_END_DECL
