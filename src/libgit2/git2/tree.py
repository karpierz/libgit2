# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .oid    import git_oid
from .types  import git_object_t
from .types  import git_object
from .types  import git_repository
from .types  import git_filemode_t
from .types  import git_tree
from .types  import git_tree_entry
from .types  import git_treebuilder

# @file git2/tree.h
# @brief Git tree parsing, loading routines
# @defgroup git_tree Git tree parsing, loading routines
# @ingroup Git

# GIT_BEGIN_DECL

# Lookup a tree object from the repository.
#
# @param out Pointer to the looked up tree
# @param repo The repo to use when locating the tree.
# @param id Identity of the tree to locate.
# @return 0 or an error code
#
git_tree_lookup = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_tree)),  
    ct.POINTER(git_repository),        
    ct.POINTER(git_oid))(              
    ("git_tree_lookup", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "id"),))

# Lookup a tree object from the repository,
# given a prefix of its identifier (short id).
#
# @see git_object_lookup_prefix
#
# @param out pointer to the looked up tree
# @param repo the repo to use when locating the tree.
# @param id identity of the tree to locate.
# @param len the length of the short identifier
# @return 0 or an error code
#
git_tree_lookup_prefix = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_tree)),  
    ct.POINTER(git_repository),        
    ct.POINTER(git_oid),               
    ct.c_size_t)(                      
    ("git_tree_lookup_prefix", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "id"),
    (1, "len"),))

# Close an open tree
#
# You can no longer use the git_tree pointer after this call.
#
# IMPORTANT: You MUST call this method when you stop using a tree to
# release memory. Failure to do so will cause a memory leak.
#
# @param tree The tree to close
#
git_tree_free = CFUNC(None,
    ct.POINTER(git_tree))(      
    ("git_tree_free", dll), (
    (1, "tree"),))

# Get the id of a tree.
#
# @param tree a previously loaded tree.
# @return object identity for the tree.
#
git_tree_id = CFUNC(ct.POINTER(git_oid),
    ct.POINTER(git_tree))(      
    ("git_tree_id", dll), (
    (1, "tree"),))

# Get the repository that contains the tree.
#
# @param tree A previously loaded tree.
# @return Repository that contains this tree.
#
git_tree_owner = CFUNC(ct.POINTER(git_repository),
    ct.POINTER(git_tree))(      
    ("git_tree_owner", dll), (
    (1, "tree"),))

# Get the number of entries listed in a tree
#
# @param tree a previously loaded tree.
# @return the number of entries in the tree
#
git_tree_entrycount = CFUNC(ct.c_size_t,
    ct.POINTER(git_tree))(      
    ("git_tree_entrycount", dll), (
    (1, "tree"),))

# Lookup a tree entry by its filename
#
# This returns a git_tree_entry that is owned by the git_tree.  You don't
# have to free it, but you must not use it after the git_tree is released.
#
# @param tree a previously loaded tree.
# @param filename the filename of the desired entry
# @return the tree entry; NULL if not found
#
git_tree_entry_byname = CFUNC(ct.POINTER(git_tree_entry),
    ct.POINTER(git_tree),             
    ct.c_char_p)(                     
    ("git_tree_entry_byname", dll), (
    (1, "tree"),
    (1, "filename"),))

# Lookup a tree entry by its position in the tree
#
# This returns a git_tree_entry that is owned by the git_tree.  You don't
# have to free it, but you must not use it after the git_tree is released.
#
# @param tree a previously loaded tree.
# @param idx the position in the entry list
# @return the tree entry; NULL if not found
#
git_tree_entry_byindex = CFUNC(ct.POINTER(git_tree_entry),
    ct.POINTER(git_tree),    
    ct.c_size_t)(            
    ("git_tree_entry_byindex", dll), (
    (1, "tree"),
    (1, "idx"),))

# Lookup a tree entry by SHA value.
#
# This returns a git_tree_entry that is owned by the git_tree.  You don't
# have to free it, but you must not use it after the git_tree is released.
#
# Warning: this must examine every entry in the tree, so it is not fast.
#
# @param tree a previously loaded tree.
# @param id the sha being looked for
# @return the tree entry; NULL if not found
#
git_tree_entry_byid = CFUNC(ct.POINTER(git_tree_entry),
    ct.POINTER(git_tree),      
    ct.POINTER(git_oid))(      
    ("git_tree_entry_byid", dll), (
    (1, "tree"),
    (1, "id"),))

