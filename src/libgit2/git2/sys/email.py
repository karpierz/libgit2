# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa
from ..oid    import git_oid
from ..buffer import git_buf
from ..diff   import git_diff
from ..types  import git_signature
from ..email  import git_email_create_options

# @file git2/sys/email.h
# @brief Advanced git email creation routines
# @defgroup git_email Advanced git email creation routines
# @ingroup Git

# GIT_BEGIN_DECL

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

# GIT_END_DECL
