# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common     import *  # noqa
from ..oid        import git_oid_t
from ..oid        import git_oid
from ..oidarray   import git_oidarray
from ..types      import git_repository
from ..types      import git_cert
from ..types      import git_remote
from ..types      import git_remote_head
from ..remote     import git_remote_connect_options
from ..credential import git_credential
from ..indexer    import git_indexer_progress
from ..transport  import git_transport_cb

# @file git2/sys/transport.h
# @brief Git custom transport registration interfaces and functions
# @defgroup git_transport Git custom transport registration
# @ingroup Git

# GIT_BEGIN_DECL

class git_fetch_negotiation(ct.Structure):
    _fields_ = [
    ("refs",              ct.POINTER(ct.POINTER(git_remote_head))),
    ("refs_len",          ct.c_size_t),
    ("shallow_roots",     ct.POINTER(git_oid)),
    ("shallow_roots_len", ct.c_size_t),
    ("depth",             ct.c_int),
]

class git_transport(ct.Structure): pass
git_transport._fields_ = [
    ("version", ct.c_uint),  # The struct version

    # Connect the transport to the remote repository, using the given
    # direction.
    #
    ("connect", GIT_CALLBACK(ct.c_int,
                    ct.POINTER(git_transport),                 # transport
                    ct.c_char_p,                               # url
                    ct.c_int,                                  # direction
                    ct.POINTER(git_remote_connect_options))),  # connect_opts

    # Resets the connect options for the given transport.  This
    # is useful for updating settings or callbacks for an already
    # connected transport.
    #
    ("set_connect_opts", GIT_CALLBACK(ct.c_int,
                             ct.POINTER(git_transport),                 # transport
                             ct.POINTER(git_remote_connect_options))),  # connect_opts

    # Gets the capabilities for this remote repository.
    #
    # This function may be called after a successful call to
    # `connect()`.
    #
    ("capabilities", GIT_CALLBACK(ct.c_int,
                         ct.POINTER(ct.c_uint),        # capabilities
                         ct.POINTER(git_transport))),  # transport
    *([
    # Gets the object type for the remote repository.
    #
    # This function may be called after a successful call to
    # `connect()`.
    #
    ("oid_type", GIT_CALLBACK(ct.c_int,
                     ct.POINTER(git_oid_t),        # object_type
                     ct.POINTER(git_transport))),  # transport
    ] if defined("GIT_EXPERIMENTAL_SHA256") else []),

    # Get the list of available references in the remote repository.
    #
    # This function may be called after a successful call to
    # `connect()`. The array returned is owned by the transport and
    # must be kept valid until the next call to one of its functions.
    #
    ("ls", GIT_CALLBACK(ct.c_int,
               ct.POINTER(ct.POINTER(ct.POINTER(git_remote_head))),  # out
               ct.POINTER(ct.c_size_t),                              # size
               ct.POINTER(git_transport))),                          # transport

    # Executes the push whose context is in the git_push object.
    ("push", GIT_CALLBACK(ct.c_int,
                 ct.POINTER(git_transport),  # transport
                 ct.POINTER(git_push))),     # push

    # Negotiate a fetch with the remote repository.
    #
    # This function may be called after a successful call to `connect()`,
    # when the direction is GIT_DIRECTION_FETCH. The function performs a
    # negotiation to calculate the `wants` list for the fetch.
    #
    ("negotiate_fetch", GIT_CALLBACK(ct.c_int,
                            ct.POINTER(git_transport),            # transport
                            ct.POINTER(git_repository),           # repo
                            ct.POINTER(git_fetch_negotiation))),  # fetch_data

    # Return the shallow roots of the remote.
    #
    # This function may be called after a successful call to
    # `negotiate_fetch`.
    #
    ("shallow_roots", GIT_CALLBACK(ct.c_int,
                          ct.POINTER(git_oidarray),     # out
                          ct.POINTER(git_transport))),  # transport

    # Start downloading the packfile from the remote repository.
    #
    # This function may be called after a successful call to
    # negotiate_fetch(), when the direction is GIT_DIRECTION_FETCH.
    #
    ("download_pack", GIT_CALLBACK(ct.c_int,
                          ct.POINTER(git_transport),           # transport
                          ct.POINTER(git_repository),          # repo
                          ct.POINTER(git_indexer_progress))),  # stats

    # Checks to see if the transport is connected
    ("is_connected", GIT_CALLBACK(ct.c_int,
                         ct.POINTER(git_transport))),  # transport

    # Cancels any outstanding transport operation
    ("cancel", GIT_CALLBACK(None,
                   ct.POINTER(git_transport))),  # transport

    # Close the connection to the remote repository.
    #
    # This function is the reverse of connect() -- it terminates the
    # connection to the remote end.
    #
    ("close", GIT_CALLBACK(ct.c_int,
                  ct.POINTER(git_transport))),  # transport

    # Frees/destructs the git_transport object.
    ("free", GIT_CALLBACK(None,
                 ct.POINTER(git_transport))),  # transport
]

