# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa
from ..oid    import git_oid
from ..types  import git_refdb
from ..types  import git_repository
from ..types  import git_reference
from ..types  import git_reflog
from ..types  import git_signature

# @file git2/refdb_backend.h
# @brief Git custom refs backend functions
# @defgroup git_refdb_backend Git custom refs backend API
# @ingroup Git

# GIT_BEGIN_DECL

# Every backend's iterator must have a pointer to itself as the first
# element, so the API can talk to it. You'd define your iterator as
#
#     class my_iterator(ct.Structure):
#         _fields_ = [
#         ("parent", git_reference_iterator),
#         ...
#     ]
#
# and assign `iter->parent.backend` to your `git_refdb_backend`.
#
class git_reference_iterator(ct.Structure): pass
git_reference_iterator._fields_ = [
    ("db", ct.POINTER(git_refdb)),

    # Return the current reference and advance the iterator.
    #
    ("next",      GIT_CALLBACK(ct.c_int,
                      ct.POINTER(ct.POINTER(git_reference)),  # ref
                      ct.POINTER(git_reference_iterator))),   # iter
    # Return the name of the current reference and advance the iterator
    #
    ("next_name", GIT_CALLBACK(ct.c_int,
                      ct.POINTER(ct.c_char_p),               # ref_name
                      ct.POINTER(git_reference_iterator))),  # iter
    # Free the iterator
    #
    ("free",      GIT_CALLBACK(None,
                      ct.POINTER(git_reference_iterator))),  # iter
]

