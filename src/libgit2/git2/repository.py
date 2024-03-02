# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .buffer import git_buf
from .oid    import git_oid_t
from .oid    import git_oid
from .types  import git_object_t
from .types  import git_odb
from .types  import git_config
from .types  import git_repository
from .types  import git_reference
from .types  import git_refdb
from .types  import git_index
from .types  import git_worktree
from .types  import git_annotated_commit

# @file git2/repository.h
# @brief Git repository management routines
# @defgroup git_repository Git repository management routines
# @ingroup Git

# GIT_BEGIN_DECL

# Open a git repository.
#
# The 'path' argument must point to either a git repository
# folder, or an existing work dir.
#
# The method will automatically detect if 'path' is a normal
# or bare repository or fail is 'path' is neither.
#
# @param out pointer to the repo which will be opened
# @param path the path to the repository
# @return 0 or an error code
#
git_repository_open = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_repository)),
    ct.c_char_p)(
    ("git_repository_open", dll), (
    (1, "out"),
    (1, "path"),))

# Open working tree as a repository
#
# Open the working directory of the working tree as a normal
# repository that can then be worked on.
#
# @param out Output pointer containing opened repository
# @param wt Working tree to open
# @return 0 or an error code
#
git_repository_open_from_worktree = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_repository)),
    ct.POINTER(git_worktree))(
    ("git_repository_open_from_worktree", dll), (
    (1, "out"),
    (1, "wt"),))

# Create a "fake" repository to wrap an object database
#
# Create a repository object to wrap an object database to be used
# with the API when all you have is an object database. This doesn't
# have any paths associated with it, so use with care.
#
# @param out pointer to the repo
# @param odb the object database to wrap
# @param oid_type the oid type of the object database
# @return 0 or an error code
#
if defined("GIT_EXPERIMENTAL_SHA256"):
    git_repository_wrap_odb = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_repository)),
        ct.POINTER(git_odb),
        git_oid_t)(
        ("git_repository_wrap_odb", dll), (
        (1, "out"),
        (1, "odb"),
        (1, "oid_type"),))
else:
    git_repository_wrap_odb = CFUNC(ct.c_int,
        ct.POINTER(ct.POINTER(git_repository)),
        ct.POINTER(git_odb))(
        ("git_repository_wrap_odb", dll), (
        (1, "out"),
        (1, "odb"),))
# endif

# Look for a git repository and copy its path in the given buffer.
# The lookup start from base_path and walk across parent directories
# if nothing has been found. The lookup ends when the first repository
# is found, or when reaching a directory referenced in ceiling_dirs
# or when the filesystem changes (in case across_fs is true).
#
# The method will automatically detect if the repository is bare
# (if there is a repository).
#
# @param out A pointer to a user-allocated git_buf which will contain
# the found path.
#
# @param start_path The base path where the lookup starts.
#
# @param across_fs If true, then the lookup will not stop when a
# filesystem device change is detected while exploring parent directories.
#
# @param ceiling_dirs A GIT_PATH_LIST_SEPARATOR separated list of
# absolute symbolic link free paths. The lookup will stop when any
# of this paths is reached. Note that the lookup always performs on
# start_path no matter start_path appears in ceiling_dirs ceiling_dirs
# might be NULL (which is equivalent to an empty string)
#
# @return 0 or an error code
#
git_repository_discover = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.c_char_p,
    ct.c_int,
    ct.c_char_p)(
    ("git_repository_discover", dll), (
    (1, "out"),
    (1, "start_path"),
    (1, "across_fs"),
    (1, "ceiling_dirs"),))

