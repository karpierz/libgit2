# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common  import *  # noqa
from .oid     import git_oid_t
from .oid     import git_oid
from .types   import git_object_t
from .types   import git_object_size_t
from .types   import git_odb
from .types   import git_odb_object
from .types   import git_odb_stream
from .types   import git_odb_writepack
from .types   import git_odb_backend
from .types   import git_commit_graph
from .indexer import git_indexer_progress_cb

# @file git2/odb.h
# @brief Git object database routines
# @defgroup git_odb Git object database routines
# @ingroup Git

# GIT_BEGIN_DECL

# Flags controlling the behavior of ODB lookup operations
git_odb_lookup_flags_t = ct.c_int
(   # Don't call `git_odb_refresh` if the lookup fails. Useful when doing
    # a batch of lookup operations for objects that may legitimately not
    # exist. When using this flag, you may wish to manually call
    # `git_odb_refresh` before processing a batch of objects.
    #
    GIT_ODB_LOOKUP_NO_REFRESH,
) = (1 << 0,)

# Function type for callbacks from git_odb_foreach.
#
git_odb_foreach_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_oid),  # id
    ct.c_void_p)          # payload

# Options for configuring a loose object backend.
class git_odb_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),  # version for the struct

    # Type of object IDs to use for this object database, or
    # 0 for default (currently SHA1).
    #
    ("oid_type", git_oid_t),
]

# The current version of the diff options structure
GIT_ODB_OPTIONS_VERSION = 1

# Stack initializer for odb options.  Alternatively use
# `git_odb_options_init` programmatic initialization.
#
#define GIT_ODB_OPTIONS_INIT { GIT_ODB_OPTIONS_VERSION }

# Create a new object database with no backends.
#
# Before the ODB can be used for read/writing, a custom database
# backend must be manually added using `git_odb_add_backend()`
#
# @param out location to store the database pointer, if opened.
#          Set to NULL if the open failed.
# @param opts the options for this object database or NULL for defaults
# @return 0 or an error code
#
if defined("GIT_EXPERIMENTAL_SHA256"):
    git_odb_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_odb)),
        ct.POINTER(git_odb_options))(
        ("git_odb_new", dll), (
        (1, "out"),
        (1, "opts"),))
else:
    git_odb_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_odb)))(
        ("git_odb_new", dll), (
        (1, "out"),))
# endif

# Create a new object database and automatically add
# the two default backends:
#
#  - git_odb_backend_loose: read and write loose object files
#      from disk, assuming `objects_dir` as the Objects folder
#
#  - git_odb_backend_pack: read objects from packfiles,
#      assuming `objects_dir` as the Objects folder which
#      contains a 'pack/' folder with the corresponding data
#
# @param out location to store the database pointer, if opened.
#          Set to NULL if the open failed.
# @param objects_dir path of the backends' "objects" directory.
# @param opts the options for this object database or NULL for defaults
# @return 0 or an error code
#
if defined("GIT_EXPERIMENTAL_SHA256"):
    git_odb_open = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_odb)),
        ct.c_char_p,
        ct.POINTER(git_odb_options))(
        ("git_odb_open", dll), (
        (1, "out"),
        (1, "objects_dir"),
        (1, "opts"),))
else:
    git_odb_open = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_odb)),
        ct.c_char_p)(
        ("git_odb_open", dll), (
        (1, "out"),
        (1, "objects_dir"),))
# endif

# Add an on-disk alternate to an existing Object DB.
#
# Note that the added path must point to an `objects`, not
# to a full repository, to use it as an alternate store.
#
# Alternate backends are always checked for objects *after*
# all the main backends have been exhausted.
#
# Writing is disabled on alternate backends.
#
# @param odb database to add the backend to
# @param path path to the objects folder for the alternate
# @return 0 on success, error code otherwise
#
git_odb_add_disk_alternate = CFUNC(ct.c_int,
    ct.POINTER(git_odb),
    ct.c_char_p)(
    ("git_odb_add_disk_alternate", dll), (
    (1, "odb"),
    (1, "path"),))