GIT_TRANSPORT_VERSION = 1
#define GIT_TRANSPORT_INIT = { GIT_TRANSPORT_VERSION }

# Initializes a `git_transport` with default values. Equivalent to
# creating an instance with GIT_TRANSPORT_INIT.
#
# @param opts the `git_transport` struct to initialize
# @param version Version of struct; pass `GIT_TRANSPORT_VERSION`
# @return Zero on success; -1 on failure.
#
git_transport_init = CFUNC(ct.c_int,
    ct.POINTER(git_transport),
    ct.c_uint)(
    ("git_transport_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Function to use to create a transport from a URL. The transport database
# is scanned to find a transport that implements the scheme of the URI (i.e.
# git:// or http://) and a transport object is returned to the caller.
#
# @param out The newly created transport (out)
# @param owner The git_remote which will own this transport
# @param url The URL to connect to
# @return 0 or an error code
#
git_transport_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_transport)),
    ct.POINTER(git_remote),
    ct.c_char_p)(
    ("git_transport_new", dll), (
    (1, "out"),
    (1, "owner"),
    (1, "url"),))

# Create an ssh transport with custom git command paths
#
# This is a factory function suitable for setting as the transport
# callback in a remote (or for a clone in the options).
#
# The payload argument must be a strarray pointer with the paths for
# the `git-upload-pack` and `git-receive-pack` at index 0 and 1.
#
# @param out the resulting transport
# @param owner the owning remote
# @param payload a strarray with the paths
# @return 0 or an error code
#
git_transport_ssh_with_paths = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_transport)),
    ct.POINTER(git_remote),
    ct.c_void_p)(
    ("git_transport_ssh_with_paths", dll), (
    (1, "out"),
    (1, "owner"),
    (1, "payload"),))

# Add a custom transport definition, to be used in addition to the built-in
# set of transports that come with libgit2.
#
# The caller is responsible for synchronizing calls to git_transport_register
# and git_transport_unregister with other calls to the library that
# instantiate transports.
#
# @param prefix The scheme (ending in "://") to match, i.e. "git://"
# @param cb The callback used to create an instance of the transport
# @param param A fixed parameter to pass to cb at creation time
# @return 0 or an error code
#
git_transport_register = CFUNC(ct.c_int,
    ct.c_char_p,
    git_transport_cb,
    ct.c_void_p)(
    ("git_transport_register", dll), (
    (1, "prefix"),
    (1, "cb"),
    (1, "param"),))

# Unregister a custom transport definition which was previously registered
# with git_transport_register.
#
# The caller is responsible for synchronizing calls to git_transport_register
# and git_transport_unregister with other calls to the library that
# instantiate transports.
#
# @param prefix From the previous call to git_transport_register
# @return 0 or an error code
#
git_transport_unregister = CFUNC(ct.c_int,
    ct.c_char_p)(
    ("git_transport_unregister", dll), (
    (1, "prefix"),))

# Transports which come with libgit2 (match git_transport_cb). The expected
# value for "param" is listed in-line below.

# Create an instance of the dummy transport.
#
# @param out The newly created transport (out)
# @param owner The git_remote which will own this transport
# @param payload You must pass NULL for this parameter.
# @return 0 or an error code
#
git_transport_dummy = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_transport)),
    ct.POINTER(git_remote),
    ct.c_void_p)(  # NULL #
    ("git_transport_dummy", dll), (
    (1, "out"),
    (1, "owner"),
    (1, "payload"),))