# Option flags for `git_repository_open_ext`.
#
git_repository_open_flag_t = ct.c_int
(
    # Only open the repository if it can be immediately found in the
    # start_path. Do not walk up from the start_path looking at parent
    # directories.
    #
    GIT_REPOSITORY_OPEN_NO_SEARCH,

    # Unless this flag is set, open will not continue searching across
    # filesystem boundaries (i.e. when `st_dev` changes from the `stat`
    # system call).  For example, searching in a user's home directory at
    # "/home/user/source/" will not return "/.git/" as the found repo if
    # "/" is a different filesystem than "/home".
    #
    GIT_REPOSITORY_OPEN_CROSS_FS,

    # Open repository as a bare repo regardless of core.bare config, and
    # defer loading config file for faster setup.
    # Unlike `git_repository_open_bare`, this can follow gitlinks.
    #
    GIT_REPOSITORY_OPEN_BARE,

    # Do not check for a repository by appending /.git to the start_path;
    # only open the repository if start_path itself points to the git
    # directory.
    #
    GIT_REPOSITORY_OPEN_NO_DOTGIT,

    # Find and open a git repository, respecting the environment variables
    # used by the git command-line tools.
    # If set, `git_repository_open_ext` will ignore the other flags and
    # the `ceiling_dirs` argument, and will allow a NULL `path` to use
    # `GIT_DIR` or search from the current directory.
    # The search for a repository will respect $GIT_CEILING_DIRECTORIES and
    # $GIT_DISCOVERY_ACROSS_FILESYSTEM.  The opened repository will
    # respect $GIT_INDEX_FILE, $GIT_NAMESPACE, $GIT_OBJECT_DIRECTORY, and
    # $GIT_ALTERNATE_OBJECT_DIRECTORIES.
    # In the future, this flag will also cause `git_repository_open_ext`
    # to respect $GIT_WORK_TREE and $GIT_COMMON_DIR; currently,
    # `git_repository_open_ext` with this flag will error out if either
    # $GIT_WORK_TREE or $GIT_COMMON_DIR is set.
    #
    GIT_REPOSITORY_OPEN_FROM_ENV,

) = (1 << 0, 1 << 1, 1 << 2, 1 << 3, 1 << 4)

# Find and open a repository with extended controls.
#
# @param out Pointer to the repo which will be opened.  This can
#        actually be NULL if you only want to use the error code to
#        see if a repo at this path could be opened.
# @param path Path to open as git repository.  If the flags
#        permit "searching", then this can be a path to a subdirectory
#        inside the working directory of the repository. May be NULL if
#        flags is GIT_REPOSITORY_OPEN_FROM_ENV.
# @param flags A combination of the GIT_REPOSITORY_OPEN flags above.
# @param ceiling_dirs A GIT_PATH_LIST_SEPARATOR delimited list of path
#        prefixes at which the search for a containing repository should
#        terminate.
# @return 0 on success, GIT_ENOTFOUND if no repository could be found,
#        or -1 if there was a repository but open failed for some reason
#        (such as repo corruption or system errors).
#
git_repository_open_ext = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_repository)),
    ct.c_char_p,
    ct.c_uint,
    ct.c_char_p)(
    ("git_repository_open_ext", dll), (
    (1, "out"),
    (1, "path"),
    (1, "flags"),
    (1, "ceiling_dirs"),))

# Open a bare repository on the serverside.
#
# This is a fast open for bare repositories that will come in handy
# if you're e.g. hosting git repositories and need to access them
# efficiently
#
# @param out Pointer to the repo which will be opened.
# @param bare_path Direct path to the bare repository
# @return 0 on success, or an error code
#
git_repository_open_bare = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_repository)),
    ct.c_char_p)(
    ("git_repository_open_bare", dll), (
    (1, "out"),
    (1, "bare_path"),))

# Free a previously allocated repository
#
# Note that after a repository is free'd, all the objects it has spawned
# will still exist until they are manually closed by the user
# with `git_object_free`, but accessing any of the attributes of
# an object without a backing repository will result in undefined
# behavior
#
# @param repo repository handle to close. If NULL nothing occurs.
#
git_repository_free = CFUNC(None,
    ct.POINTER(git_repository))(
    ("git_repository_free", dll), (
    (1, "repo"),))

# Creates a new Git repository in the given folder.
#
# TODO:
#  - Reinit the repository
#
# @param out pointer to the repo which will be created or reinitialized
# @param path the path to the repository
# @param is_bare if true, a Git repository without a working directory is
#      created at the pointed path. If false, provided path will be
#      considered as the working directory into which the .git directory
#      will be created.
#
# @return 0 or an error code
#
git_repository_init = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_repository)),
    ct.c_char_p,
    ct.c_uint)(
    ("git_repository_init", dll), (
    (1, "out"),
    (1, "path"),
    (1, "is_bare"),))