# Close an open object database.
#
# @param db database pointer to close. If NULL no action is taken.
#
git_odb_free = CFUNC(None,
    ct.POINTER(git_odb))(
    ("git_odb_free", dll), (
    (1, "db"),))

# Read an object from the database.
#
# This method queries all available ODB backends
# trying to read the given OID.
#
# The returned object is reference counted and
# internally cached, so it should be closed
# by the user once it's no longer in use.
#
# @param out pointer where to store the read object
# @param db database to search for the object in.
# @param id identity of the object to read.
# @return 0 if the object was read, GIT_ENOTFOUND if the object is
#         not in the database.
#
git_odb_read = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_odb_object)),
    ct.POINTER(git_odb),
    ct.POINTER(git_oid))(
    ("git_odb_read", dll), (
    (1, "out"),
    (1, "db"),
    (1, "id"),))

# Read an object from the database, given a prefix
# of its identifier.
#
# This method queries all available ODB backends
# trying to match the 'len' first hexadecimal
# characters of the 'short_id'.
# The remaining (GIT_OID_SHA1_HEXSIZE-len)*4 bits of
# 'short_id' must be 0s.
# 'len' must be at least GIT_OID_MINPREFIXLEN,
# and the prefix must be long enough to identify
# a unique object in all the backends; the
# method will fail otherwise.
#
# The returned object is reference counted and
# internally cached, so it should be closed
# by the user once it's no longer in use.
#
# @param out pointer where to store the read object
# @param db database to search for the object in.
# @param short_id a prefix of the id of the object to read.
# @param len the length of the prefix
# @return 0 if the object was read, GIT_ENOTFOUND if the object is not in the
#         database. GIT_EAMBIGUOUS if the prefix is ambiguous
#         (several objects match the prefix)
#
git_odb_read_prefix = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_odb_object)),
    ct.POINTER(git_odb),
    ct.POINTER(git_oid),
    ct.c_size_t)(
    ("git_odb_read_prefix", dll), (
    (1, "out"),
    (1, "db"),
    (1, "short_id"),
    (1, "len"),))

# Read the header of an object from the database, without
# reading its full contents.
#
# The header includes the length and the type of an object.
#
# Note that most backends do not support reading only the header
# of an object, so the whole object will be read and then the
# header will be returned.
#
# @param len_out pointer where to store the length
# @param type_out pointer where to store the type
# @param db database to search for the object in.
# @param id identity of the object to read.
# @return 0 if the object was read, GIT_ENOTFOUND if the object is not
#         in the database.
#
git_odb_read_header = CFUNC(ct.c_int,
    ct.POINTER(ct.c_size_t),
    ct.POINTER(git_object_t),
    ct.POINTER(git_odb),
    ct.POINTER(git_oid))(
    ("git_odb_read_header", dll), (
    (1, "len_out"),
    (1, "type_out"),
    (1, "db"),
    (1, "id"),))

# Determine if the given object can be found in the object database.
#
# @param db database to be searched for the given object.
# @param id the object to search for.
# @return 1 if the object was found, 0 otherwise
#
git_odb_exists = CFUNC(ct.c_int,
    ct.POINTER(git_odb),
    ct.POINTER(git_oid))(
    ("git_odb_exists", dll), (
    (1, "db"),
    (1, "id"),))

# Determine if the given object can be found in the object database, with
# extended options.
#
# @param db database to be searched for the given object.
# @param id the object to search for.
# @param flags flags affecting the lookup (see `git_odb_lookup_flags_t`)
# @return 1 if the object was found, 0 otherwise
#
git_odb_exists_ext = CFUNC(ct.c_int,
    ct.POINTER(git_odb),
    ct.POINTER(git_oid),
    ct.c_uint)(
    ("git_odb_exists_ext", dll), (
    (1, "db"),
    (1, "id"),
    (1, "flags"),))

# Determine if an object can be found in the object database by an
# abbreviated object ID.
#
# @param out The full OID of the found object if just one is found.
# @param db The database to be searched for the given object.
# @param short_id A prefix of the id of the object to read.
# @param len The length of the prefix.
# @return 0 if found, GIT_ENOTFOUND if not found, GIT_EAMBIGUOUS if multiple
#         matches were found, other value < 0 if there was a read error.
#
git_odb_exists_prefix = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_odb),
    ct.POINTER(git_oid),
    ct.c_size_t)(
    ("git_odb_exists_prefix", dll), (
    (1, "out"),
    (1, "db"),
    (1, "short_id"),
    (1, "len"),))

