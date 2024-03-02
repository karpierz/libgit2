# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common   import *  # noqa
from .buffer   import git_buf
from .oid      import git_oid
from .         import oid
from .types    import git_signature
from .         import oidarray
from .         import strarray
from .         import types
from .         import attr
from .         import blame
from .         import blob
from .types    import git_blob
from .         import checkout
from .         import cherrypick
from .         import clone
from .types    import git_commit
from .         import config
from .         import credential
from .         import credential_helpers
from .         import describe
from .         import diff
from .         import errors
from .         import filter
from .types    import git_index
from .         import index
from .         import indexer
from .         import merge
from .types    import git_object_t
from .         import proxy
from .         import rebase
from .types    import git_reference_t
from .         import refs
from .types    import git_remote_head
from .         import remote
from .         import revert
from .types    import git_repository
from .         import repository
from .         import revparse
from .         import stash
from .         import status
from .         import submodule
from .types    import git_worktree
from .types    import git_treebuilder
from .         import trace
from .types    import git_writestream
from .         import worktree

#
# Users can avoid deprecated functions by defining `GIT_DEPRECATE_HARD`.
#
if not defined("GIT_DEPRECATE_HARD"):

    # The credential structures are now opaque by default, and their
    # definition has moved into the `sys/credential.h` header; include
    # them here for backward compatibility.
    #
    #include "sys/credential.h"

    # @file git2/deprecated.h
    # @brief libgit2 deprecated functions and values
    # @ingroup Git

    # GIT_BEGIN_DECL

    # @name Deprecated Attribute Constants
    #
    # These enumeration values are retained for backward compatibility.
    # The newer versions of these functions should be preferred in all
    # new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    GIT_ATTR_UNSPECIFIED_T = attr.GIT_ATTR_VALUE_UNSPECIFIED
    GIT_ATTR_TRUE_T        = attr.GIT_ATTR_VALUE_TRUE
    GIT_ATTR_FALSE_T       = attr.GIT_ATTR_VALUE_FALSE
    GIT_ATTR_VALUE_T       = attr.GIT_ATTR_VALUE_STRING

    GIT_ATTR_TRUE        = lambda attr: attr.GIT_ATTR_IS_TRUE(attr)
    GIT_ATTR_FALSE       = lambda attr: attr.GIT_ATTR_IS_FALSE(attr)
    GIT_ATTR_UNSPECIFIED = lambda attr: attr.GIT_ATTR_IS_UNSPECIFIED(attr)

    git_attr_t = attr.git_attr_value_t

    # @name Deprecated Blob Functions and Constants
    #
    # These functions and enumeration values are retained for backward
    # compatibility.  The newer versions of these functions and values
    # should be preferred in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    GIT_BLOB_FILTER_ATTTRIBUTES_FROM_HEAD = blob.GIT_BLOB_FILTER_ATTRIBUTES_FROM_HEAD

    git_blob_create_fromworkdir = CFUNC(ct.c_int,
        ct.POINTER(git_oid),
        ct.POINTER(git_repository),
        ct.c_char_p)(
        ("git_blob_create_fromworkdir", dll), (
        (1, "id"),
        (1, "repo"),
        (1, "relative_path"),))

    git_blob_create_fromdisk = CFUNC(ct.c_int,
        ct.POINTER(git_oid),
        ct.POINTER(git_repository),
        ct.c_char_p)(
        ("git_blob_create_fromdisk", dll), (
        (1, "id"),
        (1, "repo"),
        (1, "path"),))

    git_blob_create_fromstream = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_writestream)),
        ct.POINTER(git_repository),
        ct.c_char_p)(
        ("git_blob_create_fromstream", dll), (
        (1, "out"),
        (1, "repo"),
        (1, "hintpath"),))

    git_blob_create_fromstream_commit = CFUNC(ct.c_int,
        ct.POINTER(git_oid),
        ct.POINTER(git_writestream))(
        ("git_blob_create_fromstream_commit", dll), (
        (1, "out"),
        (1, "stream"),))

    git_blob_create_frombuffer = CFUNC(ct.c_int,
        ct.POINTER(git_oid),
        ct.POINTER(git_repository),
        ct.c_void_p,
        ct.c_size_t)(
        ("git_blob_create_frombuffer", dll), (
        (1, "id"),
        (1, "repo"),
        (1, "buffer"),
        (1, "len"),))

    # Deprecated in favor of `git_blob_filter`.
    #
    # @deprecated Use git_blob_filter
    # @see git_blob_filter
    #
    git_blob_filtered_content = CFUNC(ct.c_int,
        ct.POINTER(git_buf),
        ct.POINTER(git_blob),
        ct.c_char_p,
        ct.c_int)(
        ("git_blob_filtered_content", dll), (
        (1, "out"),
        (1, "blob"),
        (1, "as_path"),
        (1, "check_for_binary_data"),))

    # @name Deprecated Filter Functions
    #
    # These functions are retained for backward compatibility.  The
    # newer versions of these functions should be preferred in all
    # new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    # Deprecated in favor of `git_filter_list_stream_buffer`.
    #
    # @deprecated Use git_filter_list_stream_buffer
    # @see Use git_filter_list_stream_buffer
    #
    git_filter_list_stream_data = CFUNC(ct.c_int,
        ct.POINTER(filter.git_filter_list),
        ct.POINTER(git_buf),
        ct.POINTER(git_writestream))(
        ("git_filter_list_stream_data", dll), (
        (1, "filters"),
        (1, "data"),
        (1, "target"),))

    # Deprecated in favor of `git_filter_list_apply_to_buffer`.
    #
    # @deprecated Use git_filter_list_apply_to_buffer
    # @see Use git_filter_list_apply_to_buffer
    #
    git_filter_list_apply_to_data = CFUNC(ct.c_int,
        ct.POINTER(git_buf),
        ct.POINTER(filter.git_filter_list),
        ct.POINTER(git_buf))(
        ("git_filter_list_apply_to_data", dll), (
        (1, "out"),
        (1, "filters"),
        (1, "inp"),))

    # @name Deprecated Tree Functions
    #
    # These functions are retained for backward compatibility.  The
    # newer versions of these functions and values should be preferred
    # in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    # Write the contents of the tree builder as a tree object.
    # This is an alias of `git_treebuilder_write` and is preserved
    # for backward compatibility.
    #
    # This function is deprecated, but there is no plan to remove this
    # function at this time.
    #
    # @deprecated Use git_treebuilder_write
    # @see git_treebuilder_write
    #
    git_treebuilder_write_with_buffer = CFUNC(ct.c_int,
        ct.POINTER(git_oid),
        ct.POINTER(git_treebuilder),
        ct.POINTER(git_buf))(
        ("git_treebuilder_write_with_buffer", dll), (
        (1, "oid"),
        (1, "bld"),
        (1, "tree"),))

    # @name Deprecated Buffer Functions
    #
    # These functions and enumeration values are retained for backward
    # compatibility.  The newer versions of these functions should be
    # preferred in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    # Static initializer for git_buf from static buffer
    #
    GIT_BUF_INIT_CONST = lambda str, len: (ct.c_char_p(str), 0, ct.c_size_t(len))

    # Resize the buffer allocation to make more space.
    #
    # This will attempt to grow the buffer to accommodate the target size.
    #
    # If the buffer refers to memory that was not allocated by libgit2 (i.e.
    # the `asize` field is zero), then `ptr` will be replaced with a newly
    # allocated block of data.  Be careful so that memory allocated by the
    # caller is not lost.  As a special variant, if you pass `target_size` as
    # 0 and the memory is not allocated by libgit2, this will allocate a new
    # buffer of size `size` and copy the external data into it.
    #
    # Currently, this will never shrink a buffer, only expand it.
    #
    # If the allocation fails, this will return an error and the buffer will be
    # marked as invalid for future operations, invaliding the contents.
    #
    # @param buffer The buffer to be resized; may or may not be allocated yet
    # @param target_size The desired available size
    # @return 0 on success, -1 on allocation failure
    #
    git_buf_grow = CFUNC(ct.c_int,
        ct.POINTER(git_buf),
        ct.c_size_t)(
        ("git_buf_grow", dll), (
        (1, "buffer"),
        (1, "target_size"),))

    # Set buffer to a copy of some raw data.
    #
    # @param buffer The buffer to set
    # @param data The data to copy into the buffer
    # @param datalen The length of the data to copy into the buffer
    # @return 0 on success, -1 on allocation failure
    #
    git_buf_set = CFUNC(ct.c_int,
        ct.POINTER(git_buf),
        ct.c_void_p,
        ct.c_size_t)(
        ("git_buf_set", dll), (
        (1, "buffer"),
        (1, "data"),
        (1, "datalen"),))

    # Check quickly if buffer looks like it contains binary data
    #
    # @param buffer Buffer to check
    # @return 1 if buffer looks like non-text data
    #
    git_buf_is_binary = CFUNC(ct.c_int,
        ct.POINTER(git_buf))(
        ("git_buf_is_binary", dll), (
        (1, "buffer"),))

    # Check quickly if buffer contains a NUL byte
    #
    # @param buffer Buffer to check
    # @return 1 if buffer contains a NUL byte
    #
    git_buf_contains_nul = CFUNC(ct.c_int,
        ct.POINTER(git_buf))(
        ("git_buf_contains_nul", dll), (
        (1, "buffer"),))

    # Free the memory referred to by the git_buf.  This is an alias of
    # `git_buf_dispose` and is preserved for backward compatibility.
    #
    # This function is deprecated, but there is no plan to remove this
    # function at this time.
    #
    # @deprecated Use git_buf_dispose
    # @see git_buf_dispose
    #
    git_buf_free = CFUNC(None,
        ct.POINTER(git_buf))(
        ("git_buf_free", dll), (
        (1, "buffer"),))

    # @name Deprecated Commit Definitions
    #

    # Provide a commit signature during commit creation.
    #
    # Callers should instead define a `git_commit_create_cb` that
    # generates a commit buffer using `git_commit_create_buffer`, sign
    # that buffer and call `git_commit_create_with_signature`.
    #
    # @deprecated use a `git_commit_create_cb` instead
    #
    git_commit_signing_cb = CFUNC(ct.c_int,
        ct.POINTER(git_buf),  # signature
        ct.POINTER(git_buf),  # signature_field
        ct.c_char_p,          # commit_content
        ct.c_void_p)          # payload

    # @name Deprecated Config Functions and Constants
    #

    GIT_CVAR_FALSE  = config.GIT_CONFIGMAP_FALSE
    GIT_CVAR_TRUE   = config.GIT_CONFIGMAP_TRUE
    GIT_CVAR_INT32  = config.GIT_CONFIGMAP_INT32
    GIT_CVAR_STRING = config.GIT_CONFIGMAP_STRING

    git_cvar_map = config.git_configmap

    # @name Deprecated Diff Functions and Constants
    #
    # These functions and enumeration values are retained for backward
    # compatibility.  The newer versions of these functions and values
    # should be preferred in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    # Formatting options for diff e-mail generation
    #
    git_diff_format_email_flags_t = ct.c_int
    (
        # Normal patch, the default
        GIT_DIFF_FORMAT_EMAIL_NONE,

        # Don't insert "[PATCH]" in the subject header
        GIT_DIFF_FORMAT_EMAIL_EXCLUDE_SUBJECT_PATCH_MARKER,

    ) = (0, 1 << 0)

    # Options for controlling the formatting of the generated e-mail.
    #
    class git_diff_format_email_options(ct.Structure):
        _fields_ = [
        ("version", ct.c_uint),

        # see `git_diff_format_email_flags_t` above
        ("flags", ct.c_uint32),

        # This patch number
        ("patch_no", ct.c_size_t),

        # Total number of patches in this series
        ("total_patches", ct.c_size_t),

        # id to use for the commit
        ("id", ct.POINTER(git_oid)),

        # Summary of the change
        ("summary", ct.c_char_p),

        # Commit message's body
        ("body", ct.c_char_p),

        # Author of the change
        ("author", ct.POINTER(git_signature)),
    ]

    GIT_DIFF_FORMAT_EMAIL_OPTIONS_VERSION = 1
    # GIT_DIFF_FORMAT_EMAIL_OPTIONS_INIT = { GIT_DIFF_FORMAT_EMAIL_OPTIONS_VERSION,
    #                                        0, 1, 1,
    #                                        NULL, NULL, NULL, NULL }

    # Create an e-mail ready patch from a diff.
    #
    # @deprecated git_email_create_from_diff
    # @see git_email_create_from_diff
    #
    git_diff_format_email = CFUNC(ct.c_int,
        ct.POINTER(git_buf),
        ct.POINTER(diff.git_diff),
        ct.POINTER(git_diff_format_email_options))(
        ("git_diff_format_email", dll), (
        (1, "out"),
        (1, "diff"),
        (1, "opts"),))

    # Create an e-mail ready patch for a commit.
    #
    # @deprecated git_email_create_from_commit
    # @see git_email_create_from_commit
    #
    git_diff_commit_as_email = CFUNC(ct.c_int,
        ct.POINTER(git_buf),
        ct.POINTER(git_repository),
        ct.POINTER(git_commit),
        ct.c_size_t,
        ct.c_size_t,
        ct.c_uint32,
        ct.POINTER(diff.git_diff_options))(
        ("git_diff_commit_as_email", dll), (
        (1, "out"),
        (1, "repo"),
        (1, "commit"),
        (1, "patch_no"),
        (1, "total_patches"),
        (1, "flags"),
        (1, "diff_opts"),))

    # Initialize git_diff_format_email_options structure
    #
    # Initializes a `git_diff_format_email_options` with default values. Equivalent
    # to creating an instance with GIT_DIFF_FORMAT_EMAIL_OPTIONS_INIT.
    #
    # @param opts The `git_blame_options` struct to initialize.
    # @param version The struct version; pass `GIT_DIFF_FORMAT_EMAIL_OPTIONS_VERSION`.
    # @return Zero on success; -1 on failure.
    #
    git_diff_format_email_options_init = CFUNC(ct.c_int,
        ct.POINTER(git_diff_format_email_options),
        ct.c_uint)(
        ("git_diff_format_email_options_init", dll), (
        (1, "opts"),
        (1, "version"),))

    # @name Deprecated Error Functions and Constants
    #
    # These functions and enumeration values are retained for backward
    # compatibility.  The newer versions of these functions and values
    # should be preferred in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    GITERR_NONE       =  errors.GIT_ERROR_NONE
    GITERR_NOMEMORY   =  errors.GIT_ERROR_NOMEMORY
    GITERR_OS         =  errors.GIT_ERROR_OS
    GITERR_INVALID    =  errors.GIT_ERROR_INVALID
    GITERR_REFERENCE  =  errors.GIT_ERROR_REFERENCE
    GITERR_ZLIB       =  errors.GIT_ERROR_ZLIB
    GITERR_REPOSITORY =  errors.GIT_ERROR_REPOSITORY
    GITERR_CONFIG     =  errors.GIT_ERROR_CONFIG
    GITERR_REGEX      =  errors.GIT_ERROR_REGEX
    GITERR_ODB        =  errors.GIT_ERROR_ODB
    GITERR_INDEX      =  errors.GIT_ERROR_INDEX
    GITERR_OBJECT     =  errors.GIT_ERROR_OBJECT
    GITERR_NET        =  errors.GIT_ERROR_NET
    GITERR_TAG        =  errors.GIT_ERROR_TAG
    GITERR_TREE       =  errors.GIT_ERROR_TREE
    GITERR_INDEXER    =  errors.GIT_ERROR_INDEXER
    GITERR_SSL        =  errors.GIT_ERROR_SSL
    GITERR_SUBMODULE  =  errors.GIT_ERROR_SUBMODULE
    GITERR_THREAD     =  errors.GIT_ERROR_THREAD
    GITERR_STASH      =  errors.GIT_ERROR_STASH
    GITERR_CHECKOUT   =  errors.GIT_ERROR_CHECKOUT
    GITERR_FETCHHEAD  =  errors.GIT_ERROR_FETCHHEAD
    GITERR_MERGE      =  errors.GIT_ERROR_MERGE
    GITERR_SSH        =  errors.GIT_ERROR_SSH
    GITERR_FILTER     =  errors.GIT_ERROR_FILTER
    GITERR_REVERT     =  errors.GIT_ERROR_REVERT
    GITERR_CALLBACK   =  errors.GIT_ERROR_CALLBACK
    GITERR_CHERRYPICK =  errors.GIT_ERROR_CHERRYPICK
    GITERR_DESCRIBE   =  errors.GIT_ERROR_DESCRIBE
    GITERR_REBASE     =  errors.GIT_ERROR_REBASE
    GITERR_FILESYSTEM =  errors.GIT_ERROR_FILESYSTEM
    GITERR_PATCH      =  errors.GIT_ERROR_PATCH
    GITERR_WORKTREE   =  errors.GIT_ERROR_WORKTREE
    GITERR_SHA1       =  errors.GIT_ERROR_SHA

    GIT_ERROR_SHA1 = errors.GIT_ERROR_SHA

    # Return the last `git_error` object that was generated for the
    # current thread.  This is an alias of `git_error_last` and is
    # preserved for backward compatibility.
    #
    # This function is deprecated, but there is no plan to remove this
    # function at this time.
    #
    # @deprecated Use git_error_last
    # @see git_error_last
    #
    giterr_last = CFUNC(ct.POINTER(errors.git_error))(
        ("giterr_last", dll),)

    # Clear the last error.  This is an alias of `git_error_last` and is
    # preserved for backward compatibility.
    #
    # This function is deprecated, but there is no plan to remove this
    # function at this time.
    #
    # @deprecated Use git_error_clear
    # @see git_error_clear
    #
    giterr_clear = CFUNC(None)(
        ("giterr_clear", dll),)

    # Sets the error message to the given string.  This is an alias of
    # `git_error_set_str` and is preserved for backward compatibility.
    #
    # This function is deprecated, but there is no plan to remove this
    # function at this time.
    #
    # @deprecated Use git_error_set_str
    # @see git_error_set_str
    #
    giterr_set_str = CFUNC(None,
        ct.c_int,
        ct.c_char_p)(
        ("giterr_set_str", dll), (
        (1, "error_class"),
        (1, "string"),))

    # Indicates that an out-of-memory situation occurred.  This is an alias
    # of `git_error_set_oom` and is preserved for backward compatibility.
    #
    # This function is deprecated, but there is no plan to remove this
    # function at this time.
    #
    # @deprecated Use git_error_set_oom
    # @see git_error_set_oom
    #
    giterr_set_oom = CFUNC(None)(
        ("giterr_set_oom", dll),)

    # @name Deprecated Index Functions and Constants
    #
    # These functions and enumeration values are retained for backward
    # compatibility.  The newer versions of these values should be
    # preferred in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    GIT_IDXENTRY_NAMEMASK          = index.GIT_INDEX_ENTRY_NAMEMASK
    GIT_IDXENTRY_STAGEMASK         = index.GIT_INDEX_ENTRY_STAGEMASK
    GIT_IDXENTRY_STAGESHIFT        = index.GIT_INDEX_ENTRY_STAGESHIFT

    # The git_indxentry_flag_t enum
    GIT_IDXENTRY_EXTENDED          = index.GIT_INDEX_ENTRY_EXTENDED
    GIT_IDXENTRY_VALID             = index.GIT_INDEX_ENTRY_VALID

    GIT_IDXENTRY_STAGE             = lambda E:    index.GIT_INDEX_ENTRY_STAGE(E)
    GIT_IDXENTRY_STAGE_SET         = lambda E, S: index.GIT_INDEX_ENTRY_STAGE_SET(E,S)

    # The git_idxentry_extended_flag_t enum
    GIT_IDXENTRY_INTENT_TO_ADD     = index.GIT_INDEX_ENTRY_INTENT_TO_ADD
    GIT_IDXENTRY_SKIP_WORKTREE     = index.GIT_INDEX_ENTRY_SKIP_WORKTREE
    GIT_IDXENTRY_EXTENDED_FLAGS    = (index.GIT_INDEX_ENTRY_INTENT_TO_ADD | index.GIT_INDEX_ENTRY_SKIP_WORKTREE)
    GIT_IDXENTRY_EXTENDED2         = (1 << 15)
    GIT_IDXENTRY_UPDATE            = (1 << 0)
    GIT_IDXENTRY_REMOVE            = (1 << 1)
    GIT_IDXENTRY_UPTODATE          = (1 << 2)
    GIT_IDXENTRY_ADDED             = (1 << 3)
    GIT_IDXENTRY_HASHED            = (1 << 4)
    GIT_IDXENTRY_UNHASHED          = (1 << 5)
    GIT_IDXENTRY_WT_REMOVE         = (1 << 6)
    GIT_IDXENTRY_CONFLICTED        = (1 << 7)
    GIT_IDXENTRY_UNPACKED          = (1 << 8)
    GIT_IDXENTRY_NEW_SKIP_WORKTREE = (1 << 9)

    # The git_index_capability_t enum
    GIT_INDEXCAP_IGNORE_CASE       = index.GIT_INDEX_CAPABILITY_IGNORE_CASE
    GIT_INDEXCAP_NO_FILEMODE       = index.GIT_INDEX_CAPABILITY_NO_FILEMODE
    GIT_INDEXCAP_NO_SYMLINKS       = index.GIT_INDEX_CAPABILITY_NO_SYMLINKS
    GIT_INDEXCAP_FROM_OWNER        = index.GIT_INDEX_CAPABILITY_FROM_OWNER

    git_index_add_frombuffer = CFUNC(ct.c_int,
        ct.POINTER(git_index),
        ct.POINTER(index.git_index_entry),
        ct.c_void_p,
        ct.c_size_t)(
        ("git_index_add_frombuffer", dll), (
        (1, "index"),
        (1, "entry"),
        (1, "buffer"),
        (1, "len"),))

    # @name Deprecated Object Constants
    #
    # These enumeration values are retained for backward compatibility.  The
    # newer versions of these values should be preferred in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    git_otype = git_object_t

    GIT_OBJ_ANY       = types.GIT_OBJECT_ANY
    GIT_OBJ_BAD       = types.GIT_OBJECT_INVALID
    GIT_OBJ__EXT1     = 0
    GIT_OBJ_COMMIT    = types.GIT_OBJECT_COMMIT
    GIT_OBJ_TREE      = types.GIT_OBJECT_TREE
    GIT_OBJ_BLOB      = types.GIT_OBJECT_BLOB
    GIT_OBJ_TAG       = types.GIT_OBJECT_TAG
    GIT_OBJ__EXT2     = 5
    GIT_OBJ_OFS_DELTA = types.GIT_OBJECT_OFS_DELTA
    GIT_OBJ_REF_DELTA = types.GIT_OBJECT_REF_DELTA

    # Get the size in bytes for the structure which
    # acts as an in-memory representation of any given
    # object type.
    #
    # For all the core types, this would the equivalent
    # of calling `sizeof(git_commit)` if the core types
    # were not opaque on the external API.
    #
    # @param type object type to get its size
    # @return size in bytes of the object
    #
    git_object__size = CFUNC(ct.c_size_t,
        git_object_t)(
        ("git_object__size", dll), (
        (1, "type"),))

    # @name Deprecated Remote Functions
    #
    # These functions are retained for backward compatibility.  The newer
    # versions of these functions should be preferred in all new code.
    #
    # There is no plan to remove these backward compatibility functions at
    # this time.
    #

    # Ensure the remote name is well-formed.
    #
    # @deprecated Use git_remote_name_is_valid
    # @param remote_name name to be checked.
    # @return 1 if the reference name is acceptable; 0 if it isn't
    #
    git_remote_is_valid_name = CFUNC(ct.c_int,
        ct.c_char_p)(
        ("git_remote_is_valid_name", dll), (
        (1, "remote_name"),))

    # @name Deprecated Reference Functions and Constants
    #
    # These functions and enumeration values are retained for backward
    # compatibility.  The newer versions of these values should be
    # preferred in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    # Basic type of any Git reference.
    git_ref_t                 = git_reference_t
    git_reference_normalize_t = refs.git_reference_format_t

    GIT_REF_INVALID  = types.GIT_REFERENCE_INVALID
    GIT_REF_OID      = types.GIT_REFERENCE_DIRECT
    GIT_REF_SYMBOLIC = types.GIT_REFERENCE_SYMBOLIC
    GIT_REF_LISTALL  = types.GIT_REFERENCE_ALL

    GIT_REF_FORMAT_NORMAL            = refs.GIT_REFERENCE_FORMAT_NORMAL
    GIT_REF_FORMAT_ALLOW_ONELEVEL    = refs.GIT_REFERENCE_FORMAT_ALLOW_ONELEVEL
    GIT_REF_FORMAT_REFSPEC_PATTERN   = refs.GIT_REFERENCE_FORMAT_REFSPEC_PATTERN
    GIT_REF_FORMAT_REFSPEC_SHORTHAND = refs.GIT_REFERENCE_FORMAT_REFSPEC_SHORTHAND

    # Ensure the reference name is well-formed.
    #
    # Valid reference names must follow one of two patterns:
    #
    # 1. Top-level names must contain only capital letters and underscores,
    #    and must begin and end with a letter. (e.g. "HEAD", "ORIG_HEAD").
    # 2. Names prefixed with "refs/" can be almost anything.  You must avoid
    #    the characters '~', '^', ':', '\\', '?', '[', and '*', and the
    #    sequences ".." and "@{" which have special meaning to revparse.
    #
    # @deprecated Use git_reference_name_is_valid
    # @param refname name to be checked.
    # @return 1 if the reference name is acceptable; 0 if it isn't
    #
    git_reference_is_valid_name = CFUNC(ct.c_int,
        ct.c_char_p)(
        ("git_reference_is_valid_name", dll), (
        (1, "refname"),))

    git_tag_create_frombuffer = CFUNC(ct.c_int,
        ct.POINTER(git_oid),
        ct.POINTER(git_repository),
        git_buffer_t,
        ct.c_int)(
        ("git_tag_create_frombuffer", dll), (
        (1, "oid"),
        (1, "repo"),
        (1, "buffer"),
        (1, "force"),))

    # @name Deprecated Revspec Constants
    #
    # These enumeration values are retained for backward compatibility.
    # The newer versions of these values should be preferred in all new
    # code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    git_revparse_mode_t = revparse.git_revspec_t

    GIT_REVPARSE_SINGLE     = revparse.GIT_REVSPEC_SINGLE
    GIT_REVPARSE_RANGE      = revparse.GIT_REVSPEC_RANGE
    GIT_REVPARSE_MERGE_BASE = revparse.GIT_REVSPEC_MERGE_BASE

    # @name Deprecated Credential Types
    #
    # These types are retained for backward compatibility.  The newer
    # versions of these values should be preferred in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    git_cred                    = credential.git_credential
    git_cred_userpass_plaintext = credential.git_credential_userpass_plaintext
    git_cred_username           = credential.git_credential_username
    git_cred_default            = credential.git_credential_default
    git_cred_ssh_key            = credential.git_credential_ssh_key
    git_cred_ssh_interactive    = credential.git_credential_ssh_interactive
    git_cred_ssh_custom         = credential.git_credential_ssh_custom

    git_cred_acquire_cb               = credential.git_credential_acquire_cb
    git_cred_sign_callback            = credential.git_credential_sign_cb
    git_cred_sign_cb                  = credential.git_credential_sign_cb
    git_cred_ssh_interactive_callback = credential.git_credential_ssh_interactive_cb
    git_cred_ssh_interactive_cb       = credential.git_credential_ssh_interactive_cb

    git_credtype_t = credential.git_credential_t

    GIT_CREDTYPE_USERPASS_PLAINTEXT = credential.GIT_CREDENTIAL_USERPASS_PLAINTEXT
    GIT_CREDTYPE_SSH_KEY            = credential.GIT_CREDENTIAL_SSH_KEY
    GIT_CREDTYPE_SSH_CUSTOM         = credential.GIT_CREDENTIAL_SSH_CUSTOM
    GIT_CREDTYPE_DEFAULT            = credential.GIT_CREDENTIAL_DEFAULT
    GIT_CREDTYPE_SSH_INTERACTIVE    = credential.GIT_CREDENTIAL_SSH_INTERACTIVE
    GIT_CREDTYPE_USERNAME           = credential.GIT_CREDENTIAL_USERNAME
    GIT_CREDTYPE_SSH_MEMORY         = credential.GIT_CREDENTIAL_SSH_MEMORY

    git_cred_free = CFUNC(None,
        ct.POINTER(credential.git_credential))(
        ("git_cred_free", dll), (
        (1, "cred"),))

    git_cred_has_username = CFUNC(ct.c_int,
        ct.POINTER(credential.git_credential))(
        ("git_cred_has_username", dll), (
        (1, "cred"),))

    git_cred_get_username = CFUNC(ct.c_char_p,
        ct.POINTER(credential.git_credential))(
        ("git_cred_get_username", dll), (
        (1, "cred"),))

    git_cred_userpass_plaintext_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(credential.git_credential)),
        ct.c_char_p,
        ct.c_char_p)(
        ("git_cred_userpass_plaintext_new", dll), (
        (1, "out"),
        (1, "username"),
        (1, "password"),))

    git_cred_default_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(credential.git_credential)))(
        ("git_cred_default_new", dll), (
        (1, "out"),))

    git_cred_username_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(credential.git_credential)),
        ct.c_char_p)(
        ("git_cred_username_new", dll), (
        (1, "out"),
        (1, "username"),))

    git_cred_ssh_key_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(credential.git_credential)),
        ct.c_char_p,
        ct.c_char_p,
        ct.c_char_p,
        ct.c_char_p)(  # TODO: ??? maybe ct.POINTER(ct.c_char) ?
        ("git_cred_ssh_key_new", dll), (
        (1, "out"),
        (1, "username"),
        (1, "publickey "),
        (1, "privatekey"),
        (1, "passphrase"),))

    git_cred_ssh_key_memory_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(credential.git_credential)),
        ct.c_char_p,
        ct.c_char_p,   # TODO: ??? maybe ct.POINTER(ct.c_char) ?
        ct.c_char_p,   # TODO: ??? maybe ct.POINTER(ct.c_char) ?
        ct.c_char_p)(  # TODO: ??? maybe ct.POINTER(ct.c_char) ?
        ("git_cred_ssh_key_memory_new", dll), (
        (1, "out"),
        (1, "username"),
        (1, "publickey"),
        (1, "privatekey"),
        (1, "passphrase"),))

    git_cred_ssh_interactive_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(credential.git_credential)),
        ct.c_char_p,
        credential.git_credential_ssh_interactive_cb,
        ct.c_void_p)(
        ("git_cred_ssh_interactive_new", dll), (
        (1, "out"),
        (1, "username"),
        (1, "prompt_callback"),
        (1, "payload"),))

    git_cred_ssh_key_from_agent = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(credential.git_credential)),
        ct.c_char_p)(
        ("git_cred_ssh_key_from_agent", dll), (
        (1, "out"),
        (1, "username"),))

    git_cred_ssh_custom_new = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(credential.git_credential)),
        ct.c_char_p,
        git_buffer_t,
        ct.c_size_t,
        credential.git_credential_sign_cb,
        ct.c_void_p)(
        ("git_cred_ssh_custom_new", dll), (
        (1, "out"),
        (1, "username"),
        (1, "publickey"),
        (1, "publickey_len"),
        (1, "sign_callback"),
        (1, "payload"),))

    # Deprecated Credential Helper Types

    git_cred_userpass_payload = credential_helpers.git_credential_userpass_payload

    git_cred_userpass = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(credential.git_credential)),
        ct.c_char_p,
        ct.c_char_p,
        ct.c_uint,
        ct.c_void_p)(
        ("git_cred_userpass", dll), (
        (1, "out"),
        (1, "url"),
        (1, "user_from_url"),
        (1, "allowed_types"),
        (1, "payload"),))

    # @name Deprecated Trace Callback Types
    #
    # These types are retained for backward compatibility.  The newer
    # versions of these values should be preferred in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    git_trace_callback = trace.git_trace_cb

    # @name Deprecated Object ID Types
    #
    # These types are retained for backward compatibility.  The newer
    # versions of these values should be preferred in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    if not defined("GIT_EXPERIMENTAL_SHA256"):
        GIT_OID_RAWSZ    = oid.GIT_OID_SHA1_SIZE
        GIT_OID_HEXSZ    = oid.GIT_OID_SHA1_HEXSIZE
        GIT_OID_HEX_ZERO = oid.GIT_OID_SHA1_HEXZERO
    # endif

    git_oid_iszero = CFUNC(ct.c_int,
        ct.POINTER(git_oid))(
        ("git_oid_iszero", dll), (
        (1, "id"),))

    # @name Deprecated OID Array Functions
    #
    # These types are retained for backward compatibility.  The newer
    # versions of these values should be preferred in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    # Free the memory referred to by the git_oidarray.  This is an alias of
    # `git_oidarray_dispose` and is preserved for backward compatibility.
    #
    # This function is deprecated, but there is no plan to remove this
    # function at this time.
    #
    # @deprecated Use git_oidarray_dispose
    # @see git_oidarray_dispose
    #
    git_oidarray_free = CFUNC(None,
        ct.POINTER(oidarray.git_oidarray))(
        ("git_oidarray_free", dll), (
        (1, "array"),))

    # @name Deprecated Transfer Progress Types
    #
    # These types are retained for backward compatibility.  The newer
    # versions of these values should be preferred in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    # This structure is used to provide callers information about the
    # progress of indexing a packfile.
    #
    # This type is deprecated, but there is no plan to remove this
    # type definition at this time.
    #
    git_transfer_progress = indexer.git_indexer_progress

    # Type definition for progress callbacks during indexing.
    #
    # This type is deprecated, but there is no plan to remove this
    # type definition at this time.
    #
    git_transfer_progress_cb = indexer.git_indexer_progress_cb

    # Type definition for push transfer progress callbacks.
    #
    # This type is deprecated, but there is no plan to remove this
    # type definition at this time.
    #
    git_push_transfer_progress = remote.git_push_transfer_progress_cb

    # The type of a remote completion event
    git_remote_completion_type = remote.git_remote_completion_t

    # Callback for listing the remote heads
    #
    git_headlist_cb = GIT_CALLBACK(ct.c_int,
        ct.POINTER(git_remote_head),  # rhead
        ct.c_void_p)                  # payload

    # @name Deprecated String Array Functions
    #
    # These types are retained for backward compatibility.  The newer
    # versions of these values should be preferred in all new code.
    #
    # There is no plan to remove these backward compatibility values at
    # this time.
    #

    # Copy a string array object from source to target.
    #
    # This function is deprecated, but there is no plan to remove this
    # function at this time.
    #
    # @param tgt target
    # @param src source
    # @return 0 on success, < 0 on allocation failure
    #
    git_strarray_copy = CFUNC(ct.c_int,
        ct.POINTER(strarray.git_strarray),
        ct.POINTER(strarray.git_strarray))(
        ("git_strarray_copy", dll), (
        (1, "tgt"),
        (1, "src"),))

    # Free the memory referred to by the git_strarray.  This is an alias of
    # `git_strarray_dispose` and is preserved for backward compatibility.
    #
    # This function is deprecated, but there is no plan to remove this
    # function at this time.
    #
    # @deprecated Use git_strarray_dispose
    # @see git_strarray_dispose
    #
    git_strarray_free = CFUNC(None,
        ct.POINTER(strarray.git_strarray))(
        ("git_strarray_free", dll), (
        (1, "array"),))

    # @name Deprecated Options Initialization Functions
    #
    # These functions are retained for backward compatibility.  The newer
    # versions of these functions should be preferred in all new code.
    #
    # There is no plan to remove these backward compatibility functions at
    # this time.

    git_blame_init_options = CFUNC(ct.c_int,
        ct.POINTER(blame.git_blame_options),
        ct.c_uint)(
        ("git_blame_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_checkout_init_options = CFUNC(ct.c_int,
        ct.POINTER(checkout.git_checkout_options),
        ct.c_uint)(
        ("git_checkout_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_cherrypick_init_options = CFUNC(ct.c_int,
        ct.POINTER(cherrypick.git_cherrypick_options),
        ct.c_uint)(
        ("git_cherrypick_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_clone_init_options = CFUNC(ct.c_int,
        ct.POINTER(clone.git_clone_options),
        ct.c_uint)(
        ("git_clone_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_describe_init_options = CFUNC(ct.c_int,
        ct.POINTER(describe.git_describe_options),
        ct.c_uint)(
        ("git_describe_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_describe_init_format_options = CFUNC(ct.c_int,
        ct.POINTER(describe.git_describe_format_options),
        ct.c_uint)(
        ("git_describe_init_format_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_diff_init_options = CFUNC(ct.c_int,
        ct.POINTER(diff.git_diff_options),
        ct.c_uint)(
        ("git_diff_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_diff_find_init_options = CFUNC(ct.c_int,
        ct.POINTER(diff.git_diff_find_options),
        ct.c_uint)(
        ("git_diff_find_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_diff_format_email_init_options = CFUNC(ct.c_int,
        ct.POINTER(git_diff_format_email_options),
        ct.c_uint)(
        ("git_diff_format_email_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_diff_patchid_init_options = CFUNC(ct.c_int,
        ct.POINTER(diff.git_diff_patchid_options),
        ct.c_uint)(
        ("git_diff_patchid_options_init", dll), (
        (1, "opts"),
        (1, "version"),))

    git_fetch_init_options = CFUNC(ct.c_int,
        ct.POINTER(remote.git_fetch_options),
        ct.c_uint)(
        ("git_fetch_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_indexer_init_options = CFUNC(ct.c_int,
        ct.POINTER(indexer.git_indexer_options),
        ct.c_uint)(
        ("git_indexer_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_merge_init_options = CFUNC(ct.c_int,
        ct.POINTER(merge.git_merge_options),
        ct.c_uint)(
        ("git_merge_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_merge_file_init_input = CFUNC(ct.c_int,
        ct.POINTER(merge.git_merge_file_input),
        ct.c_uint)(
        ("git_merge_file_init_input", dll), (
        (1, "input"),
        (1, "version"),))

    git_merge_file_init_options = CFUNC(ct.c_int,
        ct.POINTER(merge.git_merge_file_options),
        ct.c_uint)(
        ("git_merge_file_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_proxy_init_options = CFUNC(ct.c_int,
        ct.POINTER(proxy.git_proxy_options),
        ct.c_uint)(
        ("git_proxy_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_push_init_options = CFUNC(ct.c_int,
        ct.POINTER(remote.git_push_options),
        ct.c_uint)(
        ("git_push_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_rebase_init_options = CFUNC(ct.c_int,
        ct.POINTER(rebase.git_rebase_options),
        ct.c_uint)(
        ("git_rebase_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_remote_create_init_options = CFUNC(ct.c_int,
        ct.POINTER(remote.git_remote_create_options),
        ct.c_uint)(
        ("git_remote_create_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_repository_init_init_options = CFUNC(ct.c_int,
        ct.POINTER(repository.git_repository_init_options),
        ct.c_uint)(
        ("git_repository_init_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_revert_init_options = CFUNC(ct.c_int,
        ct.POINTER(revert.git_revert_options),
        ct.c_uint)(
        ("git_revert_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_stash_apply_init_options = CFUNC(ct.c_int,
        ct.POINTER(stash.git_stash_apply_options),
        ct.c_uint)(
        ("git_stash_apply_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_status_init_options = CFUNC(ct.c_int,
        ct.POINTER(status.git_status_options),
        ct.c_uint)(
        ("git_status_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_submodule_update_init_options = CFUNC(ct.c_int,
        ct.POINTER(submodule.git_submodule_update_options),
        ct.c_uint)(
        ("git_submodule_update_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_worktree_add_init_options = CFUNC(ct.c_int,
        ct.POINTER(worktree.git_worktree_add_options),
        ct.c_uint)(
        ("git_worktree_add_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    git_worktree_prune_init_options = CFUNC(ct.c_int,
        ct.POINTER(worktree.git_worktree_prune_options),
        ct.c_uint)(
        ("git_worktree_prune_init_options", dll), (
        (1, "opts"),
        (1, "version"),))

    # GIT_END_DECL

# endif