# Option flags for `git_repository_init_ext`.
#
# These flags configure extra behaviors to `git_repository_init_ext`.
# In every case, the default behavior is the zero value (i.e. flag is
# not set). Just OR the flag values together for the `flags` parameter
# when initializing a new repo.
#
git_repository_init_flag_t = ct.c_int
(
    # Create a bare repository with no working directory.
    #
    GIT_REPOSITORY_INIT_BARE,

    # Return an GIT_EEXISTS error if the repo_path appears to already be
    # an git repository.
    #
    GIT_REPOSITORY_INIT_NO_REINIT,

    # Normally a "/.git/" will be appended to the repo path for
    # non-bare repos (if it is not already there), but passing this flag
    # prevents that behavior.
    #
    GIT_REPOSITORY_INIT_NO_DOTGIT_DIR,

    # Make the repo_path (and workdir_path) as needed. Init is always willing
    # to create the ".git" directory even without this flag. This flag tells
    # init to create the trailing component of the repo and workdir paths
    # as needed.
    #
    GIT_REPOSITORY_INIT_MKDIR,

    # Recursively make all components of the repo and workdir paths as
    # necessary.
    #
    GIT_REPOSITORY_INIT_MKPATH,

    # libgit2 normally uses internal templates to initialize a new repo.
    # This flags enables external templates, looking the "template_path" from
    # the options if set, or the `init.templatedir` global config if not,
    # or falling back on "/usr/share/git-core/templates" if it exists.
    #
    GIT_REPOSITORY_INIT_EXTERNAL_TEMPLATE,

    # If an alternate workdir is specified, use relative paths for the gitdir
    # and core.worktree.
    #
    GIT_REPOSITORY_INIT_RELATIVE_GITLINK,

) = (1 << 0, 1 << 1, 1 << 2, 1 << 3, 1 << 4, 1 << 5, 1 << 6)

# Mode options for `git_repository_init_ext`.
#
# Set the mode field of the `git_repository_init_options` structure
# either to the custom mode that you would like, or to one of the
# defined modes.
#
git_repository_init_mode_t = ct.c_int
(
    # Use permissions configured by umask - the default.
    #
    GIT_REPOSITORY_INIT_SHARED_UMASK,

    # Use "--shared=group" behavior, chmod'ing the new repo to be group
    # writable and "g+sx" for sticky group assignment.
    #
    GIT_REPOSITORY_INIT_SHARED_GROUP,

    # Use "--shared=all" behavior, adding world readability.
    #
    GIT_REPOSITORY_INIT_SHARED_ALL,

) = (0, 0o002775, 0o002777)

# Extended options structure for `git_repository_init_ext`.
#
# This contains extra options for `git_repository_init_ext` that enable
# additional initialization features.
#
class git_repository_init_options(ct.Structure):
    _fields_ = [
    ("version", ct.c_uint),

    # Combination of GIT_REPOSITORY_INIT flags above.
    #
    ("flags", ct.c_uint32),

    # Set to one of the standard GIT_REPOSITORY_INIT_SHARED_... constants
    # above, or to a custom value that you would like.
    #
    ("mode", ct.c_uint32),

    # The path to the working dir or NULL for default (i.e. repo_path parent
    # on non-bare repos). IF THIS IS RELATIVE PATH, IT WILL BE EVALUATED
    # RELATIVE TO THE REPO_PATH. If this is not the "natural" working
    # directory, a .git gitlink file will be created here linking to the
    # repo_path.
    #
    ("workdir_path", ct.c_char_p),

    # If set, this will be used to initialize the "description" file in the
    # repository, instead of using the template content.
    #
    ("description", ct.c_char_p),

    # When GIT_REPOSITORY_INIT_EXTERNAL_TEMPLATE is set, this contains
    # the path to use for the template directory. If this is NULL, the config
    # or default directory options will be used instead.
    #
    ("template_path", ct.c_char_p),

    # The name of the head to point HEAD at. If NULL, then this will be
    # treated as "master" and the HEAD ref will be set to "refs/heads/master".
    # If this begins with "refs/" it will be used verbatim;
    # otherwise "refs/heads/" will be prefixed.
    #
    ("initial_head", ct.c_char_p),

    # If this is non-NULL, then after the rest of the repository
    # initialization is completed, an "origin" remote will be added
    # pointing to this URL.
    #
    ("origin_url", ct.c_char_p),

    #
    # Type of object IDs to use for this repository, or 0 for
    # default (currently SHA1).
    #
    *([("oid_type", git_oid_t)]
      if defined("GIT_EXPERIMENTAL_SHA256") else []),
]

GIT_REPOSITORY_INIT_OPTIONS_VERSION = 1
#define GIT_REPOSITORY_INIT_OPTIONS_INIT = { GIT_REPOSITORY_INIT_OPTIONS_VERSION }

