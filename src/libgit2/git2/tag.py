# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common   import *  # noqa
from .oid      import git_oid
from .strarray import git_strarray
from .types    import git_object_t
from .types    import git_object
from .types    import git_signature
from .types    import git_repository
from .types    import git_tag

# @file git2/tag.h
# @brief Git tag parsing routines
# @defgroup git_tag Git tag management
# @ingroup Git

# GIT_BEGIN_DECL

# Lookup a tag object from the repository.
#
# @param out pointer to the looked up tag
# @param repo the repo to use when locating the tag.
# @param id identity of the tag to locate.
# @return 0 or an error code
#
git_tag_lookup = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_tag)),
    ct.POINTER(git_repository),
    ct.POINTER(git_oid))(
    ("git_tag_lookup", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "id"),))

# Lookup a tag object from the repository,
# given a prefix of its identifier (short id).
#
# @see git_object_lookup_prefix
#
# @param out pointer to the looked up tag
# @param repo the repo to use when locating the tag.
# @param id identity of the tag to locate.
# @param len the length of the short identifier
# @return 0 or an error code
#
git_tag_lookup_prefix = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_tag)),
    ct.POINTER(git_repository),
    ct.POINTER(git_oid),
    ct.c_size_t)(
    ("git_tag_lookup_prefix", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "id"),
    (1, "len"),))

# Close an open tag
#
# You can no longer use the git_tag pointer after this call.
#
# IMPORTANT: You MUST call this method when you are through with a tag to
# release memory. Failure to do so will cause a memory leak.
#
# @param tag the tag to close
#
git_tag_free = CFUNC(None,
    ct.POINTER(git_tag))(
    ("git_tag_free", dll), (
    (1, "tag"),))

# Get the id of a tag.
#
# @param tag a previously loaded tag.
# @return object identity for the tag.
#
git_tag_id = CFUNC(ct.POINTER(git_oid),
    ct.POINTER(git_tag))(
    ("git_tag_id", dll), (
    (1, "tag"),))

# Get the repository that contains the tag.
#
# @param tag A previously loaded tag.
# @return Repository that contains this tag.
#
git_tag_owner = CFUNC(ct.POINTER(git_repository),
    ct.POINTER(git_tag))(
    ("git_tag_owner", dll), (
    (1, "tag"),))

# Get the tagged object of a tag
#
# This method performs a repository lookup for the
# given object and returns it
#
# @param target_out pointer where to store the target
# @param tag a previously loaded tag.
# @return 0 or an error code
#
git_tag_target = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_object)),
    ct.POINTER(git_tag))(
    ("git_tag_target", dll), (
    (1, "target_out"),
    (1, "tag"),))

# Get the OID of the tagged object of a tag
#
# @param tag a previously loaded tag.
# @return pointer to the OID
#
git_tag_target_id = CFUNC(ct.POINTER(git_oid),
    ct.POINTER(git_tag))(
    ("git_tag_target_id", dll), (
    (1, "tag"),))

# Get the type of a tag's tagged object
#
# @param tag a previously loaded tag.
# @return type of the tagged object
#
git_tag_target_type = CFUNC(git_object_t,
    ct.POINTER(git_tag))(
    ("git_tag_target_type", dll), (
    (1, "tag"),))

# Get the name of a tag
#
# @param tag a previously loaded tag.
# @return name of the tag
#
git_tag_name = CFUNC(ct.c_char_p,
    ct.POINTER(git_tag))(
    ("git_tag_name", dll), (
    (1, "tag"),))

# Get the tagger (author) of a tag
#
# @param tag a previously loaded tag.
# @return reference to the tag's author or NULL when unspecified
#
git_tag_tagger = CFUNC(ct.POINTER(git_signature),
    ct.POINTER(git_tag))(
    ("git_tag_tagger", dll), (
    (1, "tag"),))

# Get the message of a tag
#
# @param tag a previously loaded tag.
# @return message of the tag or NULL when unspecified
#
git_tag_message = CFUNC(ct.c_char_p,
    ct.POINTER(git_tag))(
    ("git_tag_message", dll), (
    (1, "tag"),))