# The information about object IDs to query in `git_odb_expand_ids`,
# which will be populated upon return.
#
class git_odb_expand_id(ct.Structure):
    _fields_ = [
    # The object ID to expand
    ("id", git_oid),

    # The length of the object ID (in nibbles, or packets of 4 bits; the
    # number of hex characters)
    #
    ("length", ct.c_ushort),

    # The (optional) type of the object to search for; leave as `0` or set
    # to `GIT_OBJECT_ANY` to query for any object matching the ID.
    #
    ("type", git_object_t),
]

# Determine if one or more objects can be found in the object database
# by their abbreviated object ID and type.
#
# The given array will be updated in place: for each abbreviated ID that is
# unique in the database, and of the given type (if specified),
# the full object ID, object ID length (`GIT_OID_SHA1_HEXSIZE`) and type will be
# written back to the array. For IDs that are not found (or are ambiguous),
# the array entry will be zeroed.
#
# Note that since this function operates on multiple objects, the
# underlying database will not be asked to be reloaded if an object is
# not found (which is unlike other object database operations.)
#
# @param db The database to be searched for the given objects.
# @param ids An array of short object IDs to search for
# @param count The length of the `ids` array
# @return 0 on success or an error code on failure
#
git_odb_expand_ids = CFUNC(ct.c_int,
    ct.POINTER(git_odb),
    ct.POINTER(git_odb_expand_id),
    ct.c_size_t)(
    ("git_odb_expand_ids", dll), (
    (1, "db"),
    (1, "ids"),
    (1, "count"),))

# Refresh the object database to load newly added files.
#
# If the object databases have changed on disk while the library
# is running, this function will force a reload of the underlying
# indexes.
#
# Use this function when you're confident that an external
# application has tampered with the ODB.
#
# NOTE that it is not necessary to call this function at all. The
# library will automatically attempt to refresh the ODB
# when a lookup fails, to see if the looked up object exists
# on disk but hasn't been loaded yet.
#
# @param db database to refresh
# @return 0 on success, error code otherwise
#
git_odb_refresh = CFUNC(ct.c_int,
    ct.POINTER(git_odb))(
    ("git_odb_refresh", dll), (
    (1, "db"),))

# List all objects available in the database
#
# The callback will be called for each object available in the
# database. Note that the objects are likely to be returned in the index
# order, which would make accessing the objects in that order inefficient.
# Return a non-zero value from the callback to stop looping.
#
# @param db database to use
# @param cb the callback to call for each object
# @param payload data to pass to the callback
# @return 0 on success, non-zero callback return value, or error code
#
git_odb_foreach = CFUNC(ct.c_int,
    ct.POINTER(git_odb),
    git_odb_foreach_cb,
    ct.c_void_p)(
    ("git_odb_foreach", dll), (
    (1, "db"),
    (1, "cb"),
    (1, "payload"),))

# Write an object directly into the ODB
#
# This method writes a full object straight into the ODB.
# For most cases, it is preferred to write objects through a write
# stream, which is both faster and less memory intensive, specially
# for big objects.
#
# This method is provided for compatibility with custom backends
# which are not able to support streaming writes
#
# @param out pointer to store the OID result of the write
# @param odb object database where to store the object
# @param data buffer with the data to store
# @param len size of the buffer
# @param type type of the data to store
# @return 0 or an error code
#
git_odb_write = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_odb),
    ct.c_void_p,
    ct.c_size_t,
    git_object_t)(
    ("git_odb_write", dll), (
    (1, "out"),
    (1, "odb"),
    (1, "data"),
    (1, "len"),
    (1, "type"),))