# Initialize git_repository_init_options structure
#
# Initializes a `git_repository_init_options` with default values. Equivalent to
# creating an instance with `GIT_REPOSITORY_INIT_OPTIONS_INIT`.
#
# @param opts The `git_repository_init_options` struct to initialize.
# @param version The struct version; pass `GIT_REPOSITORY_INIT_OPTIONS_VERSION`.
# @return Zero on success; -1 on failure.
#
git_repository_init_options_init = CFUNC(ct.c_int,
    ct.POINTER(git_repository_init_options),
    ct.c_uint)(
    ("git_repository_init_options_init", dll), (
    (1, "opts"),
    (1, "version"),))

# Create a new Git repository in the given folder with extended controls.
#
# This will initialize a new git repository (creating the repo_path
# if requested by flags) and working directory as needed.  It will
# auto-detect the case sensitivity of the file system and if the
# file system supports file mode bits correctly.
#
# @param out Pointer to the repo which will be created or reinitialized.
# @param repo_path The path to the repository.
# @param opts Pointer to git_repository_init_options struct.
# @return 0 or an error code on failure.
#
git_repository_init_ext = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_repository)),
    ct.c_char_p,
    ct.POINTER(git_repository_init_options))(
    ("git_repository_init_ext", dll), (
    (1, "out"),
    (1, "repo_path"),
    (1, "opts"),))

# Retrieve and resolve the reference pointed at by HEAD.
#
# The returned `git_reference` will be owned by caller and
# `git_reference_free()` must be called when done with it to release the
# allocated memory and prevent a leak.
#
# @param out pointer to the reference which will be retrieved
# @param repo a repository object
#
# @return 0 on success, GIT_EUNBORNBRANCH when HEAD points to a non existing
# branch, GIT_ENOTFOUND when HEAD is missing; an error code otherwise
#
git_repository_head = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_reference)),
    ct.POINTER(git_repository))(
    ("git_repository_head", dll), (
    (1, "out"),
    (1, "repo"),))

# Retrieve the referenced HEAD for the worktree
#
# @param out pointer to the reference which will be retrieved
# @param repo a repository object
# @param name name of the worktree to retrieve HEAD for
# @return 0 when successful, error-code otherwise
#
git_repository_head_for_worktree = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_reference)),
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_repository_head_for_worktree", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "name"),))

# Check if a repository's HEAD is detached
#
# A repository's HEAD is detached when it points directly to a commit
# instead of a branch.
#
# @param repo Repo to test
# @return 1 if HEAD is detached, 0 if it's not; error code if there
# was an error.
#
git_repository_head_detached = CFUNC(ct.c_int,
    ct.POINTER(git_repository))(
    ("git_repository_head_detached", dll), (
    (1, "repo"),))

# Check if a worktree's HEAD is detached
#
# A worktree's HEAD is detached when it points directly to a
# commit instead of a branch.
#
# @param repo a repository object
# @param name name of the worktree to retrieve HEAD for
# @return 1 if HEAD is detached, 0 if its not; error code if
#  there was an error
#
git_repository_head_detached_for_worktree = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_repository_head_detached_for_worktree", dll), (
    (1, "repo"),
    (1, "name"),))

# Check if the current branch is unborn
#
# An unborn branch is one named from HEAD but which doesn't exist in
# the refs namespace, because it doesn't have any commit to point to.
#
# @param repo Repo to test
# @return 1 if the current branch is unborn, 0 if it's not; error
# code if there was an error
#
git_repository_head_unborn = CFUNC(ct.c_int,
    ct.POINTER(git_repository))(
    ("git_repository_head_unborn", dll), (
    (1, "repo"),))

# Check if a repository is empty
#
# An empty repository has just been initialized and contains no references
# apart from HEAD, which must be pointing to the unborn master branch,
# or the branch specified for the repository in the `init.defaultBranch`
# configuration variable.
#
# @param repo Repo to test
# @return 1 if the repository is empty, 0 if it isn't, error code
# if the repository is corrupted
#
git_repository_is_empty = CFUNC(ct.c_int,
    ct.POINTER(git_repository))(
    ("git_repository_is_empty", dll), (
    (1, "repo"),))