# Create a new tag in the repository from an object
#
# A new reference will also be created pointing to
# this tag object. If `force` is true and a reference
# already exists with the given name, it'll be replaced.
#
# The message will not be cleaned up. This can be achieved
# through `git_message_prettify()`.
#
# The tag name will be checked for validity. You must avoid
# the characters '~', '^', ':', '\\', '?', '[', and '*', and the
# sequences ".." and "@{" which have special meaning to revparse.
#
# @param oid Pointer where to store the OID of the
# newly created tag. If the tag already exists, this parameter
# will be the oid of the existing tag, and the function will
# return a GIT_EEXISTS error code.
#
# @param repo Repository where to store the tag
#
# @param tag_name Name for the tag; this name is validated
# for consistency. It should also not conflict with an
# already existing tag name
#
# @param target Object to which this tag points. This object
# must belong to the given `repo`.
#
# @param tagger Signature of the tagger for this tag, and
# of the tagging time
#
# @param message Full message for this tag
#
# @param force Overwrite existing references
#
# @return 0 on success, GIT_EINVALIDSPEC or an error code
#  A tag object is written to the ODB, and a proper reference
#  is written in the /refs/tags folder, pointing to it
#
git_tag_create = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.POINTER(git_object),
    ct.POINTER(git_signature),
    ct.c_char_p,
    ct.c_int)(
    ("git_tag_create", dll), (
    (1, "oid"),
    (1, "repo"),
    (1, "tag_name"),
    (1, "target"),
    (1, "tagger"),
    (1, "message"),
    (1, "force"),))

# Create a new tag in the object database pointing to a git_object
#
# The message will not be cleaned up. This can be achieved
# through `git_message_prettify()`.
#
# @param oid Pointer where to store the OID of the
# newly created tag
#
# @param repo Repository where to store the tag
#
# @param tag_name Name for the tag
#
# @param target Object to which this tag points. This object
# must belong to the given `repo`.
#
# @param tagger Signature of the tagger for this tag, and
# of the tagging time
#
# @param message Full message for this tag
#
# @return 0 on success or an error code
#
git_tag_annotation_create = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.POINTER(git_object),
    ct.POINTER(git_signature),
    ct.c_char_p)(
    ("git_tag_annotation_create", dll), (
    (1, "oid"),
    (1, "repo"),
    (1, "tag_name"),
    (1, "target"),
    (1, "tagger"),
    (1, "message"),))

# Create a new tag in the repository from a buffer
#
# @param oid Pointer where to store the OID of the newly created tag
# @param repo Repository where to store the tag
# @param buffer Raw tag data
# @param force Overwrite existing tags
# @return 0 on success; error code otherwise
#
git_tag_create_from_buffer = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    git_buffer_t,
    ct.c_int)(
    ("git_tag_create_from_buffer", dll), (
    (1, "oid"),
    (1, "repo"),
    (1, "buffer"),
    (1, "force"),))

# Create a new lightweight tag pointing at a target object
#
# A new direct reference will be created pointing to
# this target object. If `force` is true and a reference
# already exists with the given name, it'll be replaced.
#
# The tag name will be checked for validity.
# See `git_tag_create()` for rules about valid names.
#
# @param oid Pointer where to store the OID of the provided
# target object. If the tag already exists, this parameter
# will be filled with the oid of the existing pointed object
# and the function will return a GIT_EEXISTS error code.
#
# @param repo Repository where to store the lightweight tag
#
# @param tag_name Name for the tag; this name is validated
# for consistency. It should also not conflict with an
# already existing tag name
#
# @param target Object to which this tag points. This object
# must belong to the given `repo`.
#
# @param force Overwrite existing references
#
# @return 0 on success, GIT_EINVALIDSPEC or an error code
#  A proper reference is written in the /refs/tags folder,
# pointing to the provided target object
#
git_tag_create_lightweight = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.POINTER(git_object),
    ct.c_int)(
    ("git_tag_create_lightweight", dll), (
    (1, "oid"),
    (1, "repo"),
    (1, "tag_name"),
    (1, "target"),
    (1, "force"),))

