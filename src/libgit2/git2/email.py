# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .oid    import git_oid
from .buffer import git_buf
from .types  import git_signature
from .types  import git_commit
from .diff   import git_diff
from .diff   import git_diff_options
from .diff   import git_diff_find_options

# @file git2/email.h
# @brief Git email formatting and application routines.
# @ingroup Git

# GIT_BEGIN_DECL

# Formatting options for diff e-mail generation
#
git_email_create_flags_t = ct.c_int
(
    # Normal patch, the default
    GIT_EMAIL_CREATE_DEFAULT,

    # Do not include patch numbers in the subject prefix.
    GIT_EMAIL_CREATE_OMIT_NUMBERS,

    # Include numbers in the subject prefix even when the
    # patch is for a single commit (1/1).
    #
    GIT_EMAIL_CREATE_ALWAYS_NUMBER,

    # Do not perform rename or similarity detection.
    GIT_EMAIL_CREATE_NO_RENAMES,

) = (0, 1 << 0, 1 << 1, 1 << 2)

# Options for controlling the formatting of the generated e-mail.
#
class git_email_create_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # see `git_email_create_flags_t` above
    ("flags", ct.c_uint32),

    # Options to use when creating diffs
    ("diff_opts", git_diff_options),

    # Options for finding similarities within diffs
    ("diff_find_opts", git_diff_find_options),

    # The subject prefix, by default "PATCH".  If set to an empty
    # string ("") then only the patch numbers will be shown in the
    # prefix.  If the subject_prefix is empty and patch numbers
    # are not being shown, the prefix will be omitted entirely.
    #
    ("subject_prefix", ct.c_char_p),

    # The starting patch number; this cannot be 0.  By default,
    # this is 1.
    #
    ("start_number", ct.c_size_t),

    # The "re-roll" number.  By default, there is no re-roll.
    ("reroll_number", ct.c_size_t),
]

# By default, our options include rename detection and binary
# diffs to match `git format-patch`.
#
GIT_EMAIL_CREATE_OPTIONS_VERSION = 1
#define GIT_EMAIL_CREATE_OPTIONS_INIT = { GIT_EMAIL_CREATE_OPTIONS_VERSION,
#                                         GIT_EMAIL_CREATE_DEFAULT,
#                                         { GIT_DIFF_OPTIONS_VERSION,
#                                           GIT_DIFF_SHOW_BINARY,
#                                           GIT_SUBMODULE_IGNORE_UNSPECIFIED,
#                                           { NULL, 0 }, NULL, NULL, NULL, 3 },
#                                         GIT_DIFF_FIND_OPTIONS_INIT }

# Create a diff for a commit in mbox format for sending via email.
#
# @param out buffer to store the e-mail patch in
# @param diff the changes to include in the email
# @param patch_idx the patch index
# @param patch_count the total number of patches that will be included
# @param commit_id the commit id for this change
# @param summary the commit message for this change
# @param body optional text to include above the diffstat
# @param author the person who authored this commit
# @param opts email creation options
#
git_email_create_from_diff = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_diff),
    ct.c_size_t,
    ct.c_size_t,
    ct.POINTER(git_oid),
    ct.c_char_p,
    ct.c_char_p,
    ct.POINTER(git_signature),
    ct.POINTER(git_email_create_options))(
    ("git_email_create_from_diff", dll), (
    (1, "out"),
    (1, "diff"),
    (1, "patch_idx"),
    (1, "patch_count"),
    (1, "commit_id"),
    (1, "summary"),
    (1, "body"),
    (1, "author"),
    (1, "opts"),))

# Create a diff for a commit in mbox format for sending via email.
# The commit must not be a merge commit.
#
# @param out buffer to store the e-mail patch in
# @param commit commit to create a patch for
# @param opts email creation options
#
git_email_create_from_commit = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_commit),
    ct.POINTER(git_email_create_options))(
    ("git_email_create_from_commit", dll), (
    (1, "out"),
    (1, "commit"),
    (1, "opts"),))

# GIT_END_DECL