# List of items which belong to the git repository layout
#
git_repository_item_t = ct.c_int
(   GIT_REPOSITORY_ITEM_GITDIR,
    GIT_REPOSITORY_ITEM_WORKDIR,
    GIT_REPOSITORY_ITEM_COMMONDIR,
    GIT_REPOSITORY_ITEM_INDEX,
    GIT_REPOSITORY_ITEM_OBJECTS,
    GIT_REPOSITORY_ITEM_REFS,
    GIT_REPOSITORY_ITEM_PACKED_REFS,
    GIT_REPOSITORY_ITEM_REMOTES,
    GIT_REPOSITORY_ITEM_CONFIG,
    GIT_REPOSITORY_ITEM_INFO,
    GIT_REPOSITORY_ITEM_HOOKS,
    GIT_REPOSITORY_ITEM_LOGS,
    GIT_REPOSITORY_ITEM_MODULES,
    GIT_REPOSITORY_ITEM_WORKTREES,
    GIT_REPOSITORY_ITEM__LAST,
) = range(0, 15)

# Get the location of a specific repository file or directory
#
# This function will retrieve the path of a specific repository
# item. It will thereby honor things like the repository's
# common directory, gitdir, etc. In case a file path cannot
# exist for a given item (e.g. the working directory of a bare
# repository), GIT_ENOTFOUND is returned.
#
# @param out Buffer to store the path at
# @param repo Repository to get path for
# @param item The repository item for which to retrieve the path
# @return 0, GIT_ENOTFOUND if the path cannot exist or an error code
#
git_repository_item_path = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_repository),
    git_repository_item_t)(
    ("git_repository_item_path", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "item"),))

# Get the path of this repository
#
# This is the path of the `.git` folder for normal repositories,
# or of the repository itself for bare repositories.
#
# @param repo A repository object
# @return the path to the repository
#
git_repository_path = CFUNC(ct.c_char_p,
    ct.POINTER(git_repository))(
    ("git_repository_path", dll), (
    (1, "repo"),))

# Get the path of the working directory for this repository
#
# If the repository is bare, this function will always return
# NULL.
#
# @param repo A repository object
# @return the path to the working dir, if it exists
#
git_repository_workdir = CFUNC(ct.c_char_p,
    ct.POINTER(git_repository))(
    ("git_repository_workdir", dll), (
    (1, "repo"),))

# Get the path of the shared common directory for this repository.
#
# If the repository is bare, it is the root directory for the repository.
# If the repository is a worktree, it is the parent repo's gitdir.
# Otherwise, it is the gitdir.
#
# @param repo A repository object
# @return the path to the common dir
#
git_repository_commondir = CFUNC(ct.c_char_p,
    ct.POINTER(git_repository))(
    ("git_repository_commondir", dll), (
    (1, "repo"),))

# Set the path to the working directory for this repository
#
# The working directory doesn't need to be the same one
# that contains the `.git` folder for this repository.
#
# If this repository is bare, setting its working directory
# will turn it into a normal repository, capable of performing
# all the common workdir operations (checkout, status, index
# manipulation, etc).
#
# @param repo A repository object
# @param workdir The path to a working directory
# @param update_gitlink Create/update gitlink in workdir and set config
#        "core.worktree" (if workdir is not the parent of the .git directory)
# @return 0, or an error code
#
git_repository_set_workdir = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.c_int)(
    ("git_repository_set_workdir", dll), (
    (1, "repo"),
    (1, "workdir"),
    (1, "update_gitlink"),))

# Check if a repository is bare
#
# @param repo Repo to test
# @return 1 if the repository is bare, 0 otherwise.
#
git_repository_is_bare = CFUNC(ct.c_int,
    ct.POINTER(git_repository))(
    ("git_repository_is_bare", dll), (
    (1, "repo"),))

# Check if a repository is a linked work tree
#
# @param repo Repo to test
# @return 1 if the repository is a linked work tree, 0 otherwise.
#
git_repository_is_worktree = CFUNC(ct.c_int,
    ct.POINTER(git_repository))(
    ("git_repository_is_worktree", dll), (
    (1, "repo"),))

# Get the configuration file for this repository.
#
# If a configuration file has not been set, the default
# config set for the repository will be returned, including
# global and system configurations (if they are available).
#
# The configuration file must be freed once it's no longer
# being used by the user.
#
# @param out Pointer to store the loaded configuration
# @param repo A repository object
# @return 0, or an error code
#
git_repository_config = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_config)),
    ct.POINTER(git_repository))(
    ("git_repository_config", dll), (
    (1, "out"),
    (1, "repo"),))

# Get a snapshot of the repository's configuration
#
# Convenience function to take a snapshot from the repository's
# configuration.  The contents of this snapshot will not change,
# even if the underlying config files are modified.
#
# The configuration file must be freed once it's no longer
# being used by the user.
#
# @param out Pointer to store the loaded configuration
# @param repo the repository
# @return 0, or an error code
#
git_repository_config_snapshot = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_config)),
    ct.POINTER(git_repository))(
    ("git_repository_config_snapshot", dll), (
    (1, "out"),
    (1, "repo"),))