# An instance for a custom backend
#
class git_refdb_backend(ct.Structure): pass
git_refdb_backend._fields_ = [
    ("version", ct.c_uint),  # The backend API version

    # Queries the refdb backend for the existence of a reference.
    #
    # A refdb implementation must provide this function.
    #
    # @arg exists The implementation shall set this to `0` if a ref does
    #             not exist, otherwise to `1`.
    # @arg ref_name The reference's name that should be checked for
    #               existence.
    # @return `0` on success, a negative error value code.
    #
    ("exists", GIT_CALLBACK(ct.c_int,
                   ct.POINTER(ct.c_int),           # exists
                   ct.POINTER(git_refdb_backend),  # backend
                   ct.c_char_p)),                  # ref_name

    # Queries the refdb backend for a given reference.
    #
    # A refdb implementation must provide this function.
    #
    # @arg out The implementation shall set this to the allocated
    #          reference, if it could be found, otherwise to `NULL`.
    # @arg ref_name The reference's name that should be checked for
    #               existence.
    # @return `0` on success, `GIT_ENOTFOUND` if the reference does
    #         exist, otherwise a negative error code.
    #
    ("lookup", GIT_CALLBACK(ct.c_int,
                   ct.POINTER(ct.POINTER(git_reference)),  # out,
                   ct.POINTER(git_refdb_backend),          # backend,
                   ct.c_char_p)),                          # ref_name

    # Allocate an iterator object for the backend.
    #
    # A refdb implementation must provide this function.
    #
    # @arg out The implementation shall set this to the allocated
    #          reference iterator. A custom structure may be used with an
    #          embedded `git_reference_iterator` structure. Both `next`
    #          and `next_name` functions of `git_reference_iterator` need
    #          to be populated.
    # @arg glob A pattern to filter references by. If given, the iterator
    #           shall only return references that match the glob when
    #           passed to `wildmatch`.
    # @return `0` on success, otherwise a negative error code.
    #
    ("iterator", GIT_CALLBACK(ct.c_int,
                     ct.POINTER(ct.POINTER(git_reference_iterator)),  # iter
                     ct.POINTER(git_refdb_backend),                   # backend
                     ct.c_char_p)),                                   # glob

    # Writes the given reference to the refdb.
    #
    # A refdb implementation must provide this function.
    #
    # @arg ref The reference to persist. May either be a symbolic or
    #          direct reference.
    # @arg force Whether to write the reference if a reference with the
    #            same name already exists.
    # @arg who The person updating the reference. Shall be used to create
    #          a reflog entry.
    # @arg message The message detailing what kind of reference update is
    #              performed. Shall be used to create a reflog entry.
    # @arg old If not `NULL` and `force` is not set, then the
    #          implementation needs to ensure that the reference is currently at
    #          the given OID before writing the new value. If both `old`
    #          and `old_target` are `NULL`, then the reference should not
    #          exist at the point of writing.
    # @arg old_target If not `NULL` and `force` is not set, then the
    #                 implementation needs to ensure that the symbolic
    #                 reference is currently at the given target before
    #                 writing the new value. If both `old` and
    #                 `old_target` are `NULL`, then the reference should
    #                 not exist at the point of writing.
    # @return `0` on success, otherwise a negative error code.
    #
    ("write", GIT_CALLBACK(ct.c_int,
                 ct.POINTER(git_refdb_backend),  # backend
                 ct.POINTER(git_reference),      # ref
                 ct.c_int,                       # force
                 ct.POINTER(git_signature),      # who
                 ct.c_char_p,                    # message
                 ct.POINTER(git_oid),            # old
                 ct.c_char_p)),                  # old_target

    # Rename a reference in the refdb.
    #
    # A refdb implementation must provide this function.
    #
    # @arg out The implementation shall set this to the newly created
    #          reference or `NULL` on error.
    # @arg old_name The current name of the reference that is to be renamed.
    # @arg new_name The new name that the old reference shall be renamed to.
    # @arg force Whether to write the reference if a reference with the
    #            target name already exists.
    # @arg who The person updating the reference. Shall be used to create
    #          a reflog entry.
    # @arg message The message detailing what kind of reference update is
    #              performed. Shall be used to create a reflog entry.
    # @return `0` on success, otherwise a negative error code.
    #
    ("rename", GIT_CALLBACK(ct.c_int,
                   ct.POINTER(ct.POINTER(git_reference)),  # out
                   ct.POINTER(git_refdb_backend),          # backend
                   ct.c_char_p,                            # old_name
                   ct.c_char_p,                            # new_name
                   ct.c_int,                               # force
                   ct.POINTER(git_signature),              # who
                   ct.c_char_p)),                          # message

    # Deletes the given reference from the refdb.
    #
    # If it exists, its reflog should be deleted as well.
    #
    # A refdb implementation must provide this function.
    #
    # @arg ref_name The name of the reference name that shall be deleted.
    # @arg old_id If not `NULL` and `force` is not set, then the
    #             implementation needs to ensure that the reference is currently at
    #             the given OID before writing the new value.
    # @arg old_target If not `NULL` and `force` is not set, then the
    #                 implementation needs to ensure that the symbolic
    #                 reference is currently at the given target before
    #                 writing the new value.
    # @return `0` on success, otherwise a negative error code.
    #
    ("del", GIT_CALLBACK(ct.c_int,
                ct.POINTER(git_refdb_backend),  # backend
                ct.c_char_p,                    # ref_name,
                ct.POINTER(git_oid),            # old_id,
                ct.c_char_p)),                  # old_target

    # Suggests that the given refdb compress or optimize its references.
    #
    # This mechanism is implementation specific. For on-disk reference
    # databases, this may pack all loose references.
    #
    # A refdb implementation may provide this function; if it is not
    # provided, nothing will be done.
    #
    # @return `0` on success a negative error code otherwise
    #
    ("compress", GIT_CALLBACK(ct.c_int,
                     ct.POINTER(git_refdb_backend))),  # backend

    # Query whether a particular reference has a log (may be empty)
    #
    # Shall return 1 if it has a reflog, 0 it it doesn't and negative in
    # case an error occurred.
    #
    # A refdb implementation must provide this function.
    #
    # @return `0` on success, `1` if the reflog for the given reference
    #         exists, a negative error code otherwise
    #
    ("has_log", GIT_CALLBACK(ct.c_int,
                    ct.POINTER(git_refdb_backend),  # backend
                    ct.c_char_p)),                  # refname

    # Make sure a particular reference will have a reflog which
    # will be appended to on writes.
    #
    # A refdb implementation must provide this function.
    #
    # @return `0` on success, a negative error code otherwise
    #
    ("ensure_log", GIT_CALLBACK(ct.c_int,
                       ct.POINTER(git_refdb_backend),  # backend
                       ct.c_char_p)),                  # refname

    # Frees any resources held by the refdb (including the `git_refdb_backend`
    # itself).
    #
    # A refdb backend implementation must provide this function.
    #
    ("free", GIT_CALLBACK(None,
                 ct.POINTER(git_refdb_backend))),  # backend

    # Read the reflog for the given reference name.
    #
    # A refdb implementation must provide this function.
    #
    # @return `0` on success, a negative error code otherwise
    #
    ("reflog_read", GIT_CALLBACK(ct.c_int,
                        ct.POINTER(ct.POINTER(git_reflog)),  # out
                        ct.POINTER(git_refdb_backend),       # backend
                        ct.c_char_p)),                       # name

    # Write a reflog to disk.
    #
    # A refdb implementation must provide this function.
    #
    # @arg reflog The complete reference log for a given reference. Note
    #             that this may contain entries that have already been
    #             written to disk.
    # @return `0` on success, a negative error code otherwise
    #
    ("reflog_write", GIT_CALLBACK(ct.c_int,
                         ct.POINTER(git_refdb_backend),  # backend
                         ct.POINTER(git_reflog))),       # reflog

    # Rename a reflog.
    #
    # A refdb implementation must provide this function.
    #
    # @arg old_name The name of old reference whose reflog shall be renamed from.
    # @arg new_name The name of new reference whose reflog shall be renamed to.
    # @return `0` on success, a negative error code otherwise
    #
    ("reflog_rename", GIT_CALLBACK(ct.c_int,
                          ct.POINTER(git_refdb_backend),  # backend
                          ct.c_char_p,                    # old_name
                          ct.c_char_p)),                  # new_name

    # Remove a reflog.
    #
    # A refdb implementation must provide this function.
    #
    # @arg name The name of the reference whose reflog shall be deleted.
    # @return `0` on success, a negative error code otherwise
    #
    ("reflog_delete", GIT_CALLBACK(ct.c_int,
                          ct.POINTER(git_refdb_backend),  # backend
                          ct.c_char_p)),                  # name

    # Lock a reference.
    #
    # A refdb implementation may provide this function; if it is not
    # provided, the transaction API will fail to work.
    #
    # @arg payload_out Opaque parameter that will be passed verbosely to
    #                  `unlock`.
    # @arg refname Reference that shall be locked.
    # @return `0` on success, a negative error code otherwise
    #
    ("lock", GIT_CALLBACK(ct.c_int,
                 ct.POINTER(ct.c_void_p),        # payload_out
                 ct.POINTER(git_refdb_backend),  # backend
                 ct.c_char_p)),                  # refname

    # Unlock a reference.
    #
    # Only one of target or symbolic_target will be set.
    # `success` will be true if the reference should be update, false if
    # the lock must be discarded.
    #
    # A refdb implementation must provide this function if a `lock`
    # implementation is provided.
    #
    # @arg payload The payload returned by `lock`.
    # @arg success `1` if a reference should be updated, `2` if
    #              a reference should be deleted, `0` if the lock must be
    #              discarded.
    # @arg update_reflog `1` in case the reflog should be updated, `0`
    #                    otherwise.
    # @arg ref The reference which should be unlocked.
    # @arg who The person updating the reference. Shall be used to create
    #          a reflog entry in case `update_reflog` is set.
    # @arg message The message detailing what kind of reference update is
    #              performed. Shall be used to create a reflog entry in
    #              case `update_reflog` is set.
    # @return `0` on success, a negative error code otherwise
    #
    ("unlock", GIT_CALLBACK(ct.c_int,
                   ct.POINTER(git_refdb_backend),  # backend
                   ct.c_void_p,                    # payload
                   ct.c_int,                       # success
                   ct.c_int,                       # update_reflog
                   ct.POINTER(git_reference),      # ref
                   ct.POINTER(git_signature),      # sig
                   ct.c_char_p)),                  # message
]

