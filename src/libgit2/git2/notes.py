# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .oid    import git_oid
from .buffer import git_buf
from .types  import git_signature
from .types  import git_repository
from .types  import git_commit
from .types  import git_note

# @file git2/notes.h
# @brief Git notes management routines
# @defgroup git_note Git notes management routines
# @ingroup Git

# GIT_BEGIN_DECL

# Callback for git_note_foreach.
#
# Receives:
# - blob_id: Oid of the blob containing the message
# - annotated_object_id: Oid of the git object being annotated
# - payload: Payload data passed to `git_note_foreach`
#
git_note_foreach_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_oid),  # blob_id
    ct.POINTER(git_oid),  # annotated_object_id
    ct.c_void_p)          # payload

# note iterator
#
class git_iterator(ct.Structure): pass
git_note_iterator = git_iterator

# Creates a new iterator for notes
#
# The iterator must be freed manually by the user.
#
# @param out pointer to the iterator
# @param repo repository where to look up the note
# @param notes_ref canonical name of the reference to use (optional); defaults to
#                  "refs/notes/commits"
#
# @return 0 or an error code
#
git_note_iterator_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_note_iterator)),
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_note_iterator_new", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "notes_ref"),))

# Creates a new iterator for notes from a commit
#
# The iterator must be freed manually by the user.
#
# @param out pointer to the iterator
# @param notes_commit a pointer to the notes commit object
#
# @return 0 or an error code
#
git_note_commit_iterator_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_note_iterator)),
    ct.POINTER(git_commit))(
    ("git_note_commit_iterator_new", dll), (
    (1, "out"),
    (1, "notes_commit"),))

# Frees an git_note_iterator
#
# @param it pointer to the iterator
#
git_note_iterator_free = CFUNC(None,
    ct.POINTER(git_note_iterator))(
    ("git_note_iterator_free", dll), (
    (1, "it"),))

# Return the current item (note_id and annotated_id) and advance the iterator
# internally to the next value
#
# @param note_id id of blob containing the message
# @param annotated_id id of the git object being annotated
# @param it pointer to the iterator
#
# @return 0 (no error), GIT_ITEROVER (iteration is done) or an error code
#         (negative value)
#
git_note_next = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_oid),
    ct.POINTER(git_note_iterator))(
    ("git_note_next", dll), (
    (1, "note_id"),
    (1, "annotated_id"),
    (1, "it"),))

# Read the note for an object
#
# The note must be freed manually by the user.
#
# @param out pointer to the read note; NULL in case of error
# @param repo repository where to look up the note
# @param notes_ref canonical name of the reference to use (optional); defaults to
#                  "refs/notes/commits"
# @param oid OID of the git object to read the note from
#
# @return 0 or an error code
#
git_note_read = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_note)),
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.POINTER(git_oid))(
    ("git_note_read", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "notes_ref"),
    (1, "oid"),))

# Read the note for an object from a note commit
#
# The note must be freed manually by the user.
#
# @param out pointer to the read note; NULL in case of error
# @param repo repository where to look up the note
# @param notes_commit a pointer to the notes commit object
# @param oid OID of the git object to read the note from
#
# @return 0 or an error code
#
git_note_commit_read = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_note)),
    ct.POINTER(git_repository),
    ct.POINTER(git_commit),
    ct.POINTER(git_oid))(
    ("git_note_commit_read", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "notes_commit"),
    (1, "oid"),))

# Get the note author
#
# @param note the note
# @return the author
#
git_note_author = CFUNC(ct.POINTER(git_signature),
    ct.POINTER(git_note))(
    ("git_note_author", dll), (
    (1, "note"),))

# Get the note committer
#
# @param note the note
# @return the committer
#
git_note_committer = CFUNC(ct.POINTER(git_signature),
    ct.POINTER(git_note))(
    ("git_note_committer", dll), (
    (1, "note"),))

# Get the note message
#
# @param note the note
# @return the note message
#
git_note_message = CFUNC(ct.c_char_p,
    ct.POINTER(git_note))(
    ("git_note_message", dll), (
    (1, "note"),))

# Get the note object's id
#
# @param note the note
# @return the note object's id
#
git_note_id = CFUNC(ct.POINTER(git_oid),
    ct.POINTER(git_note))(
    ("git_note_id", dll), (
    (1, "note"),))

