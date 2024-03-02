# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .buffer import git_buf
from .oid    import git_oid
from .types  import git_object_size_t
from .types  import git_repository
from .types  import git_blob
from .types  import git_writestream

# @file git2/blob.h
# @brief Git blob load and write routines
# @defgroup git_blob Git blob load and write routines
# @ingroup Git

# GIT_BEGIN_DECL

# Lookup a blob object from a repository.
#
# @param blob pointer to the looked up blob
# @param repo the repo to use when locating the blob.
# @param id identity of the blob to locate.
# @return 0 or an error code
#
git_blob_lookup = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_blob)),
    ct.POINTER(git_repository),
    ct.POINTER(git_oid))(
    ("git_blob_lookup", dll), (
    (1, "blob"),
    (1, "repo"),
    (1, "id"),))

# Lookup a blob object from a repository,
# given a prefix of its identifier (short id).
#
# @see git_object_lookup_prefix
#
# @param blob pointer to the looked up blob
# @param repo the repo to use when locating the blob.
# @param id identity of the blob to locate.
# @param len the length of the short identifier
# @return 0 or an error code
#
git_blob_lookup_prefix = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_blob)),
    ct.POINTER(git_repository),
    ct.POINTER(git_oid),
    ct.c_size_t)(
    ("git_blob_lookup_prefix", dll), (
    (1, "blob"),
    (1, "repo"),
    (1, "id"),
    (1, "len"),))

# Close an open blob
#
# This is a wrapper around git_object_free()
#
# IMPORTANT:
# It *is* necessary to call this method when you stop
# using a blob. Failure to do so will cause a memory leak.
#
# @param blob the blob to close
#
git_blob_free = CFUNC(None,
    ct.POINTER(git_blob))(
    ("git_blob_free", dll), (
    (1, "blob"),))

# Get the id of a blob.
#
# @param blob a previously loaded blob.
# @return SHA1 hash for this blob.
#
git_blob_id = CFUNC(ct.POINTER(git_oid),
    ct.POINTER(git_blob))(
    ("git_blob_id", dll), (
    (1, "blob"),))

# Get the repository that contains the blob.
#
# @param blob A previously loaded blob.
# @return Repository that contains this blob.
#
git_blob_owner = CFUNC(ct.POINTER(git_repository),
    ct.POINTER(git_blob))(
    ("git_blob_owner", dll), (
    (1, "blob"),))

# Get a read-only buffer with the raw content of a blob.
#
# A pointer to the raw content of a blob is returned;
# this pointer is owned internally by the object and shall
# not be free'd. The pointer may be invalidated at a later
# time.
#
# @param blob pointer to the blob
# @return the pointer, or NULL on error
#
git_blob_rawcontent = CFUNC(ct.c_void_p,
    ct.POINTER(git_blob))(
    ("git_blob_rawcontent", dll), (
    (1, "blob"),))

# Get the size in bytes of the contents of a blob
#
# @param blob pointer to the blob
# @return size on bytes
#
git_blob_rawsize = CFUNC(git_object_size_t,
    ct.POINTER(git_blob))(
    ("git_blob_rawsize", dll), (
    (1, "blob"),))

# Flags to control the functionality of `git_blob_filter`.
#
git_blob_filter_flag_t = ct.c_int
(
    # When set, filters will not be applied to binary files.
    GIT_BLOB_FILTER_CHECK_FOR_BINARY,

    # When set, filters will not load configuration from the
    # system-wide `gitattributes` in `/etc` (or system equivalent).
    #
    GIT_BLOB_FILTER_NO_SYSTEM_ATTRIBUTES,

    # When set, filters will be loaded from a `.gitattributes` file
    # in the HEAD commit.
    #
    GIT_BLOB_FILTER_ATTRIBUTES_FROM_HEAD,

    # When set, filters will be loaded from a `.gitattributes` file
    # in the specified commit.
    #
    GIT_BLOB_FILTER_ATTRIBUTES_FROM_COMMIT,

) = (1 << 0, 1 << 1, 1 << 2, 1 << 3)

# The options used when applying filter options to a file.
#
# Initialize with `GIT_BLOB_FILTER_OPTIONS_INIT`. Alternatively, you can
# use `git_blob_filter_options_init`.
#
#
class git_blob_filter_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_int),

    # Flags to control the filtering process, see `git_blob_filter_flag_t` above
    ("flags", ct.c_uint32),

    *([("reserved", ct.c_void_p)]
      if defined("GIT_DEPRECATE_HARD") else
      [("commit_id", ct.POINTER(git_oid))]),

    # The commit to load attributes from, when
    # `GIT_BLOB_FILTER_ATTRIBUTES_FROM_COMMIT` is specified.
    ("attr_commit_id", git_oid),
]

GIT_BLOB_FILTER_OPTIONS_VERSION = 1
#define GIT_BLOB_FILTER_OPTIONS_INIT = { GIT_BLOB_FILTER_OPTIONS_VERSION, GIT_BLOB_FILTER_CHECK_FOR_BINARY }