GIT_REFDB_BACKEND_VERSION = 1
#define GIT_REFDB_BACKEND_INIT {GIT_REFDB_BACKEND_VERSION}

# Initializes a `git_refdb_backend` with default values. Equivalent to
# creating an instance with GIT_REFDB_BACKEND_INIT.
#
# @param backend the `git_refdb_backend` struct to initialize
# @param version Version of struct; pass `GIT_REFDB_BACKEND_VERSION`
# @return Zero on success; -1 on failure.
#
git_refdb_init_backend = CFUNC(ct.c_int,
    ct.POINTER(git_refdb_backend) ,
    ct.c_uint)(
    ("git_refdb_init_backend", dll), (
    (1, "backend"),
    (1, "version"),))

# Constructors for default filesystem-based refdb backend
#
# Under normal usage, this is called for you when the repository is
# opened / created, but you can use this to explicitly construct a
# filesystem refdb backend for a repository.
#
# @param backend_out Output pointer to the git_refdb_backend object
# @param repo Git repository to access
# @return 0 on success, <0 error code on failure
#
git_refdb_backend_fs = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_refdb_backend)),
    ct.POINTER(git_repository))(
    ("git_refdb_backend_fs", dll), (
    (1, "backend_out"),
    (1, "repo"),))

# Sets the custom backend to an existing reference DB
#
# The `git_refdb` will take ownership of the `git_refdb_backend` so you
# should NOT free it after calling this function.
#
# @param refdb database to add the backend to
# @param backend pointer to a git_refdb_backend instance
# @return 0 on success; error code otherwise
#
git_refdb_set_backend = CFUNC(ct.c_int,
    ct.POINTER(git_refdb),
    ct.POINTER(git_refdb_backend))(
    ("git_refdb_set_backend", dll), (
    (1, "refdb"),
    (1, "backend"),))

# GIT_END_DECL
