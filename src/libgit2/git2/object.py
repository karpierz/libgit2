# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .oid    import git_oid_t
from .oid    import git_oid
from .buffer import git_buf
from .types  import git_object_t
from .types  import git_object
from .types  import git_repository

# @file git2/object.h
# @brief Git revision object management routines
# @defgroup git_object Git revision object management routines
# @ingroup Git

# GIT_BEGIN_DECL

GIT_OBJECT_SIZE_MAX = ct.c_uint64(-1).value  # UINT64_MAX

# Lookup a reference to one of the objects in a repository.
#
# The generated reference is owned by the repository and
# should be closed with the `git_object_free` method
# instead of free'd manually.
#
# The 'type' parameter must match the type of the object
# in the odb; the method will fail otherwise.
# The special value 'GIT_OBJECT_ANY' may be passed to let
# the method guess the object's type.
#
# @param object pointer to the looked-up object
# @param repo the repository to look up the object
# @param id the unique identifier for the object
# @param type the type of the object
# @return 0 or an error code
#
git_object_lookup = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_object)),
    ct.POINTER(git_repository),
    ct.POINTER(git_oid),
    git_object_t)(
    ("git_object_lookup", dll), (
    (1, "object"),
    (1, "repo"),
    (1, "id"),
    (1, "type"),))

# Lookup a reference to one of the objects in a repository,
# given a prefix of its identifier (short id).
#
# The object obtained will be so that its identifier
# matches the first 'len' hexadecimal characters
# (packets of 4 bits) of the given 'id'.
# 'len' must be at least GIT_OID_MINPREFIXLEN, and
# long enough to identify a unique object matching
# the prefix; otherwise the method will fail.
#
# The generated reference is owned by the repository and
# should be closed with the `git_object_free` method
# instead of free'd manually.
#
# The 'type' parameter must match the type of the object
# in the odb; the method will fail otherwise.
# The special value 'GIT_OBJECT_ANY' may be passed to let
# the method guess the object's type.
#
# @param object_out pointer where to store the looked-up object
# @param repo the repository to look up the object
# @param id a short identifier for the object
# @param len the length of the short identifier
# @param type the type of the object
# @return 0 or an error code
#
git_object_lookup_prefix = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_object)),
    ct.POINTER(git_repository),
    ct.POINTER(git_oid),
    ct.c_size_t,
    git_object_t)(
    ("git_object_lookup_prefix", dll), (
    (1, "object_out"),
    (1, "repo"),
    (1, "id"),
    (1, "len"),
    (1, "type"),))

# Lookup an object that represents a tree entry.
#
# @param out buffer that receives a pointer to the object (which must be freed
#            by the caller)
# @param treeish root object that can be peeled to a tree
# @param path relative path from the root object to the desired object
# @param type type of object desired
# @return 0 on success, or an error code
#
git_object_lookup_bypath = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_object)),
    ct.POINTER(git_object),
    ct.c_char_p,
    git_object_t)(
    ("git_object_lookup_bypath", dll), (
    (1, "out"),
    (1, "treeish"),
    (1, "path"),
    (1, "type"),))

# Get the id (SHA1) of a repository object
#
# @param obj the repository object
# @return the SHA1 id
#
git_object_id = CFUNC(ct.POINTER(git_oid),
    ct.POINTER(git_object))(
    ("git_object_id", dll), (
    (1, "obj"),))

# Get a short abbreviated OID string for the object
#
# This starts at the "core.abbrev" length (default 7 characters) and
# iteratively extends to a longer string if that length is ambiguous.
# The result will be unambiguous (at least until new objects are added to
# the repository).
#
# @param out Buffer to write string into
# @param obj The object to get an ID for
# @return 0 on success, <0 for error
#
git_object_short_id = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_object))(
    ("git_object_short_id", dll), (
    (1, "out"),
    (1, "obj"),))

# Get the object type of an object
#
# @param obj the repository object
# @return the object's type
#
git_object_type = CFUNC(git_object_t,
    ct.POINTER(git_object))(
    ("git_object_type", dll), (
    (1, "obj"),))

# Get the repository that owns this object
#
# Freeing or calling `git_repository_close` on the
# returned pointer will invalidate the actual object.
#
# Any other operation may be run on the repository without
# affecting the object.
#
# @param obj the object
# @return the repository who owns this object
#
git_object_owner = CFUNC(ct.POINTER(git_repository),
    ct.POINTER(git_object))(
    ("git_object_owner", dll), (
    (1, "obj"),))

