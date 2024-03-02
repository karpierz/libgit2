# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .buffer import git_buf

# @file git2/message.h
# @brief Git message management routines
# @ingroup Git

# GIT_BEGIN_DECL

# Clean up excess whitespace and make sure there is a trailing newline in the message.
#
# Optionally, it can remove lines which start with the comment character.
#
# @param out The user-allocated git_buf which will be filled with the
#     cleaned up message.
#
# @param message The message to be prettified.
#
# @param strip_comments Non-zero to remove comment lines, 0 to leave them in.
#
# @param comment_char Comment character. Lines starting with this character
# are considered to be comments and removed if `strip_comments` is non-zero.
#
# @return 0 or an error code.
#
git_message_prettify = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.c_char_p,
    ct.c_int,
    ct.c_char)(
    ("git_message_prettify", dll), (
    (1, "out"),
    (1, "message"),
    (1, "strip_comments"),
    (1, "comment_char"),))

# Represents a single git message trailer.
#
class git_message_trailer(ct.Structure):
    _fields_ = [
    ("key",   ct.c_char_p),
    ("value", ct.c_char_p),
]

# Represents an array of git message trailers.
#
# Struct members under the private comment are private, subject to change
# and should not be used by callers.
#
class git_message_trailer_array(ct.Structure):
    _fields_ = [
    ("trailers", ct.POINTER(git_message_trailer)),
    ("count",    ct.c_size_t),
    # private
    ("_trailer_block", git_buffer_t),
]

# Parse trailers out of a message, filling the array pointed to by +arr+.
#
# Trailers are key/value pairs in the last paragraph of a message, not
# including any patches or conflicts that may be present.
#
# @param arr A pre-allocated git_message_trailer_array struct to be filled in
#            with any trailers found during parsing.
# @param message The message to be parsed
# @return 0 on success, or non-zero on error.
#
git_message_trailers = CFUNC(ct.c_int,
    ct.POINTER(git_message_trailer_array),
    ct.c_char_p)(
    ("git_message_trailers", dll), (
    (1, "arr"),
    (1, "message"),))

# Clean's up any allocated memory in the git_message_trailer_array filled by
# a call to git_message_trailers.
#
# @param arr The trailer to free.
#
git_message_trailer_array_free = CFUNC(None,
    ct.POINTER(git_message_trailer_array))(
    ("git_message_trailer_array_free", dll), (
    (1, "arr"),))

# GIT_END_DECL