# Get the Object Database for this repository.
#
# If a custom ODB has not been set, the default
# database for the repository will be returned (the one
# located in `.git/objects`).
#
# The ODB must be freed once it's no longer being used by
# the user.
#
# @param out Pointer to store the loaded ODB
# @param repo A repository object
# @return 0, or an error code
#
git_repository_odb = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_odb)),
    ct.POINTER(git_repository))(
    ("git_repository_odb", dll), (
    (1, "out"),
    (1, "repo"),))

# Get the Reference Database Backend for this repository.
#
# If a custom refsdb has not been set, the default database for
# the repository will be returned (the one that manipulates loose
# and packed references in the `.git` directory).
#
# The refdb must be freed once it's no longer being used by
# the user.
#
# @param out Pointer to store the loaded refdb
# @param repo A repository object
# @return 0, or an error code
#
git_repository_refdb = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_refdb)),
    ct.POINTER(git_repository))(
    ("git_repository_refdb", dll), (
    (1, "out"),
    (1, "repo"),))

# Get the Index file for this repository.
#
# If a custom index has not been set, the default
# index for the repository will be returned (the one
# located in `.git/index`).
#
# The index must be freed once it's no longer being used by
# the user.
#
# @param out Pointer to store the loaded index
# @param repo A repository object
# @return 0, or an error code
#
git_repository_index = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_index)),
    ct.POINTER(git_repository))(
    ("git_repository_index", dll), (
    (1, "out"),
    (1, "repo"),))

# Retrieve git's prepared message
#
# Operations such as git revert/cherry-pick/merge with the -n option
# stop just short of creating a commit with the changes and save
# their prepared message in .git/MERGE_MSG so the next git-commit
# execution can present it to the user for them to amend if they
# wish.
#
# Use this function to get the contents of this file. Don't forget to
# remove the file after you create the commit.
#
# @param out git_buf to write data into
# @param repo Repository to read prepared message from
# @return 0, GIT_ENOTFOUND if no message exists or an error code
#
git_repository_message = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_repository))(
    ("git_repository_message", dll), (
    (1, "out"),
    (1, "repo"),))

# Remove git's prepared message.
#
# Remove the message that `git_repository_message` retrieves.
#
# @param repo Repository to remove prepared message from.
# @return 0 or an error code.
#
git_repository_message_remove = CFUNC(ct.c_int,
    ct.POINTER(git_repository))(
    ("git_repository_message_remove", dll), (
    (1, "repo"),))

# Remove all the metadata associated with an ongoing command like merge,
# revert, cherry-pick, etc.  For example: MERGE_HEAD, MERGE_MSG, etc.
#
# @param repo A repository object
# @return 0 on success, or error
#
git_repository_state_cleanup = CFUNC(ct.c_int,
    ct.POINTER(git_repository))(
    ("git_repository_state_cleanup", dll), (
    (1, "repo"),))

# Callback used to iterate over each FETCH_HEAD entry
#
# @see git_repository_fetchhead_foreach
#
# @param ref_name The reference name
# @param remote_url The remote URL
# @param oid The reference target OID
# @param is_merge Was the reference the result of a merge
# @param payload Payload passed to git_repository_fetchhead_foreach
# @return non-zero to terminate the iteration
#
git_repository_fetchhead_foreach_cb = GIT_CALLBACK(ct.c_int,
    ct.c_char_p,          # ref_name
    ct.c_char_p,          # remote_url
    ct.POINTER(git_oid),  # oid
    ct.c_uint,            # is_merge
    ct.c_void_p)          # payload

# Invoke 'callback' for each entry in the given FETCH_HEAD file.
#
# Return a non-zero value from the callback to stop the loop.
#
# @param repo A repository object
# @param callback Callback function
# @param payload Pointer to callback data (optional)
# @return 0 on success, non-zero callback return value, GIT_ENOTFOUND if
#         there is no FETCH_HEAD file, or other error code.
#
git_repository_fetchhead_foreach = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    git_repository_fetchhead_foreach_cb,
    ct.c_void_p)(
    ("git_repository_fetchhead_foreach", dll), (
    (1, "repo"),
    (1, "callback"),
    (1, "payload"),))