# Delete an existing tag reference.
#
# The tag name will be checked for validity.
# See `git_tag_create()` for rules about valid names.
#
# @param repo Repository where lives the tag
#
# @param tag_name Name of the tag to be deleted;
# this name is validated for consistency.
#
# @return 0 on success, GIT_EINVALIDSPEC or an error code
#
git_tag_delete = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_tag_delete", dll), (
    (1, "repo"),
    (1, "tag_name"),))

# Fill a list with all the tags in the Repository
#
# The string array will be filled with the names of the
# matching tags; these values are owned by the user and
# should be free'd manually when no longer needed, using
# `git_strarray_free`.
#
# @param tag_names Pointer to a git_strarray structure where
#      the tag names will be stored
# @param repo Repository where to find the tags
# @return 0 or an error code
#
git_tag_list = CFUNC(ct.c_int,
    ct.POINTER(git_strarray),
    ct.POINTER(git_repository))(
    ("git_tag_list", dll), (
    (1, "tag_names"),
    (1, "repo"),))

# Fill a list with all the tags in the Repository
# which name match a defined pattern
#
# If an empty pattern is provided, all the tags
# will be returned.
#
# The string array will be filled with the names of the
# matching tags; these values are owned by the user and
# should be free'd manually when no longer needed, using
# `git_strarray_free`.
#
# @param tag_names Pointer to a git_strarray structure where
#      the tag names will be stored
# @param pattern Standard fnmatch pattern
# @param repo Repository where to find the tags
# @return 0 or an error code
#
git_tag_list_match = CFUNC(ct.c_int,
    ct.POINTER(git_strarray),
    ct.c_char_p,
    ct.POINTER(git_repository))(
    ("git_tag_list_match", dll), (
    (1, "tag_names"),
    (1, "pattern"),
    (1, "repo"),))

# Callback used to iterate over tag names
#
# @see git_tag_foreach
#
# @param name The tag name
# @param oid The tag's OID
# @param payload Payload passed to git_tag_foreach
# @return non-zero to terminate the iteration
#
git_tag_foreach_cb = GIT_CALLBACK(ct.c_int,
    ct.c_char_p,          # name
    ct.POINTER(git_oid),  # oid
    ct.c_void_p)          # payload

# Call callback `cb' for each tag in the repository
#
# @param repo Repository
# @param callback Callback function
# @param payload Pointer to callback data (optional)
#
git_tag_foreach = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    git_tag_foreach_cb,
    ct.c_void_p)(
    ("git_tag_foreach", dll), (
    (1, "repo"),
    (1, "callback"),
    (1, "payload"),))

# Recursively peel a tag until a non tag git_object is found
#
# The retrieved `tag_target` object is owned by the repository
# and should be closed with the `git_object_free` method.
#
# @param tag_target_out Pointer to the peeled git_object
# @param tag The tag to be processed
# @return 0 or an error code
#
git_tag_peel = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_object)),
    ct.POINTER(git_tag))(
    ("git_tag_peel", dll), (
    (1, "tag_target_out"),
    (1, "tag"),))

# Create an in-memory copy of a tag. The copy must be explicitly
# free'd or it will leak.
#
# @param out Pointer to store the copy of the tag
# @param source Original tag to copy
# @return 0
#
git_tag_dup = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_tag)),
    ct.POINTER(git_tag))(
    ("git_tag_dup", dll), (
    (1, "out"),
    (1, "source"),))

# Determine whether a tag name is valid, meaning that (when prefixed
# with `refs/tags/`) that it is a valid reference name, and that any
# additional tag name restrictions are imposed (eg, it cannot start
# with a `-`).
#
# @param valid output pointer to set with validity of given tag name
# @param name a tag name to test
# @return 0 on success or an error code
#
git_tag_name_is_valid = CFUNC(ct.c_int,
    ct.POINTER(ct.c_int),
    ct.c_char_p)(
    ("git_tag_name_is_valid", dll), (
    (1, "valid"),
    (1, "name"),))

# GIT_END_DECL
