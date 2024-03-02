# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa

# GIT_BEGIN_DECL

# Similarity signature of arbitrary text content based on line hashes
#
class git_hashsig(ct.Structure): pass

# Options for hashsig computation
#
# The options GIT_HASHSIG_NORMAL, GIT_HASHSIG_IGNORE_WHITESPACE,
# GIT_HASHSIG_SMART_WHITESPACE are exclusive and should not be combined.
#
git_hashsig_option_t = ct.c_int
(
    # Use all data
    GIT_HASHSIG_NORMAL,

    # Ignore whitespace
    GIT_HASHSIG_IGNORE_WHITESPACE,

    # Ignore \r and all space after \n
    GIT_HASHSIG_SMART_WHITESPACE,

    # Allow hashing of small files
    GIT_HASHSIG_ALLOW_SMALL_FILES,

) = (0, 1 << 0, 1 << 1, 1 << 2)

# Compute a similarity signature for a text buffer
#
# If you have passed the option GIT_HASHSIG_IGNORE_WHITESPACE, then the
# whitespace will be removed from the buffer while it is being processed,
# modifying the buffer in place. Sorry about that!
#
# @param out The computed similarity signature.
# @param buf The input buffer.
# @param buflen The input buffer size.
# @param opts The signature computation options (see above).
# @return 0 on success, GIT_EBUFS if the buffer doesn't contain enough data to
# compute a valid signature (unless GIT_HASHSIG_ALLOW_SMALL_FILES is set), or
# error code.
#
git_hashsig_create = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_hashsig)),
    git_buffer_t,
    ct.c_size_t,
    git_hashsig_option_t)(
    ("git_hashsig_create", dll), (
    (1, "out"),
    (1, "buf"),
    (1, "buflen"),
    (1, "opts"),))

# Compute a similarity signature for a text file
#
# This walks through the file, only loading a maximum of 4K of file data at
# a time. Otherwise, it acts just like `git_hashsig_create`.
#
# @param out The computed similarity signature.
# @param path The path to the input file.
# @param opts The signature computation options (see above).
# @return 0 on success, GIT_EBUFS if the buffer doesn't contain enough data to
# compute a valid signature (unless GIT_HASHSIG_ALLOW_SMALL_FILES is set), or
# error code.
#
git_hashsig_create_fromfile = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_hashsig)),
    ct.c_char_p,
    git_hashsig_option_t)(
    ("git_hashsig_create_fromfile", dll), (
    (1, "out"),
    (1, "path"),
    (1, "opts"),))

# Release memory for a content similarity signature
#
# @param sig The similarity signature to free.
#
git_hashsig_free = CFUNC(None,
    ct.POINTER(git_hashsig))(
    ("git_hashsig_free", dll), (
    (1, "sig"),))

# Measure similarity score between two similarity signatures
#
# @param a The first similarity signature to compare.
# @param b The second similarity signature to compare.
# @return [0 to 100] on success as the similarity score, or error code.
#
git_hashsig_compare = CFUNC(ct.c_int,
    ct.POINTER(git_hashsig),
    ct.POINTER(git_hashsig))(
    ("git_hashsig_compare", dll), (
    (1, "a"),
    (1, "b"),))

# GIT_END_DECL