# Create an instance of the local transport.
#
# @param out The newly created transport (out)
# @param owner The git_remote which will own this transport
# @param payload You must pass NULL for this parameter.
# @return 0 or an error code
#
git_transport_local = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_transport)),
    ct.POINTER(git_remote),
    ct.c_void_p)(  # NULL #
    ("git_transport_local", dll), (
    (1, "out"),
    (1, "owner"),
    (1, "payload"),))

# Create an instance of the smart transport.
#
# @param out The newly created transport (out)
# @param owner The git_remote which will own this transport
# @param payload A pointer to a git_smart_subtransport_definition
# @return 0 or an error code
#
git_transport_smart = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_transport)),
    ct.POINTER(git_remote),
    ct.c_void_p)(  # ct.POINTER(git_smart_subtransport_definition) #
    ("git_transport_smart", dll), (
    (1, "out"),
    (1, "owner"),
    (1, "payload"),))

# Call the certificate check for this transport.
#
# @param transport a smart transport
# @param cert the certificate to pass to the caller
# @param valid whether we believe the certificate is valid
# @param hostname the hostname we connected to
# @return the return value of the callback: 0 for no error, GIT_PASSTHROUGH
#         to indicate that there is no callback registered (or the callback
#         refused to validate the certificate and callers should behave as
#         if no callback was set), or < 0 for an error
#
git_transport_smart_certificate_check = CFUNC(ct.c_int,
    ct.POINTER(git_transport),
    ct.POINTER(git_cert),
    ct.c_int,
    ct.c_char_p)(
    ("git_transport_smart_certificate_check", dll), (
    (1, "transport"),
    (1, "cert"),
    (1, "valid"),
    (1, "hostname"),))

# Call the credentials callback for this transport
#
# @param out the pointer where the creds are to be stored
# @param transport a smart transport
# @param user the user we saw on the url (if any)
# @param methods available methods for authentication
# @return the return value of the callback: 0 for no error, GIT_PASSTHROUGH
#         to indicate that there is no callback registered (or the callback
#         refused to provide credentials and callers should behave as if no
#         callback was set), or < 0 for an error
#
git_transport_smart_credentials = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_credential)),
    ct.POINTER(git_transport),
    ct.c_char_p,
    ct.c_int)(
    ("git_transport_smart_credentials", dll), (
    (1, "out"),
    (1, "transport"),
    (1, "user"),
    (1, "methods"),))

# Get a copy of the remote connect options
#
# All data is copied and must be freed by the caller by calling
# `git_remote_connect_options_dispose`.
#
# @param out options struct to fill
# @param transport the transport to extract the data from.
#
git_transport_remote_connect_options = CFUNC(ct.c_int,
    ct.POINTER(git_remote_connect_options),
    ct.POINTER(git_transport))(
    ("git_transport_remote_connect_options", dll), (
    (1, "out"),
    (1, "transport"),))

# *** End of base transport interface ***
# *** Begin interface for subtransports for the smart transport ***
#

# Actions that the smart transport can ask a subtransport to perform
#
git_smart_service_t = ct.c_int
(   GIT_SERVICE_UPLOADPACK_LS,
    GIT_SERVICE_UPLOADPACK,
    GIT_SERVICE_RECEIVEPACK_LS,
    GIT_SERVICE_RECEIVEPACK,
) = (1, 2, 3, 4)

class git_smart_subtransport(ct.Structure): pass  # Forward definition

# A stream used by the smart transport to read and write data
# from a subtransport.
#
# This provides a customization point in case you need to
# support some other communication method.
#
class git_smart_subtransport_stream(ct.Structure): pass
git_smart_subtransport_stream._fields_ = [
    ("subtransport", ct.POINTER(git_smart_subtransport)),  # The owning subtransport

    # Read available data from the stream.
    #
    # The implementation may read less than requested.
    #
    ("read", GIT_CALLBACK(ct.c_int,
                  ct.POINTER(git_smart_subtransport_stream),  # stream
                  git_buffer_t,                               # buffer
                  ct.c_size_t,                                # buf_size
                  ct.POINTER(ct.c_size_t))),                  # bytes_read

    # Write data to the stream
    #
    # The implementation must write all data or return an error.
    #
    ("write", GIT_CALLBACK(ct.c_int,
                  ct.POINTER(git_smart_subtransport_stream),  # stream
                  git_buffer_t,                               # buffer
                  ct.c_size_t)),                              # len

    # Free the stream
    ("free", GIT_CALLBACK(None,
                  ct.POINTER(git_smart_subtransport_stream))),  # stream
]

