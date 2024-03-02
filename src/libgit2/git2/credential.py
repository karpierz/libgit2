# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa

# @file git2/credential.h
# @brief Git authentication & credential management
# @defgroup git_credential Authentication & credential management
# @ingroup Git

# GIT_BEGIN_DECL

# Supported credential types
#
# This represents the various types of authentication methods supported by
# the library.
#
git_credential_t = ct.c_int
(
    # A vanilla user/password request
    # @see git_credential_userpass_plaintext_new
    #
    GIT_CREDENTIAL_USERPASS_PLAINTEXT,

    # An SSH key-based authentication request
    # @see git_credential_ssh_key_new
    #
    GIT_CREDENTIAL_SSH_KEY,

    # An SSH key-based authentication request, with a custom signature
    # @see git_credential_ssh_custom_new
    #
    GIT_CREDENTIAL_SSH_CUSTOM,

    # An NTLM/Negotiate-based authentication request.
    # @see git_credential_default
    #
    GIT_CREDENTIAL_DEFAULT,

    # An SSH interactive authentication request
    # @see git_credential_ssh_interactive_new
    #
    GIT_CREDENTIAL_SSH_INTERACTIVE,

    # Username-only authentication request
    #
    # Used as a pre-authentication step if the underlying transport
    # (eg. SSH, with no username in its URL) does not know which username
    # to use.
    #
    # @see git_credential_username_new
    #
    GIT_CREDENTIAL_USERNAME,

    # An SSH key-based authentication request
    #
    # Allows credentials to be read from memory instead of files.
    # Note that because of differences in crypto backend support, it might
    # not be functional.
    #
    # @see git_credential_ssh_key_memory_new
    #
    GIT_CREDENTIAL_SSH_MEMORY,

) = (1 << 0, 1 << 1, 1 << 2, 1 << 3, 1 << 4, 1 << 5, 1 << 6)

# The base structure for all credential types
#
class git_credential(ct.Structure): pass
# from .sys.credential import git_credential

class git_credential_userpass_plaintext(ct.Structure): pass
# from .sys.credential import git_credential_userpass_plaintext

# Username-only credential information
class git_credential_username(ct.Structure): pass
# from .sys.credential import git_credential_username

# A key for NTLM/Kerberos "default" credentials
git_credential_default = git_credential

# A ssh key from disk
#
class git_credential_ssh_key(ct.Structure): pass
# from .sys.credential import git_credential_ssh_key

# Keyboard-interactive based ssh authentication
#
class git_credential_ssh_interactive(ct.Structure): pass
# from .sys.credential import git_credential_ssh_interactive

# A key with a custom signature function
#
class git_credential_ssh_custom(ct.Structure): pass
# from .sys.credential import git_credential_ssh_custom

# Credential acquisition callback.
#
# This callback is usually involved any time another system might need
# authentication. As such, you are expected to provide a valid
# git_credential object back, depending on allowed_types (a
# git_credential_t bitmask).
#
# Note that most authentication details are your responsibility - this
# callback will be called until the authentication succeeds, or you report
# an error. As such, it's easy to get in a loop if you fail to stop providing
# the same incorrect credentials.
#
# @param out The newly created credential object.
# @param url The resource for which we are demanding a credential.
# @param username_from_url The username that was embedded in a "user\@host"
#                          remote url, or NULL if not included.
# @param allowed_types A bitmask stating which credential types are OK to return.
# @param payload The payload provided when specifying this callback.
# @return 0 for success, < 0 to indicate an error, > 0 to indicate
#       no credential was acquired
#
git_credential_acquire_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(ct.POINTER(git_credential)),  # out
    ct.c_char_p,                             # url
    ct.c_char_p,                             # username_from_url
    ct.c_uint,                               # allowed_types
    ct.c_void_p)                             # payload

# Free a credential.
#
# This is only necessary if you own the object; that is, if you are a
# transport.
#
# @param cred the object to free
#
git_credential_free = CFUNC(None,
    ct.POINTER(git_credential))(
    ("git_credential_free", dll), (
    (1, "cred"),))

# Check whether a credential object contains username information.
#
# @param cred object to check
# @return 1 if the credential object has non-NULL username, 0 otherwise
#
git_credential_has_username = CFUNC(ct.c_int,
    ct.POINTER(git_credential))(
    ("git_credential_has_username", dll), (
    (1, "cred"),))

# Return the username associated with a credential object.
#
# @param cred object to check
# @return the credential username, or NULL if not applicable
#
git_credential_get_username = CFUNC(ct.c_char_p,
    ct.POINTER(git_credential))(
    ("git_credential_get_username", dll), (
    (1, "cred"),))

# Create a new plain-text username and password credential object.
# The supplied credential parameter will be internally duplicated.
#
# @param out The newly created credential object.
# @param username The username of the credential.
# @param password The password of the credential.
# @return 0 for success or an error code for failure
#
git_credential_userpass_plaintext_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_credential)),
    ct.c_char_p,
    ct.c_char_p)(
    ("git_credential_userpass_plaintext_new", dll), (
    (1, "out"),
    (1, "username"),
    (1, "password"),))

# Create a "default" credential usable for Negotiate mechanisms like NTLM
# or Kerberos authentication.
#
# @param out The newly created credential object.
# @return 0 for success or an error code for failure
#
git_credential_default_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_credential)))(
    ("git_credential_default_new", dll), (
    (1, "out"),))

# Create a credential to specify a username.
#
# This is used with ssh authentication to query for the username if
# none is specified in the url.
#
# @param out The newly created credential object.
# @param username The username to authenticate with
# @return 0 for success or an error code for failure
#
git_credential_username_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_credential)),
    ct.c_char_p)(
    ("git_credential_username_new", dll), (
    (1, "out"),
    (1, "username"),))