# Callback used to iterate over each MERGE_HEAD entry
#
# @see git_repository_mergehead_foreach
#
# @param oid The merge OID
# @param payload Payload passed to git_repository_mergehead_foreach
# @return non-zero to terminate the iteration
#
git_repository_mergehead_foreach_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_oid),  # oid
    ct.c_void_p)          # payload

# If a merge is in progress, invoke 'callback' for each commit ID in the
# MERGE_HEAD file.
#
# Return a non-zero value from the callback to stop the loop.
#
# @param repo A repository object
# @param callback Callback function
# @param payload Pointer to callback data (optional)
# @return 0 on success, non-zero callback return value, GIT_ENOTFOUND if
#         there is no MERGE_HEAD file, or other error code.
#
git_repository_mergehead_foreach = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    git_repository_mergehead_foreach_cb,
    ct.c_void_p)(
    ("git_repository_mergehead_foreach", dll), (
    (1, "repo"),
    (1, "callback"),
    (1, "payload"),))

# Calculate hash of file using repository filtering rules.
#
# If you simply want to calculate the hash of a file on disk with no filters,
# you can just use the `git_odb_hashfile()` API.  However, if you want to
# hash a file in the repository and you want to apply filtering rules (e.g.
# crlf filters) before generating the SHA, then use this function.
#
# Note: if the repository has `core.safecrlf` set to fail and the
# filtering triggers that failure, then this function will return an
# error and not calculate the hash of the file.
#
# @param out Output value of calculated SHA
# @param repo Repository pointer
# @param path Path to file on disk whose contents should be hashed.  This
#             may be an absolute path or a relative path, in which case it
#             will be treated as a path within the working directory.
# @param type The object type to hash as (e.g. GIT_OBJECT_BLOB)
# @param as_path The path to use to look up filtering rules. If this is
#             an empty string then no filters will be applied when
#             calculating the hash. If this is `NULL` and the `path`
#             parameter is a file within the repository's working
#             directory, then the `path` will be used.
# @return 0 on success, or an error code
#
git_repository_hashfile = CFUNC(ct.c_int,
    ct.POINTER(git_oid),
    ct.POINTER(git_repository),
    ct.c_char_p,
    git_object_t,
    ct.c_char_p)(
    ("git_repository_hashfile", dll), (
    (1, "out"),
    (1, "repo"),
    (1, "path"),
    (1, "type"),
    (1, "as_path"),))

# Make the repository HEAD point to the specified reference.
#
# If the provided reference points to a Tree or a Blob, the HEAD is
# unaltered and -1 is returned.
#
# If the provided reference points to a branch, the HEAD will point
# to that branch, staying attached, or become attached if it isn't yet.
# If the branch doesn't exist yet, no error will be return. The HEAD
# will then be attached to an unborn branch.
#
# Otherwise, the HEAD will be detached and will directly point to
# the Commit.
#
# @param repo Repository pointer
# @param refname Canonical name of the reference the HEAD should point at
# @return 0 on success, or an error code
#
git_repository_set_head = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_repository_set_head", dll), (
    (1, "repo"),
    (1, "refname"),))

# Make the repository HEAD directly point to the Commit.
#
# If the provided committish cannot be found in the repository, the HEAD
# is unaltered and GIT_ENOTFOUND is returned.
#
# If the provided committish cannot be peeled into a commit, the HEAD
# is unaltered and -1 is returned.
#
# Otherwise, the HEAD will eventually be detached and will directly point to
# the peeled Commit.
#
# @param repo Repository pointer
# @param committish Object id of the Commit the HEAD should point to
# @return 0 on success, or an error code
#
git_repository_set_head_detached = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_oid))(
    ("git_repository_set_head_detached", dll), (
    (1, "repo"),
    (1, "committish"),))

# Make the repository HEAD directly point to the Commit.
#
# This behaves like `git_repository_set_head_detached()` but takes an
# annotated commit, which lets you specify which extended sha syntax
# string was specified by a user, allowing for more exact reflog
# messages.
#
# See the documentation for `git_repository_set_head_detached()`.
#
# @see git_repository_set_head_detached
#
git_repository_set_head_detached_from_annotated = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.POINTER(git_annotated_commit))(
    ("git_repository_set_head_detached_from_annotated", dll), (
    (1, "repo"),
    (1, "committish"),))