# Retrieve a tree entry contained in a tree or in any of its subtrees,
# given its relative path.
#
# Unlike the other lookup functions, the returned tree entry is owned by
# the user and must be freed explicitly with `git_tree_entry_free()`.
#
# @param out Pointer where to store the tree entry
# @param root Previously loaded tree which is the root of the relative path
# @param path Path to the contained entry
# @return 0 on success; GIT_ENOTFOUND if the path does not exist
#
git_tree_entry_bypath = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_tree_entry)),      
    ct.POINTER(git_tree),   
    ct.c_char_p)(           
    ("git_tree_entry_bypath", dll), (
    (1, "out"),
    (1, "root"),
    (1, "path"),))

# Duplicate a tree entry
#
# Create a copy of a tree entry. The returned copy is owned by the user,
# and must be freed explicitly with `git_tree_entry_free()`.
#
# @param dest pointer where to store the copy
# @param source tree entry to duplicate
# @return 0 or an error code
#
git_tree_entry_dup = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_tree_entry)),               
    ct.POINTER(git_tree_entry))(     
    ("git_tree_entry_dup", dll), (
    (1, "dest"),
    (1, "source"),))

# Free a user-owned tree entry
#
# IMPORTANT: This function is only needed for tree entries owned by the
# user, such as the ones returned by `git_tree_entry_dup()` or
# `git_tree_entry_bypath()`.
#
# @param entry The entry to free
#
git_tree_entry_free = CFUNC(None,
    ct.POINTER(git_tree_entry))(             
    ("git_tree_entry_free", dll), (
    (1, "entry"),))

# Get the filename of a tree entry
#
# @param entry a tree entry
# @return the name of the file
#
git_tree_entry_name = CFUNC(ct.c_char_p,
    ct.POINTER(git_tree_entry))(   
    ("git_tree_entry_name", dll), (
    (1, "entry"),))

# Get the id of the object pointed by the entry
#
# @param entry a tree entry
# @return the oid of the object
#
git_tree_entry_id = CFUNC(ct.POINTER(git_oid),
    ct.POINTER(git_tree_entry))(
    ("git_tree_entry_id", dll), (
    (1, "entry"),))

# Get the type of the object pointed by the entry
#
# @param entry a tree entry
# @return the type of the pointed object
#
git_tree_entry_type = CFUNC(git_object_t,
    ct.POINTER(git_tree_entry))(  
    ("git_tree_entry_type", dll), (
    (1, "entry"),))

# Get the UNIX file attributes of a tree entry
#
# @param entry a tree entry
# @return filemode as an integer
#
git_tree_entry_filemode = CFUNC(git_filemode_t,
    ct.POINTER(git_tree_entry))(  
    ("git_tree_entry_filemode", dll), (
    (1, "entry"),))

# Get the raw UNIX file attributes of a tree entry
#
# This function does not perform any normalization and is only useful
# if you need to be able to recreate the original tree object.
#
# @param entry a tree entry
# @return filemode as an integer
#
git_tree_entry_filemode_raw = CFUNC(git_filemode_t,
    ct.POINTER(git_tree_entry))(  
    ("git_tree_entry_filemode_raw", dll), (
    (1, "entry"),))

# Compare two tree entries
#
# @param e1 first tree entry
# @param e2 second tree entry
# @return <0 if e1 is before e2, 0 if e1 == e2, >0 if e1 is after e2
#
git_tree_entry_cmp = CFUNC(ct.c_int,
    ct.POINTER(git_tree_entry),    
    ct.POINTER(git_tree_entry))(   
    ("git_tree_entry_cmp", dll), (
    (1, "e1"),
    (1, "e2"),))

# Convert a tree entry to the git_object it points to.
#
# You must call `git_object_free()` on the object when you are done with it.
#
# @param object_out pointer to the converted object
# @param repo repository where to lookup the pointed object
# @param entry a tree entry
# @return 0 or an error code
#
git_tree_entry_to_object = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_object)),
    ct.POINTER(git_repository),        
    ct.POINTER(git_tree_entry))(       
    ("git_tree_entry_to_object", dll), (
    (1, "object_out"),
    (1, "repo"),
    (1, "entry"),))