# Initialize git_blob_filter_options structure
#
# Initializes a `git_blob_filter_options` with default values. Equivalent
# to creating an instance with `GIT_BLOB_FILTER_OPTIONS_INIT`.
#
# @param opts The `git_blob_filter_options` struct to initialize.
# @param version The struct version; pass `GIT_BLOB_FILTER_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_blob_filter_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_blob_filter_options),
    ct.c_uint)(
    ("git_blob_filter_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Get a buffer with the filtered content of a blob.
#
# This applies filters as if the blob was being checked out to the
# working directory under the specified filename.  This may apply
# CRLF filtering or other types of changes depending on the file
# attributes set for the blob and the content detected in it.
#
# The output is written into a `git_buf` which the caller must free
# when done (via `git_buf_dispose`).
#
# If no filters need to be applied, then the `out` buffer will just
# be populated with a pointer to the raw content of the blob.  In
# that case, be careful to *not* free the blob until done with the
# buffer or copy it into memory you own.
#
# @param out The git_buf to be filled in
# @param blob Pointer to the blob
# @param as_path Path used for file attribute lookups, etc.
# @param opts Options to use for filtering the blob
# @return 0 on success or an error code
#
git_blob_filter = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_blob),
    ct.c_char_p,
    ct.POINTER(git_blob_filter_options))(
    ("git_blob_filter", dll), (
    (1, "out"),
    (1, "blob"),
    (1, "as_path"),
    (1, "opts"),))

# Read a file from the working folder of a repository
# and write it to the Object Database as a loose blob
#
# @param id return the id of the written blob
# @param repo repository where the blob will be written.
#  this repository cannot be bare
# @param relative_path file from which the blob will be created,
#  relative to the repository's working dir
# @return 0 or an error code
#
git_blob_create_from_workdir = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_blob_create_from_workdir", dll), (
    (1, "id"),
    (1, "repo"),
    (1, "relative_path"),))

# Read a file from the filesystem and write its content
# to the Object Database as a loose blob
#
# @param id return the id of the written blob
# @param repo repository where the blob will be written.
#  this repository can be bare or not
# @param path file from which the blob will be created
# @return 0 or an error code
#
git_blob_create_from_disk = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_blob_create_from_disk", dll), (
    (1, "id"),
    (1, "repo"),
    (1, "path"),))

# Create a stream to write a new blob into the object db
#
# This function may need to buffer the data on disk and will in
# general not be the right choice if you know the size of the data
# to write. If you have data in memory, use
# `git_blob_create_from_buffer()`. If you do not, but know the size of
# the contents (and don't want/need to perform filtering), use
# `git_odb_open_wstream()`.
#
# Don't close this stream yourself but pass it to
# `git_blob_create_from_stream_commit()` to commit the write to the
# object db and get the object id.
#
# If the `hintpath` parameter is filled, it will be used to determine
# what git filters should be applied to the object before it is written
# to the object database.
#
# @param out the stream into which to write
# @param repo Repository where the blob will be written.
#        This repository can be bare or not.
# @param hintpath If not NULL, will be used to select data filters
#        to apply onto the content of the blob to be created.
# @return 0 or error code
#
git_blob_create_from_stream = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_writestream)),
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_blob_create_from_stream", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "hintpath"),))

# Close the stream and write the blob to the object db
#
# The stream will be closed and freed.
#
# @param out the id of the new blob
# @param stream the stream to close
# @return 0 or an error code
#
git_blob_create_from_stream_commit = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_writestream))(
    ("git_blob_create_from_stream_commit", dll), (
    (1, "out"),
    (1, "stream"),))

# Write an in-memory buffer to the ODB as a blob
#
# @param id return the id of the written blob
# @param repo repository where the blob will be written
# @param buffer data to be written into the blob
# @param len length of the data
# @return 0 or an error code
#
git_blob_create_from_buffer = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.c_void_p,
    ct.c_size_t)(
    ("git_blob_create_from_buffer", dll), (
    (1, "id"),
    (1, "repo"),
    (1, "buffer"),
    (1, "len"),))

# Determine if the blob content is most certainly binary or not.
#
# The heuristic used to guess if a file is binary is taken from core git:
# Searching for NUL bytes and looking for a reasonable ratio of printable
# to non-printable characters among the first 8000 bytes.
#
# @param blob The blob which content should be analyzed
# @return 1 if the content of the blob is detected
# as binary; 0 otherwise.
#
git_blob_is_binary = CFUNC(ct.c_int,
    ct.POINTER(git_blob))(
    ("git_blob_is_binary", dll), (
    (1, "blob"),))

# Determine if the given content is most certainly binary or not;
# this is the same mechanism used by `git_blob_is_binary` but only
# looking at raw data.
#
# @param data The blob data which content should be analyzed
# @param len The length of the data
# @return 1 if the content of the blob is detected
# as binary; 0 otherwise.
#
git_blob_data_is_binary = CFUNC(ct.c_int,
    git_buffer_t,
    ct.c_size_t)(
    ("git_blob_data_is_binary", dll), (
    (1, "data"),
    (1, "len"),))

# Create an in-memory copy of a blob. The copy must be explicitly
# free'd or it will leak.
#
# @param out Pointer to store the copy of the object
# @param source Original object to copy
# @return 0.
#
git_blob_dup = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_blob)),
    ct.POINTER(git_blob))(
    ("git_blob_dup", dll), (
    (1, "out"),
    (1, "source"),))

# GIT_END_DECL