# Detach the HEAD.
#
# If the HEAD is already detached and points to a Commit, 0 is returned.
#
# If the HEAD is already detached and points to a Tag, the HEAD is
# updated into making it point to the peeled Commit, and 0 is returned.
#
# If the HEAD is already detached and points to a non committish, the HEAD is
# unaltered, and -1 is returned.
#
# Otherwise, the HEAD will be detached and point to the peeled Commit.
#
# @param repo Repository pointer
# @return 0 on success, GIT_EUNBORNBRANCH when HEAD points to a non existing
# branch or an error code
#
git_repository_detach_head = CFUNC(ct.c_int,
    ct.POINTER(git_repository))(
    ("git_repository_detach_head", dll), (
    (1, "repo"),))

# Repository state
#
# These values represent possible states for the repository to be in,
# based on the current operation which is ongoing.
#
git_repository_state_t = ct.c_int
(   GIT_REPOSITORY_STATE_NONE,
    GIT_REPOSITORY_STATE_MERGE,
    GIT_REPOSITORY_STATE_REVERT,
    GIT_REPOSITORY_STATE_REVERT_SEQUENCE,
    GIT_REPOSITORY_STATE_CHERRYPICK,
    GIT_REPOSITORY_STATE_CHERRYPICK_SEQUENCE,
    GIT_REPOSITORY_STATE_BISECT,
    GIT_REPOSITORY_STATE_REBASE,
    GIT_REPOSITORY_STATE_REBASE_INTERACTIVE,
    GIT_REPOSITORY_STATE_REBASE_MERGE,
    GIT_REPOSITORY_STATE_APPLY_MAILBOX,
    GIT_REPOSITORY_STATE_APPLY_MAILBOX_OR_REBASE,
) = range(0, 12)

# Determines the status of a git repository - ie, whether an operation
# (merge, cherry-pick, etc) is in progress.
#
# @param repo Repository pointer
# @return The state of the repository
#
git_repository_state = CFUNC(ct.c_int,
    ct.POINTER(git_repository))(
    ("git_repository_state", dll), (
    (1, "repo"),))

# Sets the active namespace for this Git Repository
#
# This namespace affects all reference operations for the repo.
# See `man gitnamespaces`
#
# @param repo The repo
# @param nmspace The namespace. This should not include the refs
#  folder, e.g. to namespace all references under `refs/namespaces/foo/`,
#  use `foo` as the namespace.
#  @return 0 on success, -1 on error
#
git_repository_set_namespace = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.c_char_p)(
    ("git_repository_set_namespace", dll), (
    (1, "repo"),
    (1, "nmspace"),))

# Get the currently active namespace for this repository
#
# @param repo The repo
# @return the active namespace, or NULL if there isn't one
#
git_repository_get_namespace = CFUNC(ct.c_char_p,
    ct.POINTER(git_repository))(
    ("git_repository_get_namespace", dll), (
    (1, "repo"),))

# Determine if the repository was a shallow clone
#
# @param repo The repository
# @return 1 if shallow, zero if not
#
git_repository_is_shallow = CFUNC(ct.c_int,
    ct.POINTER(git_repository))(
    ("git_repository_is_shallow", dll), (
    (1, "repo"),))

# Retrieve the configured identity to use for reflogs
#
# The memory is owned by the repository and must not be freed by the
# user.
#
# @param name where to store the pointer to the name
# @param email where to store the pointer to the email
# @param repo the repository
# @return 0 or an error code
#
git_repository_ident = CFUNC(ct.c_int,
    ct.POINTER(ct.c_char_p),
    ct.POINTER(ct.c_char_p),
    ct.POINTER(git_repository))(
    ("git_repository_ident", dll), (
    (1, "name"),
    (1, "email"),
    (1, "repo"),))

# Set the identity to be used for writing reflogs
#
# If both are set, this name and email will be used to write to the
# reflog. Pass NULL to unset. When unset, the identity will be taken
# from the repository's configuration.
#
# @param repo the repository to configure
# @param name the name to use for the reflog entries
# @param email the email to use for the reflog entries
# @return 0 or an error code.
#
git_repository_set_ident = CFUNC(ct.c_int,
    ct.POINTER(git_repository),
    ct.c_char_p,
    ct.c_char_p)(
    ("git_repository_set_ident", dll), (
    (1, "repo"),
    (1, "name"),
    (1, "email"),))

# Gets the object type used by this repository.
#
# @param repo the repository
# @return the object id type
#
git_repository_oid_type = CFUNC(git_oid_t,
    ct.POINTER(git_repository))(
    ("git_repository_oid_type", dll), (
    (1, "repo"),))

# GIT_END_DECL