# Open a stream to write an object into the ODB
#
# The type and final length of the object must be specified
# when opening the stream.
#
# The returned stream will be of type `GIT_STREAM_WRONLY`, and it
# won't be effective until `git_odb_stream_finalize_write` is called
# and returns without an error
#
# The stream must always be freed when done with `git_odb_stream_free` or
# will leak memory.
#
# @see git_odb_stream
#
# @param out pointer where to store the stream
# @param db object database where the stream will write
# @param size final size of the object that will be written
# @param type type of the object that will be written
# @return 0 if the stream was created; error code otherwise
#
git_odb_open_wstream = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_odb_stream)),
    ct.POINTER(git_odb),
    git_object_size_t,
    git_object_t)(
    ("git_odb_open_wstream", dll), (
    (1, "out"),
    (1, "db"),
    (1, "size"),
    (1, "type"),))

# Write to an odb stream
#
# This method will fail if the total number of received bytes exceeds the
# size declared with `git_odb_open_wstream()`
#
# @param stream the stream
# @param buffer the data to write
# @param len the buffer's length
# @return 0 if the write succeeded, error code otherwise
#
git_odb_stream_write = CFUNC(ct.c_int,
    ct.POINTER(git_odb_stream),
    git_buffer_t,
    ct.c_size_t)(
    ("git_odb_stream_write", dll), (
    (1, "stream"),
    (1, "buffer"),
    (1, "len"),))

# Finish writing to an odb stream
#
# The object will take its final name and will be available to the
# odb.
#
# This method will fail if the total number of received bytes
# differs from the size declared with `git_odb_open_wstream()`
#
# @param out pointer to store the resulting object's id
# @param stream the stream
# @return 0 on success, an error code otherwise
#
git_odb_stream_finalize_write = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_odb_stream))(
    ("git_odb_stream_finalize_write", dll), (
    (1, "out"),
    (1, "stream"),))

# Read from an odb stream
#
# Most backends don't implement streaming reads
#
# @param stream the stream
# @param buffer a user-allocated buffer to store the data in.
# @param len the buffer's length
# @return 0 if the read succeeded, error code otherwise
#
git_odb_stream_read = CFUNC(ct.c_int,
    ct.POINTER(git_odb_stream),
    git_buffer_t,
    ct.c_size_t)(
    ("git_odb_stream_read", dll), (
    (1, "stream"),
    (1, "buffer"),
    (1, "len"),))

# Free an odb stream
#
# @param stream the stream to free
#
git_odb_stream_free = CFUNC(None,
    ct.POINTER(git_odb_stream))(
    ("git_odb_stream_free", dll), (
    (1, "stream"),))

# Open a stream to read an object from the ODB
#
# Note that most backends do *not* support streaming reads
# because they store their objects as compressed/delta'ed blobs.
#
# It's recommended to use `git_odb_read` instead, which is
# assured to work on all backends.
#
# The returned stream will be of type `GIT_STREAM_RDONLY` and
# will have the following methods:
#
#      - stream->read: read `n` bytes from the stream
#      - stream->free: free the stream
#
# The stream must always be free'd or will leak memory.
#
# @see git_odb_stream
#
# @param out pointer where to store the stream
# @param len pointer where to store the length of the object
# @param type pointer where to store the type of the object
# @param db object database where the stream will read from
# @param oid oid of the object the stream will read from
# @return 0 if the stream was created, error code otherwise
#
git_odb_open_rstream = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_odb_stream)),
    ct.POINTER(ct.c_size_t),
    ct.POINTER(git_object_t),
    ct.POINTER(git_odb),
    ct.POINTER(git_oid))(
    ("git_odb_open_rstream", dll), (
    (1, "out"),
    (1, "len"),
    (1, "type"),
    (1, "db"),
    (1, "oid"),))

# Open a stream for writing a pack file to the ODB.
#
# If the ODB layer understands pack files, then the given
# packfile will likely be streamed directly to disk (and a
# corresponding index created).  If the ODB layer does not
# understand pack files, the objects will be stored in whatever
# format the ODB layer uses.
#
# @see git_odb_writepack
#
# @param out pointer to the writepack functions
# @param db object database where the stream will read from
# @param progress_cb function to call with progress information.
# Be aware that this is called inline with network and indexing operations,
# so performance may be affected.
# @param progress_payload payload for the progress callback
# @return 0 or an error code.
#
git_odb_write_pack = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_odb_writepack)),
    ct.POINTER(git_odb),
    git_indexer_progress_cb,
    ct.c_void_p)(
    ("git_odb_write_pack", dll), (
    (1, "out"),
    (1, "db"),
    (1, "progress_cb"),
    (1, "progress_payload"),))