# Create a new tree builder.
#
# The tree builder can be used to create or modify trees in memory and
# write them as tree objects to the database.
#
# If the `source` parameter is not NULL, the tree builder will be
# initialized with the entries of the given tree.
#
# If the `source` parameter is NULL, the tree builder will start with no
# entries and will have to be filled manually.
#
# @param out Pointer where to store the tree builder
# @param repo Repository in which to store the object
# @param source Source tree to initialize the builder (optional)
# @return 0 on success; error code otherwise
#
git_treebuilder_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_treebuilder)),   
    ct.POINTER(git_repository),                
    ct.POINTER(git_tree))(                     
    ("git_treebuilder_new", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "source"),))

# Clear all the entries in the builder
#
# @param bld Builder to clear
# @return 0 on success; error code otherwise
#
git_treebuilder_clear = CFUNC(ct.c_int,
    ct.POINTER(git_treebuilder))(       
    ("git_treebuilder_clear", dll), (
    (1, "bld"),))

# Get the number of entries listed in a treebuilder
#
# @param bld a previously loaded treebuilder.
# @return the number of entries in the treebuilder
#
git_treebuilder_entrycount = CFUNC(ct.c_size_t,
    ct.POINTER(git_treebuilder))(       
    ("git_treebuilder_entrycount", dll), (
    (1, "bld"),))

# Free a tree builder
#
# This will clear all the entries and free to builder.
# Failing to free the builder after you're done using it
# will result in a memory leak
#
# @param bld Builder to free
#
git_treebuilder_free = CFUNC(None,
    ct.POINTER(git_treebuilder))(       
    ("git_treebuilder_free", dll), (
    (1, "bld"),))

# Get an entry from the builder from its filename
#
# The returned entry is owned by the builder and should
# not be freed manually.
#
# @param bld Tree builder
# @param filename Name of the entry
# @return pointer to the entry; NULL if not found
#
git_treebuilder_get = CFUNC(ct.POINTER(git_tree_entry),
    ct.POINTER(git_treebuilder),     
    ct.c_char_p)(    
    ("git_treebuilder_get", dll), (
    (1, "bld"),
    (1, "filename"),))

# Add or update an entry to the builder
#
# Insert a new entry for `filename` in the builder with the
# given attributes.
#
# If an entry named `filename` already exists, its attributes
# will be updated with the given ones.
#
# The optional pointer `out` can be used to retrieve a pointer to the
# newly created/updated entry.  Pass NULL if you do not need it. The
# pointer may not be valid past the next operation in this
# builder. Duplicate the entry if you want to keep it.
#
# By default the entry that you are inserting will be checked for
# validity; that it exists in the object database and is of the
# correct type.  If you do not want this behavior, set the
# `GIT_OPT_ENABLE_STRICT_OBJECT_CREATION` library option to false.
#
# @param out Pointer to store the entry (optional)
# @param bld Tree builder
# @param filename Filename of the entry
# @param id SHA1 oid of the entry
# @param filemode Folder attributes of the entry. This parameter must
#          be valued with one of the following entries: 0040000, 0100644,
#          0100755, 0120000 or 0160000.
# @return 0 or an error code
#
git_treebuilder_insert = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_tree_entry)),  
    ct.POINTER(git_treebuilder),             
    ct.c_char_p,                             
    ct.POINTER(git_oid),                     
    git_filemode_t)(                         
    ("git_treebuilder_insert", dll), (
    (1, "out"),
    (1, "bld"),
    (1, "filename"),
    (1, "id"),
    (1, "filemode"),))

# Remove an entry from the builder by its filename
#
# @param bld Tree builder
# @param filename Filename of the entry to remove
# @return 0 or an error code
#
git_treebuilder_remove = CFUNC(ct.c_int,
    ct.POINTER(git_treebuilder),     
    ct.c_char_p)(                    
    ("git_treebuilder_remove", dll), (
    (1, "bld"),
    (1, "filename"),))

# Callback for git_treebuilder_filter
#
# The return value is treated as a boolean, with zero indicating that the
# entry should be left alone and any non-zero value meaning that the
# entry should be removed from the treebuilder list (i.e. filtered out).
#
git_treebuilder_filter_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_tree_entry),  # entry
    ct.c_void_p)                 # payload

