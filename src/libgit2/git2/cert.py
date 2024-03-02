# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa

# @file git2/cert.h
# @brief Git certificate objects
# @defgroup git_cert Certificate objects
# @ingroup Git

# GIT_BEGIN_DECL

# Type of host certificate structure that is passed to the check callback
#
git_cert_t = ct.c_int
(   # No information about the certificate is available. This may
    # happen when using curl.
    GIT_CERT_NONE,
    # The `data` argument to the callback will be a pointer to
    # the DER-encoded data.
    GIT_CERT_X509,
    # The `data` argument to the callback will be a pointer to a
    # `git_cert_hostkey` structure.
    GIT_CERT_HOSTKEY_LIBSSH2,
    # The `data` argument to the callback will be a pointer to a
    # `git_strarray` with `name:content` strings containing
    # information about the certificate. This is used when using
    # curl.
    GIT_CERT_STRARRAY,
) = range(0, 4)

# Parent type for `git_cert_hostkey` and `git_cert_x509`.
#
class git_cert(ct.Structure):
    _fields_ = [
    # Type of certificate. A `GIT_CERT_` value.
    ("cert_type", git_cert_t),
]

# Callback for the user's custom certificate checks.
#
# @param cert The host certificate
# @param valid Whether the libgit2 checks (OpenSSL or WinHTTP) think
# this certificate is valid
# @param host Hostname of the host libgit2 connected to
# @param payload Payload provided by the caller
# @return 0 to proceed with the connection, < 0 to fail the connection
#         or > 0 to indicate that the callback refused to act and that
#         the existing validity determination should be honored
#
git_transport_certificate_check_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_cert),  # cert
    ct.c_int,              # valid
    ct.c_char_p,           # host
    ct.c_void_p)           # payload

# Type of SSH host fingerprint
#
git_cert_ssh_t = ct.c_int
(   # MD5 is available
    GIT_CERT_SSH_MD5,
    # SHA-1 is available
    GIT_CERT_SSH_SHA1,
    # SHA-256 is available
    GIT_CERT_SSH_SHA256,
    # Raw hostkey is available
    GIT_CERT_SSH_RAW,
) = (1 << 0, 1 << 1, 1 << 2, 1 << 3)

git_cert_ssh_raw_type_t = ct.c_int
(   # The raw key is of an unknown type.
    GIT_CERT_SSH_RAW_TYPE_UNKNOWN,
    # The raw key is an RSA key.
    GIT_CERT_SSH_RAW_TYPE_RSA,
    # The raw key is a DSS key.
    GIT_CERT_SSH_RAW_TYPE_DSS,
    # The raw key is a ECDSA 256 key.
    GIT_CERT_SSH_RAW_TYPE_KEY_ECDSA_256,
    # The raw key is a ECDSA 384 key.
    GIT_CERT_SSH_RAW_TYPE_KEY_ECDSA_384,
    # The raw key is a ECDSA 521 key.
    GIT_CERT_SSH_RAW_TYPE_KEY_ECDSA_521,
    # The raw key is a ED25519 key.
    GIT_CERT_SSH_RAW_TYPE_KEY_ED25519,
) = (0, 1, 2, 3, 4, 5, 6)

# Hostkey information taken from libssh2
#
class git_cert_hostkey(ct.Structure):
    _fields_ = [
    ("parent", git_cert),  # The parent cert

    # A bitmask containing the available fields.
    ("type", git_cert_ssh_t),

    # Hostkey hash. If `type` has `GIT_CERT_SSH_MD5` set, this will
    # have the MD5 hash of the hostkey.
    ("hash_md5", (ct.c_ubyte * 16)),

    # Hostkey hash. If `type` has `GIT_CERT_SSH_SHA1` set, this will
    # have the SHA-1 hash of the hostkey.
    ("hash_sha1", (ct.c_ubyte * 20)),

    # Hostkey hash. If `type` has `GIT_CERT_SSH_SHA256` set, this will
    # have the SHA-256 hash of the hostkey.
    ("hash_sha256", (ct.c_ubyte * 32)),

    # Raw hostkey type. If `type` has `GIT_CERT_SSH_RAW` set, this will
    # have the type of the raw hostkey.
    ("raw_type", git_cert_ssh_raw_type_t),

    # Pointer to the raw hostkey. If `type` has `GIT_CERT_SSH_RAW` set,
    # this will have the raw contents of the hostkey.
    ("hostkey", ct.c_char_p),

    # Raw hostkey length. If `type` has `GIT_CERT_SSH_RAW` set, this will
    # have the length of the raw contents of the hostkey.
    ("hostkey_len", ct.c_size_t),
]

# X.509 certificate information
#
class git_cert_x509(ct.Structure):
    _fields_ = [
    ("parent", git_cert),  # The parent cert

    # Pointer to the X.509 certificate data
    ("data", ct.c_void_p),

    # Length of the memory block pointed to by `data`.
    ("len", ct.c_size_t),
]

# GIT_END_DECL