# Write a `multi-pack-index` file from all the `.pack` files in the ODB.
#
# If the ODB layer understands pack files, then this will create a file called
# `multi-pack-index` next to the `.pack` and `.idx` files, which will contain
# an index of all objects stored in `.pack` files. This will allow for
# O(log n) lookup for n objects (regardless of how many packfiles there
# exist).
#
# @param db object database where the `multi-pack-index` file will be written.
# @return 0 or an error code.
#
git_odb_write_multi_pack_index = CFUNC(ct.c_int,
    ct.POINTER(git_odb))(
    ("git_odb_write_multi_pack_index", dll), (
    (1, "db"),))

# Determine the object-ID (sha1 or sha256 hash) of a data buffer
#
# The resulting OID will be the identifier for the data buffer as if
# the data buffer it were to written to the ODB.
#
# @param out the resulting object-ID.
# @param data data to hash
# @param len size of the data
# @param object_type of the data to hash
# @param oid_type the oid type to hash to
# @return 0 or an error code
#
if defined("GIT_EXPERIMENTAL_SHA256"):
    git_odb_hash = CFUNC(ct.c_int,
        ct.POINTER(git_oid),
        ct.c_void_p,
        ct.c_size_t,
        git_object_t,
        git_oid_t)(
        ("git_odb_hash", dll), (
        (1, "out"),
        (1, "data"),
        (1, "len"),
        (1, "object_type"),
        (1, "oid_type"),))
else:
    git_odb_hash = CFUNC(ct.c_int,
        ct.POINTER(git_oid),
        ct.c_void_p,
        ct.c_size_t,
        git_object_t)(
        ("git_odb_hash", dll), (
        (1, "out"),
        (1, "data"),
        (1, "len"),
        (1, "type"),))
# endif

# Read a file from disk and fill a git_oid with the object id
# that the file would have if it were written to the Object
# Database as an object of the given type (w/o applying filters).
# Similar functionality to git.git's `git hash-object` without
# the `-w` flag, however, with the --no-filters flag.
# If you need filters, see git_repository_hashfile.
#
# @param out oid structure the result is written into.
# @param path file to read and determine object id for
# @param object_type of the data to hash
# @param oid_type the oid type to hash to
# @return 0 or an error code
#
if defined("GIT_EXPERIMENTAL_SHA256"):
    git_odb_hashfile = CFUNC(ct.c_int,
        ct.POINTER(git_oid),
        ct.c_char_p,
        git_object_t,
        git_oid_t)(
        ("git_odb_hashfile", dll), (
        (1, "out"),
        (1, "path"),
        (1, "object_type"),
        (1, "oid_type"),))
else:
    git_odb_hashfile = CFUNC(ct.c_int,
        ct.POINTER(git_oid),
        ct.c_char_p,
        git_object_t)(
        ("git_odb_hashfile", dll), (
        (1, "out"),
        (1, "path"),
        (1, "type"),))
# endif

# Create a copy of an odb_object
#
# The returned copy must be manually freed with `git_odb_object_free`.
# Note that because of an implementation detail, the returned copy will be
# the same pointer as `source`: the object is internally refcounted, so the
# copy still needs to be freed twice.
#
# @param dest pointer where to store the copy
# @param source object to copy
# @return 0 or an error code
#
git_odb_object_dup = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_odb_object)),
    ct.POINTER(git_odb_object))(
    ("git_odb_object_dup", dll), (
    (1, "dest"),
    (1, "source"),))

# Close an ODB object
#
# This method must always be called once a `git_odb_object` is no
# longer needed, otherwise memory will leak.
#
# @param object object to close
#
git_odb_object_free = CFUNC(None,
    ct.POINTER(git_odb_object))(
    ("git_odb_object_free", dll), (
    (1, "object"),))