# Create a new passphrase-protected ssh key credential object.
# The supplied credential parameter will be internally duplicated.
#
# @param out The newly created credential object.
# @param username username to use to authenticate
# @param publickey The path to the public key of the credential.
# @param privatekey The path to the private key of the credential.
# @param passphrase The passphrase of the credential.
# @return 0 for success or an error code for failure
#
git_credential_ssh_key_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_credential)),
    ct.c_char_p,
    ct.c_char_p,
    ct.c_char_p,
    ct.c_char_p)(  # TODO: ??? maybe ct.POINTER(ct.c_char) ?
    ("git_credential_ssh_key_new", dll), (
    (1, "out"),
    (1, "username"),
    (1, "publickey"),
    (1, "privatekey"),
    (1, "passphrase"),))

# Create a new ssh key credential object reading the keys from memory.
#
# @param out The newly created credential object.
# @param username username to use to authenticate.
# @param publickey The public key of the credential.
# @param privatekey The private key of the credential.
# @param passphrase The passphrase of the credential.
# @return 0 for success or an error code for failure
#
git_credential_ssh_key_memory_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_credential)),
    ct.c_char_p,
    ct.c_char_p,   # TODO: ??? maybe ct.POINTER(ct.c_char) ?
    ct.c_char_p,   # TODO: ??? maybe ct.POINTER(ct.c_char) ?
    ct.c_char_p)(  # TODO: ??? maybe ct.POINTER(ct.c_char) ?
    ("git_credential_ssh_key_memory_new", dll), (
    (1, "out"),
    (1, "username"),
    (1, "publickey"),
    (1, "privatekey"),
    (1, "passphrase"),))

# If the user hasn't included libssh2.h before git2.h, we need to
# define a few types for the callback signatures.
#
# TODO: !!!
if not defined("LIBSSH2_VERSION"):
    class _LIBSSH2_SESSION(ct.Structure): pass
    class _LIBSSH2_USERAUTH_KBDINT_PROMPT(ct.Structure): pass
    class _LIBSSH2_USERAUTH_KBDINT_RESPONSE(ct.Structure): pass
    LIBSSH2_SESSION                  = _LIBSSH2_SESSION
    LIBSSH2_USERAUTH_KBDINT_PROMPT   = _LIBSSH2_USERAUTH_KBDINT_PROMPT
    LIBSSH2_USERAUTH_KBDINT_RESPONSE = _LIBSSH2_USERAUTH_KBDINT_RESPONSE
else:
    class LIBSSH2_SESSION(ct.Structure): pass
    class LIBSSH2_USERAUTH_KBDINT_PROMPT(ct.Structure): pass
    class LIBSSH2_USERAUTH_KBDINT_RESPONSE(ct.Structure): pass
# endif

git_credential_ssh_interactive_cb = GIT_CALLBACK(None,
    git_buffer_t,                                  # name
    ct.c_int,                                      # name_len
    git_buffer_t,                                  # instruction
    ct.c_int,                                      # instruction_len
    ct.c_int,                                      # num_prompts
    ct.POINTER(LIBSSH2_USERAUTH_KBDINT_PROMPT),    # prompts
    ct.POINTER(LIBSSH2_USERAUTH_KBDINT_RESPONSE),  # responses
    ct.POINTER(ct.c_void_p))                       # abstract

# Create a new ssh keyboard-interactive based credential object.
# The supplied credential parameter will be internally duplicated.
#
# @param out The newly created credential object.
# @param username Username to use to authenticate.
# @param prompt_callback The callback method used for prompts.
# @param payload Additional data to pass to the callback.
# @return 0 for success or an error code for failure.
#
git_credential_ssh_interactive_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_credential)),
    ct.c_char_p,
    git_credential_ssh_interactive_cb,
    ct.c_void_p)(
    ("git_credential_ssh_interactive_new", dll), (
    (1, "out"),
    (1, "username"),
    (1, "prompt_callback"),
    (1, "payload"),))

# Create a new ssh key credential object used for querying an ssh-agent.
# The supplied credential parameter will be internally duplicated.
#
# @param out The newly created credential object.
# @param username username to use to authenticate
# @return 0 for success or an error code for failure
#
git_credential_ssh_key_from_agent = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_credential)),
    ct.c_char_p)(
    ("git_credential_ssh_key_from_agent", dll), (
    (1, "out"),
    (1, "username"),))

git_credential_sign_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(LIBSSH2_SESSION),         # session
    ct.POINTER(ct.POINTER(ct.c_ubyte)),  # sig
    ct.POINTER(ct.c_size_t),             # sig_len
    ct.POINTER(ct.c_ubyte),              # data
    ct.c_size_t,                         # data_len
    ct.POINTER(ct.c_void_p))             # abstract

# Create an ssh key credential with a custom signing function.
#
# This lets you use your own function to sign the challenge.
#
# This function and its credential type is provided for completeness
# and wraps `libssh2_userauth_publickey()`, which is undocumented.
#
# The supplied credential parameter will be internally duplicated.
#
# @param out The newly created credential object.
# @param username username to use to authenticate
# @param publickey The bytes of the public key.
# @param publickey_len The length of the public key in bytes.
# @param sign_callback The callback method to sign the data during the challenge.
# @param payload Additional data to pass to the callback.
# @return 0 for success or an error code for failure
#
git_credential_ssh_custom_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_credential)),
    ct.c_char_p,
    git_buffer_t,
    ct.c_size_t,
    git_credential_sign_cb,
    ct.c_void_p)(
    ("git_credential_ssh_custom_new", dll), (
    (1, "out"),
    (1, "username"),
    (1, "publickey"),
    (1, "publickey_len"),
    (1, "sign_callback"),
    (1, "payload"),))

# GIT_END_DECL