# Selectively remove entries in the tree
#
# The `filter` callback will be called for each entry in the tree with a
# pointer to the entry and the provided `payload`; if the callback returns
# non-zero, the entry will be filtered (removed from the builder).
#
# @param bld Tree builder
# @param filter Callback to filter entries
# @param payload Extra data to pass to filter callback
# @return 0 on success, non-zero callback return value, or error code
#
git_treebuilder_filter = CFUNC(ct.c_int,
    ct.POINTER(git_treebuilder),     
    git_treebuilder_filter_cb,       
    ct.c_void_p)(                    
    ("git_treebuilder_filter", dll), (
    (1, "bld"),
    (1, "filter"),
    (1, "payload"),))

# Write the contents of the tree builder as a tree object
#
# The tree builder will be written to the given `repo`, and its
# identifying SHA1 hash will be stored in the `id` pointer.
#
# @param id Pointer to store the OID of the newly written tree
# @param bld Tree builder to write
# @return 0 or an error code
#
git_treebuilder_write = CFUNC(ct.c_int,
    ct.POINTER(git_oid),                
    ct.POINTER(git_treebuilder))(       
    ("git_treebuilder_write", dll), (
    (1, "id"),
    (1, "bld"),))

# Callback for the tree traversal method
git_treewalk_cb = GIT_CALLBACK(ct.c_int,
    ct.c_char_p,                 # root
    ct.POINTER(git_tree_entry),  # entry
    ct.c_void_p)                 # payload

# Tree traversal modes
git_treewalk_mode = ct.c_int
(   GIT_TREEWALK_PRE,   # Pre-order
    GIT_TREEWALK_POST,  # Post-order
) = (0, 1)

# Traverse the entries in a tree and its subtrees in post or pre order.
#
# The entries will be traversed in the specified order, children subtrees
# will be automatically loaded as required, and the `callback` will be
# called once per entry with the current (relative) root for the entry and
# the entry data itself.
#
# If the callback returns a positive value, the passed entry will be
# skipped on the traversal (in pre mode). A negative value stops the walk.
#
# @param tree The tree to walk
# @param mode Traversal mode (pre or post-order)
# @param callback Function to call on each tree entry
# @param payload Opaque pointer to be passed on each callback
# @return 0 or an error code
#
git_tree_walk = CFUNC(ct.c_int,
    ct.POINTER(git_tree),      
    git_treewalk_mode,         
    git_treewalk_cb,           
    ct.c_void_p)(              
    ("git_tree_walk", dll), (
    (1, "tree"),
    (1, "mode"),
    (1, "callback"),
    (1, "payload"),))

# Create an in-memory copy of a tree. The copy must be explicitly
# free'd or it will leak.
#
# @param out Pointer to store the copy of the tree
# @param source Original tree to copy
# @return 0
#
git_tree_dup = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_tree)),  
    ct.POINTER(git_tree))(             
    ("git_tree_dup", dll), (
    (1, "out"),
    (1, "source"),))

# The kind of update to perform
#
git_tree_update_t = ct.c_int
(   # Update or insert an entry at the specified path
    GIT_TREE_UPDATE_UPSERT,
    # Remove an entry from the specified path
    GIT_TREE_UPDATE_REMOVE,
) = range(0, 2)

# An action to perform during the update of a tree
#
class git_tree_update(ct.Structure):
    _fields_ = [
    # Update action. If it's an removal, only the path is looked at
    ("action", git_tree_update_t),
    # The entry's id
    ("id", git_oid),
    # The filemode/kind of object
    ("filemode", git_filemode_t),
    # The full path from the root tree
    ("path", ct.c_char_p),
]

# Create a tree based on another one with the specified modifications
#
# Given the `baseline` perform the changes described in the list of
# `updates` and create a new tree.
#
# This function is optimized for common file/directory addition, removal and
# replacement in trees. It is much more efficient than reading the tree into a
# `git_index` and modifying that, but in exchange it is not as flexible.
#
# Deleting and adding the same entry is undefined behaviour, changing
# a tree to a blob or viceversa is not supported.
#
# @param out id of the new tree
# @param repo the repository in which to create the tree, must be the
# same as for `baseline`
# @param baseline the tree to base these changes on
# @param nupdates the number of elements in the update list
# @param updates the list of updates to perform
# @return 0 or an error code
#
git_tree_create_updated = CFUNC(ct.c_int,
    ct.POINTER(git_oid),               
    ct.POINTER(git_repository),        
    ct.POINTER(git_tree),              
    ct.c_size_t,                       
    ct.POINTER(git_tree_update))(      
    ("git_tree_create_updated", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "baseline"),
    (1, "nupdates"),
    (1, "updates"),))

# GIT_END_DECL
