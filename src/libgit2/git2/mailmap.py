# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .types  import git_repository
from .types  import git_signature
from .types  import git_mailmap

# @file git2/mailmap.h
# @brief Mailmap parsing routines
# @defgroup git_mailmap Git mailmap routines
# @ingroup Git

# GIT_BEGIN_DECL

# Allocate a new mailmap object.
#
# This object is empty, so you'll have to add a mailmap file before you can do
# anything with it. The mailmap must be freed with 'git_mailmap_free'.
#
# @param out pointer to store the new mailmap
# @return 0 on success, or an error code
#
git_mailmap_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_mailmap)))(
    ("git_mailmap_new", dll), (
    (1, "out"),))

# Free the mailmap and its associated memory.
#
# @param mm the mailmap to free
#
git_mailmap_free = CFUNC(None,
    ct.POINTER(git_mailmap))(
    ("git_mailmap_free", dll), (
    (1, "mm"),))

# Add a single entry to the given mailmap object. If the entry already exists,
# it will be replaced with the new entry.
#
# @param mm mailmap to add the entry to
# @param real_name the real name to use, or NULL
# @param real_email the real email to use, or NULL
# @param replace_name the name to replace, or NULL
# @param replace_email the email to replace
# @return 0 on success, or an error code
#
git_mailmap_add_entry = CFUNC(ct.c_int,
    ct.POINTER(git_mailmap),
    ct.c_char_p,
    ct.c_char_p,
    ct.c_char_p,
    ct.c_char_p)(
    ("git_mailmap_add_entry", dll), (
    (1, "mm"),
    (1, "real_name"),
    (1, "real_email"),
    (1, "replace_name"),
    (1, "replace_email"),))

# Create a new mailmap instance containing a single mailmap file
#
# @param out pointer to store the new mailmap
# @param buf buffer to parse the mailmap from
# @param len the length of the input buffer
# @return 0 on success, or an error code
#
git_mailmap_from_buffer = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_mailmap)),
    git_buffer_t,
    ct.c_size_t)(
    ("git_mailmap_from_buffer", dll), (
    (1, "out"),
    (1, "buf"),
    (1, "len"),))

# Create a new mailmap instance from a repository, loading mailmap files based
# on the repository's configuration.
#
# Mailmaps are loaded in the following order:
#  1. '.mailmap' in the root of the repository's working directory, if present.
#  2. The blob object identified by the 'mailmap.blob' config entry, if set.
#     [NOTE: 'mailmap.blob' defaults to 'HEAD:.mailmap' in bare repositories]
#  3. The path in the 'mailmap.file' config entry, if set.
#
# @param out pointer to store the new mailmap
# @param repo repository to load mailmap information from
# @return 0 on success, or an error code
#
git_mailmap_from_repository = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_mailmap)),
    ct.POINTER(git_repository))(
    ("git_mailmap_from_repository", dll), (
    (1, "out"),
    (1, "repo"),))

# Resolve a name and email to the corresponding real name and email.
#
# The lifetime of the strings are tied to `mm`, `name`, and `email` parameters.
#
# @param real_name pointer to store the real name
# @param real_email pointer to store the real email
# @param mm the mailmap to perform a lookup with (may be NULL)
# @param name the name to look up
# @param email the email to look up
# @return 0 on success, or an error code
#
git_mailmap_resolve = CFUNC(ct.c_int,
    ct.POINTER(ct.c_char_p),
    ct.POINTER(ct.c_char_p),
    ct.POINTER(git_mailmap),
    ct.c_char_p,
    ct.c_char_p)(
    ("git_mailmap_resolve", dll), (
    (1, "real_name"),
    (1, "real_email"),
    (1, "mm"),
    (1, "name"),
    (1, "email"),))

# Resolve a signature to use real names and emails with a mailmap.
#
# Call `git_signature_free()` to free the data.
#
# @param out new signature
# @param mm mailmap to resolve with
# @param sig signature to resolve
# @return 0 or an error code
#
git_mailmap_resolve_signature = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_signature)),
    ct.POINTER(git_mailmap),
    ct.POINTER(git_signature))(
    ("git_mailmap_resolve_signature", dll), (
    (1, "out"),
    (1, "mm"),
    (1, "sig"),))

# GIT_END_DECL