# An implementation of a subtransport which carries data for the
# smart transport
#
git_smart_subtransport._fields_ = [

    # Setup a subtransport stream for the requested action.
    #
    ("action", GIT_CALLBACK(ct.c_int,
                   ct.POINTER(ct.POINTER(git_smart_subtransport_stream)),  # out
                   ct.POINTER(git_smart_subtransport),                     # transport
                   ct.c_char_p,                                            # url
                   git_smart_service_t)),                                  # action

    # Close the subtransport.
    #
    # Subtransports are guaranteed a call to close() between
    # calls to action(), except for the following two "natural" progressions
    # of actions against a constant URL:
    #
    # - UPLOADPACK_LS -> UPLOADPACK
    # - RECEIVEPACK_LS -> RECEIVEPACK
    #
    ("close", GIT_CALLBACK(ct.c_int,
                  ct.POINTER(git_smart_subtransport))),  # transport

    # Free the subtransport
    ("free",  GIT_CALLBACK(None,
                  ct.POINTER(git_smart_subtransport))),  # transport
]

# A function which creates a new subtransport for the smart transport
git_smart_subtransport_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(ct.POINTER(git_smart_subtransport)),  # out
    ct.POINTER(git_transport),                       # owner
    ct.c_void_p)                                     # param

# Definition for a "subtransport"
#
# The smart transport knows how to speak the git protocol, but it has no
# knowledge of how to establish a connection between it and another endpoint,
# or how to move data back and forth. For this, a subtransport interface is
# declared, and the smart transport delegates this work to the subtransports.
#
# Three subtransports are provided by libgit2: ssh, git, http(s).
#
# Subtransports can either be RPC = 0 (persistent connection) or RPC = 1
# (request/response). The smart transport handles the differences in its own
# logic. The git subtransport is RPC = 0, while http is RPC = 1.
#
class git_smart_subtransport_definition(ct.Structure):
    _fields_ = [
    # The function to use to create the git_smart_subtransport
    ("callback", git_smart_subtransport_cb),

    # True if the protocol is stateless; false otherwise. For example,
    # http:// is stateless, but git:// is not.
    #
    ("rpc", ct.c_uint),

    # User-specified parameter passed to the callback
    ("param", ct.c_void_p),
]

# Smart transport subtransports that come with libgit2

# Create an instance of the http subtransport.
#
# This subtransport also supports https.
#
# @param out The newly created subtransport
# @param owner The smart transport to own this subtransport
# @return 0 or an error code
#
git_smart_subtransport_http = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_smart_subtransport)),
    ct.POINTER(git_transport),
    ct.c_void_p)(
    ("git_smart_subtransport_http", dll), (
    (1, "out"),
    (1, "owner"),
    (1, "param"),))

# Create an instance of the git subtransport.
#
# @param out The newly created subtransport
# @param owner The smart transport to own this subtransport
# @return 0 or an error code
#
git_smart_subtransport_git = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_smart_subtransport)),
    ct.POINTER(git_transport),
    ct.c_void_p)(
    ("git_smart_subtransport_git", dll), (
    (1, "out"),
    (1, "owner"),
    (1, "param"),))

# Create an instance of the ssh subtransport.
#
# @param out The newly created subtransport
# @param owner The smart transport to own this subtransport
# @return 0 or an error code
#
git_smart_subtransport_ssh = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_smart_subtransport)),
    ct.POINTER(git_transport),
    ct.c_void_p)(
    ("git_smart_subtransport_ssh", dll), (
    (1, "out"),
    (1, "owner"),
    (1, "param"),))

# GIT_END_DECL
