# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common     import *  # noqa
from .credential import git_credential

# @file git2/credential_helpers.h
# @brief Utility functions for credential management
# @defgroup git_credential_helpers credential management helpers
# @ingroup Git

# GIT_BEGIN_DECL

# Payload for git_credential_userpass_plaintext.
#
class git_credential_userpass_payload(ct.Structure):
    _fields_ = [
    ("username", ct.c_char_p),
    ("password", ct.c_char_p),
]

# Stock callback usable as a git_credential_acquire_cb.  This calls
# git_cred_userpass_plaintext_new unless the protocol has not specified
# `GIT_CREDENTIAL_USERPASS_PLAINTEXT` as an allowed type.
#
# @param out The newly created credential object.
# @param url The resource for which we are demanding a credential.
# @param user_from_url The username that was embedded in a "user\@host"
#                          remote url, or NULL if not included.
# @param allowed_types A bitmask stating which credential types are OK to return.
# @param payload The payload provided when specifying this callback.  (This is
#        interpreted as a `git_credential_userpass_payload*`.)
# @return 0 or an error code.
#
git_credential_userpass = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_credential)),
    ct.c_char_p,
    ct.c_char_p,
    ct.c_uint,
    ct.c_void_p)(
    ("git_credential_userpass", dll), (
    (1, "out"),
    (1, "url"),
    (1, "user_from_url"),
    (1, "allowed_types"),
    (1, "payload"),))

# GIT_END_DECL