# Close an open object
#
# This method instructs the library to close an existing
# object; note that git_objects are owned and cached by the repository
# so the object may or may not be freed after this library call,
# depending on how aggressive is the caching mechanism used
# by the repository.
#
# IMPORTANT:
# It *is* necessary to call this method when you stop using
# an object. Failure to do so will cause a memory leak.
#
# @param object the object to close
#
git_object_free = CFUNC(None,
    ct.POINTER(git_object))(
    ("git_object_free", dll), (
    (1, "obj"),))

# Convert an object type to its string representation.
#
# The result is a pointer to a string in static memory and
# should not be free()'ed.
#
# @param type object type to convert.
# @return the corresponding string representation.
#
git_object_type2string = CFUNC(ct.c_char_p,
    git_object_t)(
    ("git_object_type2string", dll), (
    (1, "type"),))

# Convert a string object type representation to it's git_object_t.
#
# @param str the string to convert.
# @return the corresponding git_object_t.
#
git_object_string2type = CFUNC(git_object_t,
    ct.c_char_p)(
    ("git_object_string2type", dll), (
    (1, "str"),))

# Determine if the given git_object_t is a valid loose object type.
#
# @param type object type to test.
# @return true if the type represents a valid loose object type,
# false otherwise.
#
git_object_typeisloose = CFUNC(ct.c_int,
    git_object_t)(
    ("git_object_typeisloose", dll), (
    (1, "type"),))

# Recursively peel an object until an object of the specified type is met.
#
# If the query cannot be satisfied due to the object model,
# GIT_EINVALIDSPEC will be returned (e.g. trying to peel a blob to a
# tree).
#
# If you pass `GIT_OBJECT_ANY` as the target type, then the object will
# be peeled until the type changes. A tag will be peeled until the
# referenced object is no longer a tag, and a commit will be peeled
# to a tree. Any other object type will return GIT_EINVALIDSPEC.
#
# If peeling a tag we discover an object which cannot be peeled to
# the target type due to the object model, GIT_EPEEL will be
# returned.
#
# You must free the returned object.
#
# @param peeled Pointer to the peeled git_object
# @param object The object to be processed
# @param target_type The type of the requested object (a GIT_OBJECT_ value)
# @return 0 on success, GIT_EINVALIDSPEC, GIT_EPEEL, or an error code
#
git_object_peel = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_object)),
    ct.POINTER(git_object),
    git_object_t)(
    ("git_object_peel", dll), (
    (1, "peeled"),
    (1, "object"),
    (1, "target_type"),))

# Create an in-memory copy of a Git object. The copy must be
# explicitly free'd or it will leak.
#
# @param dest Pointer to store the copy of the object
# @param source Original object to copy
# @return 0 or an error code
#
git_object_dup = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_object)),
    ct.POINTER(git_object))(
    ("git_object_dup", dll), (
    (1, "dest"),
    (1, "source"),))

if defined("GIT_EXPERIMENTAL_SHA256"):
    # Analyzes a buffer of raw object content and determines its validity.
    # Tree, commit, and tag objects will be parsed and ensured that they
    # are valid, parseable content.  (Blobs are always valid by definition.)
    # An error message will be set with an informative message if the object
    # is not valid.
    #
    # @warning This function is experimental and its signature may change in
    # the future.
    #
    # @param valid Output pointer to set with validity of the object content
    # @param buf The contents to validate
    # @param len The length of the buffer
    # @param object_type The type of the object in the buffer
    # @param oid_type The object ID type for the OIDs in the given buffer
    # @return 0 on success or an error code
    #
    git_object_rawcontent_is_valid = CFUNC(ct.c_int,
        ct.POINTER(ct.c_int),
        git_buffer_t,
        ct.c_size_t,
        git_object_t,
        git_oid_t)(
        ("git_object_rawcontent_is_valid", dll), (
        (1, "valid"),
        (1, "buf"),
        (1, "len"),
        (1, "object_type"),
        (1, "oid_type"),))
else:
    # Analyzes a buffer of raw object content and determines its validity.
    # Tree, commit, and tag objects will be parsed and ensured that they
    # are valid, parseable content.  (Blobs are always valid by definition.)
    # An error message will be set with an informative message if the object
    # is not valid.
    #
    # @warning This function is experimental and its signature may change in
    # the future.
    #
    # @param valid Output pointer to set with validity of the object content
    # @param buf The contents to validate
    # @param len The length of the buffer
    # @param object_type The type of the object in the buffer
    # @return 0 on success or an error code
    #
    git_object_rawcontent_is_valid = CFUNC(ct.c_int,
        ct.POINTER(ct.c_int),
        git_buffer_t,
        ct.c_size_t,
        git_object_t)(
        ("git_object_rawcontent_is_valid", dll), (
        (1, "valid"),
        (1, "buf"),
        (1, "len"),
        (1, "object_type"),))
# endif

# GIT_END_DECL
