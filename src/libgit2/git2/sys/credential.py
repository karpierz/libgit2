# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common     import *  # noqa
from ..credential import git_credential_t
from ..credential import git_credential_ssh_interactive_cb
from ..credential import git_credential_sign_cb

# @file git2/sys/cred.h
# @brief Git credentials low-level implementation
# @defgroup git_credential Git credentials low-level implementation
# @ingroup Git

# GIT_BEGIN_DECL

# The base structure for all credential types
#
class git_credential(ct.Structure): pass
git_credential._fields_ = [
    ("credtype", git_credential_t),  # A type of credential
    # The deallocator for this type of credentials
    ("free",     GIT_CALLBACK(None,
                     ct.POINTER(git_credential))),  # cred
]

# A plaintext username and password
class git_credential_userpass_plaintext(ct.Structure):
    _fields_ = [
    ("parent",   git_credential),  # The parent credential
    ("username", ct.c_char_p),     # The username to authenticate as
    ("password", ct.c_char_p),     # The password to use
]

# Username-only credential information
class git_credential_username(ct.Structure):
    _fields_ = [
    ("parent",   git_credential),  # The parent credential
    ("username", (char * 1)),      # The username to authenticate as
]

# A ssh key from disk
#
class git_credential_ssh_key(ct.Structure):
    _fields_ = [
    ("parent",     git_credential),  # The parent credential
    ("username",   ct.c_char_p),     # The username to authenticate as
    ("publickey",  ct.c_char_p),     # The path to a public key
    ("privatekey", ct.c_char_p),     # The path to a private key
    ("passphrase", ct.c_char_p),     # Passphrase to decrypt the private key
                                     # TODO: ??? maybe ct.POINTER(ct.c_char) ?
]

# Keyboard-interactive based ssh authentication
#
class git_credential_ssh_interactive(ct.Structure):
    _fields_ = [
    ("parent",          git_credential),  # The parent credential
    ("username",        ct.c_char_p),     # The username to authenticate as
    # Callback used for authentication.
    ("prompt_callback", git_credential_ssh_interactive_cb),
    ("payload",         ct.c_void_p),     # Payload passed to prompt_callback
]

# A key with a custom signature function
#
class git_credential_ssh_custom(ct.Structure):
    _fields_ = [
    ("parent",        git_credential),  # The parent credential
    ("username",      ct.c_char_p),     # The username to authenticate as
    ("publickey",     git_buffer_t),    # The public key data
    ("publickey_len", ct.c_size_t),     # Length of the public key
    # Callback used to sign the data.
    ("sign_callback", git_credential_sign_cb),
    ("payload",       ct.c_void_p),     # Payload passed to prompt_callback
]

# GIT_END_DECL