# Return the OID of an ODB object
#
# This is the OID from which the object was read from
#
# @param object the object
# @return a pointer to the OID
#
git_odb_object_id = CFUNC(ct.POINTER(git_oid),
    ct.POINTER(git_odb_object))(
    ("git_odb_object_id", dll), (
    (1, "object"),))

# Return the data of an ODB object
#
# This is the uncompressed, raw data as read from the ODB,
# without the leading header.
#
# This pointer is owned by the object and shall not be free'd.
#
# @param object the object
# @return a pointer to the data
#
git_odb_object_data = CFUNC(ct.c_void_p,
    ct.POINTER(git_odb_object))(
    ("git_odb_object_data", dll), (
    (1, "object"),))

# Return the size of an ODB object
#
# This is the real size of the `data` buffer, not the
# actual size of the object.
#
# @param object the object
# @return the size
#
git_odb_object_size = CFUNC(ct.c_size_t,
    ct.POINTER(git_odb_object))(
    ("git_odb_object_size", dll), (
    (1, "object"),))

# Return the type of an ODB object
#
# @param object the object
# @return the type
#
git_odb_object_type = CFUNC(git_object_t,
    ct.POINTER(git_odb_object))(
    ("git_odb_object_type", dll), (
    (1, "object"),))

# Add a custom backend to an existing Object DB
#
# The backends are checked in relative ordering, based on the
# value of the `priority` parameter.
#
# Read <sys/odb_backend.h> for more information.
#
# @param odb database to add the backend to
# @param backend pointer to a git_odb_backend instance
# @param priority Value for ordering the backends queue
# @return 0 on success, error code otherwise
#
git_odb_add_backend = CFUNC(ct.c_int,
    ct.POINTER(git_odb),
    ct.POINTER(git_odb_backend),
    ct.c_int)(
    ("git_odb_add_backend", dll), (
    (1, "odb"),
    (1, "backend"),
    (1, "priority"),))

# Add a custom backend to an existing Object DB; this
# backend will work as an alternate.
#
# Alternate backends are always checked for objects *after*
# all the main backends have been exhausted.
#
# The backends are checked in relative ordering, based on the
# value of the `priority` parameter.
#
# Writing is disabled on alternate backends.
#
# Read <sys/odb_backend.h> for more information.
#
# @param odb database to add the backend to
# @param backend pointer to a git_odb_backend instance
# @param priority Value for ordering the backends queue
# @return 0 on success, error code otherwise
#
git_odb_add_alternate = CFUNC(ct.c_int,
    ct.POINTER(git_odb),
    ct.POINTER(git_odb_backend),
    ct.c_int)(
    ("git_odb_add_alternate", dll), (
    (1, "odb"),
    (1, "backend"),
    (1, "priority"),))

# Get the number of ODB backend objects
#
# @param odb object database
# @return number of backends in the ODB
#
git_odb_num_backends = CFUNC(ct.c_size_t,
    ct.POINTER(git_odb))(
    ("git_odb_num_backends", dll), (
    (1, "odb"),))

# Lookup an ODB backend object by index
#
# @param out output pointer to ODB backend at pos
# @param odb object database
# @param pos index into object database backend list
# @return 0 on success, GIT_ENOTFOUND if pos is invalid, other errors < 0
#
git_odb_get_backend = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_odb_backend)),
    ct.POINTER(git_odb),
    ct.c_size_t)(
    ("git_odb_get_backend", dll), (
    (1, "out"),
    (1, "odb"),
    (1, "pos"),))

# Set the git commit-graph for the ODB.
#
# After a successful call, the ownership of the cgraph parameter will be
# transferred to libgit2, and the caller should not free it.
#
# The commit-graph can also be unset by explicitly passing NULL as the cgraph
# parameter.
#
# @param odb object database
# @param cgraph the git commit-graph
# @return 0 on success; error code otherwise
#
git_odb_set_commit_graph = CFUNC(ct.c_int,
    ct.POINTER(git_odb),
    ct.POINTER(git_commit_graph))(
    ("git_odb_set_commit_graph", dll), (
    (1, "odb"),
    (1, "cgraph"),))

# GIT_END_DECL
