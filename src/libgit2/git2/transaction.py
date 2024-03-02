# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .types  import git_repository
from .oid    import git_oid
from .types  import git_signature
from .types  import git_reflog
from .types  import git_transaction

# @file git2/transaction.h
# @brief Git transactional reference routines
# @defgroup git_transaction Git transactional reference routines
# @ingroup Git

# GIT_BEGIN_DECL

# Create a new transaction object
#
# This does not lock anything, but sets up the transaction object to
# know from which repository to lock.
#
# @param out the resulting transaction
# @param repo the repository in which to lock
# @return 0 or an error code
#
git_transaction_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_transaction)),
    ct.POINTER(git_repository))(
    ("git_transaction_new", dll), (
    (1, "out"),
    (1, "repo"),))

# Lock a reference
#
# Lock the specified reference. This is the first step to updating a
# reference.
#
# @param tx the transaction
# @param refname the reference to lock
# @return 0 or an error message
#
git_transaction_lock_ref = CFUNC(ct.c_int,
    ct.POINTER(git_transaction),
    ct.c_char_p)(
    ("git_transaction_lock_ref", dll), (
    (1, "tx"),
    (1, "refname"),))

# Set the target of a reference
#
# Set the target of the specified reference. This reference must be
# locked.
#
# @param tx the transaction
# @param refname reference to update
# @param target target to set the reference to
# @param sig signature to use in the reflog; pass NULL to read the identity from the config
# @param msg message to use in the reflog
# @return 0, GIT_ENOTFOUND if the reference is not among the locked ones, or an error code
#
git_transaction_set_target = CFUNC(ct.c_int,
    ct.POINTER(git_transaction),
    ct.c_char_p,
    ct.POINTER(git_oid),
    ct.POINTER(git_signature),
    ct.c_char_p)(
    ("git_transaction_set_target", dll), (
    (1, "tx"),
    (1, "refname"),
    (1, "target"),
    (1, "sig"),
    (1, "msg"),))

# Set the target of a reference
#
# Set the target of the specified reference. This reference must be
# locked.
#
# @param tx the transaction
# @param refname reference to update
# @param target target to set the reference to
# @param sig signature to use in the reflog; pass NULL to read the identity from the config
# @param msg message to use in the reflog
# @return 0, GIT_ENOTFOUND if the reference is not among the locked ones, or an error code
#
git_transaction_set_symbolic_target = CFUNC(ct.c_int,
    ct.POINTER(git_transaction),
    ct.c_char_p,
    ct.c_char_p,
    ct.POINTER(git_signature),
    ct.c_char_p)(
    ("git_transaction_set_symbolic_target", dll), (
    (1, "tx"),
    (1, "refname"),
    (1, "target"),
    (1, "sig"),
    (1, "msg"),))

# Set the reflog of a reference
#
# Set the specified reference's reflog. If this is combined with
# setting the target, that update won't be written to the reflog.
#
# @param tx the transaction
# @param refname the reference whose reflog to set
# @param reflog the reflog as it should be written out
# @return 0, GIT_ENOTFOUND if the reference is not among the locked ones, or an error code
#
git_transaction_set_reflog = CFUNC(ct.c_int,
    ct.POINTER(git_transaction),
    ct.c_char_p,
    ct.POINTER(git_reflog))(
    ("git_transaction_set_reflog", dll), (
    (1, "tx"),
    (1, "refname"),
    (1, "reflog"),))

# Remove a reference
#
# @param tx the transaction
# @param refname the reference to remove
# @return 0, GIT_ENOTFOUND if the reference is not among the locked ones, or an error code
#
git_transaction_remove = CFUNC(ct.c_int,
    ct.POINTER(git_transaction),
    ct.c_char_p)(
    ("git_transaction_remove", dll), (
    (1, "tx"),
    (1, "refname"),))

# Commit the changes from the transaction
#
# Perform the changes that have been queued. The updates will be made
# one by one, and the first failure will stop the processing.
#
# @param tx the transaction
# @return 0 or an error code
#
git_transaction_commit = CFUNC(ct.c_int,
    ct.POINTER(git_transaction))(
    ("git_transaction_commit", dll), (
    (1, "tx"),))

# Free the resources allocated by this transaction
#
# If any references remain locked, they will be unlocked without any
# changes made to them.
#
# @param tx the transaction
#
git_transaction_free = CFUNC(None,
    ct.POINTER(git_transaction))(
    ("git_transaction_free", dll), (
    (1, "tx"),))

# GIT_END_DECL