# Add a note for an object
#
# @param out pointer to store the OID (optional); NULL in case of error
# @param repo repository where to store the note
# @param notes_ref canonical name of the reference to use (optional);
#                  defaults to "refs/notes/commits"
# @param author signature of the notes commit author
# @param committer signature of the notes commit committer
# @param oid OID of the git object to decorate
# @param note Content of the note to add for object oid
# @param force Overwrite existing note
#
# @return 0 or an error code
#
git_note_create = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.POINTER(git_signature),
    ct.POINTER(git_signature),
    ct.POINTER(git_oid),
    ct.c_char_p,
    ct.c_int)(
    ("git_note_create", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "notes_ref"),
    (1, "author"),
    (1, "committer"),
    (1, "oid"),
    (1, "note"),
    (1, "force"),))

# Add a note for an object from a commit
#
# This function will create a notes commit for a given object,
# the commit is a dangling commit, no reference is created.
#
# @param notes_commit_out pointer to store the commit (optional);
#                  NULL in case of error
# @param notes_blob_out a point to the id of a note blob (optional)
# @param repo repository where the note will live
# @param parent Pointer to parent note
#                  or NULL if this shall start a new notes tree
# @param author signature of the notes commit author
# @param committer signature of the notes commit committer
# @param oid OID of the git object to decorate
# @param note Content of the note to add for object oid
# @param allow_note_overwrite Overwrite existing note
#
# @return 0 or an error code
#
git_note_commit_create = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.POINTER(git_commit),
    ct.POINTER(git_signature),
    ct.POINTER(git_signature),
    ct.POINTER(git_oid),
    ct.c_char_p,
    ct.c_int)(
    ("git_note_commit_create", dll), (
    (1, "notes_commit_out"),
    (1, "notes_blob_out"),
    (1, "repo"),
    (1, "parent"),
    (1, "author"),
    (1, "committer"),
    (1, "oid"),
    (1, "note"),
    (1, "allow_note_overwrite"),))

# Remove the note for an object
#
# @param repo repository where the note lives
# @param notes_ref canonical name of the reference to use (optional);
#                  defaults to "refs/notes/commits"
# @param author signature of the notes commit author
# @param committer signature of the notes commit committer
# @param oid OID of the git object to remove the note from
#
# @return 0 or an error code
#
git_note_remove = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.POINTER(git_signature),
    ct.POINTER(git_signature),
    ct.POINTER(git_oid))(
    ("git_note_remove", dll), (
    (1, "repo"),
    (1, "notes_ref"),
    (1, "author"),
    (1, "committer"),
    (1, "oid"),))

# Remove the note for an object
#
# @param notes_commit_out pointer to store the new notes commit (optional);
#                  NULL in case of error.
#                  When removing a note a new tree containing all notes
#                  sans the note to be removed is created and a new commit
#                  pointing to that tree is also created.
#                  In the case where the resulting tree is an empty tree
#                  a new commit pointing to this empty tree will be returned.
# @param repo repository where the note lives
# @param notes_commit a pointer to the notes commit object
# @param author signature of the notes commit author
# @param committer signature of the notes commit committer
# @param oid OID of the git object to remove the note from
#
# @return 0 or an error code
#
git_note_commit_remove = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.POINTER(git_commit),
    ct.POINTER(git_signature),
    ct.POINTER(git_signature),
    ct.POINTER(git_oid))(
    ("git_note_commit_remove", dll), (
    (1, "notes_commit_out"),
    (1, "repo"),
    (1, "notes_commit"),
    (1, "author"),
    (1, "committer"),
    (1, "oid"),))

# Free a git_note object
#
# @param note git_note object
#
git_note_free = CFUNC(None,
    ct.POINTER(git_note))(
    ("git_note_free", dll), (
    (1, "note"),))

# Get the default notes reference for a repository
#
# @param out buffer in which to store the name of the default notes reference
# @param repo The Git repository
#
# @return 0 or an error code
#
git_note_default_ref = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_repository))(
    ("git_note_default_ref", dll), (
    (1, "out"),
    (1, "repo"),))

# Loop over all the notes within a specified namespace
# and issue a callback for each one.
#
# @param repo Repository where to find the notes.
#
# @param notes_ref Reference to read from (optional); defaults to
#        "refs/notes/commits".
#
# @param note_cb Callback to invoke per found annotation.  Return non-zero
#        to stop looping.
#
# @param payload Extra parameter to callback function.
#
# @return 0 on success, non-zero callback return value, or error code
#
git_note_foreach = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.c_char_p,
    git_note_foreach_cb,
    ct.c_void_p)(
    ("git_note_foreach", dll), (
    (1, "repo"),
    (1, "notes_ref"),
    (1, "note_cb"),
    (1, "payload"),))

# GIT_END_DECL
