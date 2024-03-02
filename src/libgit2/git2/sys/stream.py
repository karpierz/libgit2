# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa
from ..types  import git_cert
from ..proxy  import git_proxy_options

# GIT_BEGIN_DECL

GIT_STREAM_VERSION = 1

# Every stream must have this struct as its first element, so the
# API can talk to it. You'd define your stream as
#
#     class my_stream(ct.Structure):
#         _fields_ = [
#         ("parent", git_stream),
#         ...
#     ]
#
# and fill the functions
#
class git_stream(ct.Structure): pass
git_stream._fields_ = [
    ("version", ct.c_int),

    ("encrypted", ct.c_int, 1),

    ("proxy_support", ct.c_int, 1),

    # Timeout for read and write operations; can be set to `0` to
    # block indefinitely.
    #
    ("timeout", ct.c_int),

    # Timeout to connect to the remote server; can be set to `0`
    # to use the system defaults. This can be shorter than the
    # system default - often 75 seconds - but cannot be longer.
    #
    ("connect_timeout", ct.c_int),

    ("connect",     GIT_CALLBACK(ct.c_int,
                        ct.POINTER(git_stream))),  # stream
    ("certificate", GIT_CALLBACK(ct.c_int,
                        ct.POINTER(ct.POINTER(git_cert)),  # cert
                        ct.POINTER(git_stream))),          # stream
    ("set_proxy",   GIT_CALLBACK(ct.c_int,
                        ct.POINTER(git_stream),            # stream
                        ct.POINTER(git_proxy_options))),   # proxy_opts
    ("read",        GIT_CALLBACK(ct.c_ssize_t,
                        ct.POINTER(git_stream),  # stream
                        ct.c_void_p,             # buffer
                        ct.c_size_t)),           # len
    ("write",       GIT_CALLBACK(ct.c_ssize_t,
                        ct.POINTER(git_stream),  # stream
                        git_buffer_t,            # buffer
                        ct.c_size_t,             # len
                        ct.c_int)),              # ???
    ("close",       GIT_CALLBACK(ct.c_int,
                        ct.POINTER(git_stream))),  # stream
    ("free",        GIT_CALLBACK(None,
                        ct.POINTER(git_stream))),  # stream
]

class git_stream_registration(ct.Structure):
    _fields_ = [
    # The `version` field should be set to `GIT_STREAM_VERSION`.
    ("version", ct.c_int),

    # Called to create a new connection to a given host.
    #
    # @param out The created stream
    # @param host The hostname to connect to; may be a hostname or
    #             IP address
    # @param port The port to connect to; may be a port number or
    #             service name
    # @return 0 or an error code
    #
    ("init", GIT_CALLBACK(ct.c_int,
                 ct.POINTER(ct.POINTER(git_stream)),  # out
                 ct.c_char_p,                         # host
                 ct.c_char_p)),                       # port

    # Called to create a new connection on top of the given stream.  If
    # this is a TLS stream, then this function may be used to proxy a
    # TLS stream over an HTTP CONNECT session.  If this is unset, then
    # HTTP CONNECT proxies will not be supported.
    #
    # @param out The created stream
    # @param in An existing stream to add TLS to
    # @param host The hostname that the stream is connected to,
    #             for certificate validation
    # @return 0 or an error code
    #
    ("wrap", GIT_CALLBACK(ct.c_int,
                 ct.POINTER(ct.POINTER(git_stream)),  # out
                 ct.POINTER(git_stream),              # inp
                 ct.c_char_p)),                       # host
]

# The type of stream to register.
#
git_stream_t = ct.c_int
(   # A standard (non-TLS) socket.
    GIT_STREAM_STANDARD,
    # A TLS-encrypted socket.
    GIT_STREAM_TLS,
) = (1, 2)

# Register stream constructors for the library to use
#
# If a registration structure is already set, it will be overwritten.
# Pass `NULL` in order to deregister the current constructor and return
# to the system defaults.
#
# The type parameter may be a bitwise AND of types.
#
# @param type the type or types of stream to register
# @param registration the registration data
# @return 0 or an error code
#
git_stream_register = CFUNC(ct.c_int,
    git_stream_t,
    ct.POINTER(git_stream_registration))(
    ("git_stream_register", dll), (
    (1, "type"),
    (1, "registration"),))

if not defined("GIT_DEPRECATE_HARD"):

    # @name Deprecated TLS Stream Registration Functions
    #
    # These functions are retained for backward compatibility.  The newer
    # versions of these values should be preferred in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    # @deprecated Provide a git_stream_registration to git_stream_register
    # @see git_stream_registration
    #
    git_stream_cb = GIT_CALLBACK(ct.c_int,
        ct.POINTER(ct.POINTER(git_stream)),  # out
        ct.c_char_p,                         # host
        ct.c_char_p)                         # port

    # Register a TLS stream constructor for the library to use.  This stream
    # will not support HTTP CONNECT proxies.  This internally calls
    # `git_stream_register` and is preserved for backward compatibility.
    #
    # This function is deprecated, but there is no plan to remove this
    # function at this time.
    #
    # @deprecated Provide a git_stream_registration to git_stream_register
    # @see git_stream_register
    #
    git_stream_register_tls = CFUNC(ct.c_int,
        git_stream_cb)(
        ("git_stream_register_tls", dll), (
        (1, "ctor"),))

# endif

# GIT_END_DECL
