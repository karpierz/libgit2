# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from .common import *  # noqa
from .buffer import git_buf
from .types  import git_repository
from .types  import git_config
from .types  import git_config_backend
from .types  import git_transaction

# @file git2/config.h
# @brief Git config management routines
# @defgroup git_config Git config management routines
# @ingroup Git

# GIT_BEGIN_DECL

# Priority level of a config file.
# These priority levels correspond to the natural escalation logic
# (from higher to lower) when searching for config entries in git.git.
#
# git_config_open_default() and git_repository_config() honor those
# priority levels as well.
#
git_config_level_t = ct.c_int
(
    # System-wide on Windows, for compatibility with portable git
    GIT_CONFIG_LEVEL_PROGRAMDATA,

    # System-wide configuration file; /etc/gitconfig on Linux systems
    GIT_CONFIG_LEVEL_SYSTEM,

    # XDG compatible configuration file; typically ~/.config/git/config
    GIT_CONFIG_LEVEL_XDG,

    # User-specific configuration file (also called Global configuration
    # file); typically ~/.gitconfig
    #
    GIT_CONFIG_LEVEL_GLOBAL,

    # Repository specific configuration file; $WORK_DIR/.git/config on
    # non-bare repos
    #
    GIT_CONFIG_LEVEL_LOCAL,

    # Application specific configuration file; freely defined by applications
    #
    GIT_CONFIG_LEVEL_APP,

    # Represents the highest level available config file (i.e. the most
    # specific config file available that actually is loaded)
    #
    GIT_CONFIG_HIGHEST_LEVEL,

) = (1,  2,  3,  4,  5,  6,  -1)

# An entry in a configuration file
#
class git_config_entry(ct.Structure): pass
git_config_entry._fields_ = [
    ("name",          ct.c_char_p),         # Name of the entry (normalised)
    ("value",         ct.c_char_p),         # String value of the entry
    ("include_depth", ct.c_uint),           # Depth of includes where this variable was found
    ("level",         git_config_level_t),  # Which config file this was found in
    ("free",          GIT_CALLBACK(None,    # Free function for this entry
                          ct.POINTER(git_config_entry))),  # entry
    ("payload",       ct.c_void_p),         # Opaque value for the free function.
                                            # Do not read or write
]

# Free a config entry
#
# @param entry The entry to free.
#
git_config_entry_free = CFUNC(None,
    ct.POINTER(git_config_entry))(
    ("git_config_entry_free", dll), (
    (1, "entry"),))

# A config enumeration callback
#
# @param entry the entry currently being enumerated
# @param payload a user-specified pointer
# @return non-zero to terminate the iteration.
#
git_config_foreach_cb = GIT_CALLBACK(ct.c_int,
    ct.POINTER(git_config_entry),  # entry
    ct.c_void_p)                   # payload

# An opaque structure for a configuration iterator
#
# class git_config_iterator(ct.Structure): pass
from .sys.config import git_config_iterator

# Config var type
#
git_configmap_t = ct.c_int
(   GIT_CONFIGMAP_FALSE,
    GIT_CONFIGMAP_TRUE,
    GIT_CONFIGMAP_INT32,
    GIT_CONFIGMAP_STRING,
) = (0, 1, 2, 3)

# Mapping from config variables to values.
#
class git_configmap(ct.Structure):
    _fields_ = [
    ("type",      git_configmap_t),
    ("str_match", ct.c_char_p),
    ("map_value", ct.c_int),
]

# Locate the path to the global configuration file
#
# The user or global configuration file is usually
# located in `$HOME/.gitconfig`.
#
# This method will try to guess the full path to that
# file, if the file exists. The returned path
# may be used on any `git_config` call to load the
# global configuration file.
#
# This method will not guess the path to the xdg compatible
# config file (`.config/git/config`).
#
# @param out Pointer to a user-allocated git_buf in which to store the path
# @return 0 if a global configuration file has been found. Its path will be stored in `out`.
#
git_config_find_global = CFUNC(ct.c_int,
    ct.POINTER(git_buf))(
    ("git_config_find_global", dll), (
    (1, "out"),))

# Locate the path to the global xdg compatible configuration file
#
# The xdg compatible configuration file is usually
# located in `$HOME/.config/git/config`.
#
# This method will try to guess the full path to that
# file, if the file exists. The returned path
# may be used on any `git_config` call to load the
# xdg compatible configuration file.
#
# @param out Pointer to a user-allocated git_buf in which to store the path
# @return 0 if a xdg compatible configuration file has been
#  found. Its path will be stored in `out`.
#
git_config_find_xdg = CFUNC(ct.c_int,
    ct.POINTER(git_buf))(
    ("git_config_find_xdg", dll), (
    (1, "out"),))

# Locate the path to the system configuration file
#
# If `/etc/gitconfig` doesn't exist, it will look for
# `%PROGRAMFILES%\Git\etc\gitconfig`.
#
# @param out Pointer to a user-allocated git_buf in which to store the path
# @return 0 if a system configuration file has been
#  found. Its path will be stored in `out`.
#
git_config_find_system = CFUNC(ct.c_int,
    ct.POINTER(git_buf))(
    ("git_config_find_system", dll), (
    (1, "out"),))

# Locate the path to the configuration file in ProgramData
#
# Look for the file in `%PROGRAMDATA%\Git\config` used by portable git.
#
# @param out Pointer to a user-allocated git_buf in which to store the path
# @return 0 if a ProgramData configuration file has been
#  found. Its path will be stored in `out`.
#
git_config_find_programdata = CFUNC(ct.c_int,
    ct.POINTER(git_buf))(
    ("git_config_find_programdata", dll), (
    (1, "out"),))

# Open the global, XDG and system configuration files
#
# Utility wrapper that finds the global, XDG and system configuration files
# and opens them into a single prioritized config object that can be
# used when accessing default config data outside a repository.
#
# @param out Pointer to store the config instance
# @return 0 or an error code
#
git_config_open_default = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_config)))(
    ("git_config_open_default", dll), (
    (1, "out"),))

# Allocate a new configuration object
#
# This object is empty, so you have to add a file to it before you
# can do anything with it.
#
# @param out pointer to the new configuration
# @return 0 or an error code
#
git_config_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_config)))(
    ("git_config_new", dll), (
    (1, "out"),))

# Add an on-disk config file instance to an existing config
#
# The on-disk file pointed at by `path` will be opened and
# parsed; it's expected to be a native Git config file following
# the default Git config syntax (see man git-config).
#
# If the file does not exist, the file will still be added and it
# will be created the first time we write to it.
#
# Note that the configuration object will free the file
# automatically.
#
# Further queries on this config object will access each
# of the config file instances in order (instances with
# a higher priority level will be accessed first).
#
# @param cfg the configuration to add the file to
# @param path path to the configuration file to add
# @param level the priority level of the backend
# @param force replace config file at the given priority level
# @param repo optional repository to allow parsing of
#  conditional includes
# @return 0 on success, GIT_EEXISTS when adding more than one file
#  for a given priority level (and force_replace set to 0),
#  GIT_ENOTFOUND when the file doesn't exist or error code
#
git_config_add_file_ondisk = CFUNC(ct.c_int,
    ct.POINTER(git_config),
    ct.c_char_p,
    git_config_level_t,
    ct.POINTER(git_repository),
    ct.c_int)(
    ("git_config_add_file_ondisk", dll), (
    (1, "cfg"),
    (1, "path"),
    (1, "level"),
    (1, "repo"),
    (1, "force"),))

# Create a new config instance containing a single on-disk file
#
# This method is a simple utility wrapper for the following sequence
# of calls:
#  - git_config_new
#  - git_config_add_file_ondisk
#
# @param out The configuration instance to create
# @param path Path to the on-disk file to open
# @return 0 on success, or an error code
#
git_config_open_ondisk = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_config)),
    ct.c_char_p)(
    ("git_config_open_ondisk", dll), (
    (1, "out"),
    (1, "path"),))

# Build a single-level focused config object from a multi-level one.
#
# The returned config object can be used to perform get/set/delete operations
# on a single specific level.
#
# Getting several times the same level from the same parent multi-level config
# will return different config instances, but containing the same config_file
# instance.
#
# @param out The configuration instance to create
# @param parent Multi-level config to search for the given level
# @param level Configuration level to search for
# @return 0, GIT_ENOTFOUND if the passed level cannot be found in the
# multi-level parent config, or an error code
#
git_config_open_level = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_config)),
    ct.POINTER(git_config),
    git_config_level_t)(
    ("git_config_open_level", dll), (
    (1, "out"),
    (1, "parent"),
    (1, "level"),))

# Open the global/XDG configuration file according to git's rules
#
# Git allows you to store your global configuration at
# `$HOME/.gitconfig` or `$XDG_CONFIG_HOME/git/config`. For backwards
# compatibility, the XDG file shouldn't be used unless the use has
# created it explicitly. With this function you'll open the correct
# one to write to.
#
# @param out pointer in which to store the config object
# @param config the config object in which to look
# @return 0 or an error code.
#
git_config_open_global = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_config)),
    ct.POINTER(git_config))(
    ("git_config_open_global", dll), (
    (1, "out"),
    (1, "config"),))

# Create a snapshot of the configuration
#
# Create a snapshot of the current state of a configuration, which
# allows you to look into a consistent view of the configuration for
# looking up complex values (e.g. a remote, submodule).
#
# The string returned when querying such a config object is valid
# until it is freed.
#
# @param out pointer in which to store the snapshot config object
# @param config configuration to snapshot
# @return 0 or an error code
#
git_config_snapshot = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_config)),
    ct.POINTER(git_config))(
    ("git_config_snapshot", dll), (
    (1, "out"),
    (1, "config"),))

# Free the configuration and its associated memory and files
#
# @param cfg the configuration to free
#
git_config_free = CFUNC(None,
    ct.POINTER(git_config))(
    ("git_config_free", dll), (
    (1, "cfg"),))

# Get the git_config_entry of a config variable.
#
# Free the git_config_entry after use with `git_config_entry_free()`.
#
# @param out pointer to the variable git_config_entry
# @param cfg where to look for the variable
# @param name the variable's name
# @return 0 or an error code
#
git_config_get_entry = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_config_entry)),
    ct.POINTER(git_config),
    ct.c_char_p)(
    ("git_config_get_entry", dll), (
    (1, "out"),
    (1, "cfg"),
    (1, "name"),))

# Get the value of an integer config variable.
#
# All config files will be looked into, in the order of their
# defined level. A higher level means a higher priority. The
# first occurrence of the variable will be returned here.
#
# @param out pointer to the variable where the value should be stored
# @param cfg where to look for the variable
# @param name the variable's name
# @return 0 or an error code
#
git_config_get_int32 = CFUNC(ct.c_int,
    ct.POINTER(ct.c_int32),
    ct.POINTER(git_config),
    ct.c_char_p)(
    ("git_config_get_int32", dll), (
    (1, "out"),
    (1, "cfg"),
    (1, "name"),))

# Get the value of a long integer config variable.
#
# All config files will be looked into, in the order of their
# defined level. A higher level means a higher priority. The
# first occurrence of the variable will be returned here.
#
# @param out pointer to the variable where the value should be stored
# @param cfg where to look for the variable
# @param name the variable's name
# @return 0 or an error code
#
git_config_get_int64 = CFUNC(ct.c_int,
    ct.POINTER(ct.c_int64),
    ct.POINTER(git_config),
    ct.c_char_p)(
    ("git_config_get_int64", dll), (
    (1, "out"),
    (1, "cfg"),
    (1, "name"),))

# Get the value of a boolean config variable.
#
# This function uses the usual C convention of 0 being false and
# anything else true.
#
# All config files will be looked into, in the order of their
# defined level. A higher level means a higher priority. The
# first occurrence of the variable will be returned here.
#
# @param out pointer to the variable where the value should be stored
# @param cfg where to look for the variable
# @param name the variable's name
# @return 0 or an error code
#
git_config_get_bool = CFUNC(ct.c_int,
    ct.POINTER(ct.c_int),
    ct.POINTER(git_config),
    ct.c_char_p)(
    ("git_config_get_bool", dll), (
    (1, "out"),
    (1, "cfg"),
    (1, "name"),))

# Get the value of a path config variable.
#
# A leading '~' will be expanded to the global search path (which
# defaults to the user's home directory but can be overridden via
# `git_libgit2_opts()`.
#
# All config files will be looked into, in the order of their
# defined level. A higher level means a higher priority. The
# first occurrence of the variable will be returned here.
#
# @param out the buffer in which to store the result
# @param cfg where to look for the variable
# @param name the variable's name
# @return 0 or an error code
#
git_config_get_path = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_config),
    ct.c_char_p)(
    ("git_config_get_path", dll), (
    (1, "out"),
    (1, "cfg"),
    (1, "name"),))

# Get the value of a string config variable.
#
# This function can only be used on snapshot config objects. The
# string is owned by the config and should not be freed by the
# user. The pointer will be valid until the config is freed.
#
# All config files will be looked into, in the order of their
# defined level. A higher level means a higher priority. The
# first occurrence of the variable will be returned here.
#
# @param out pointer to the string
# @param cfg where to look for the variable
# @param name the variable's name
# @return 0 or an error code
#
git_config_get_string = CFUNC(ct.c_int,
    ct.POINTER(ct.c_char_p),
    ct.POINTER(git_config),
    ct.c_char_p)(
    ("git_config_get_string", dll), (
    (1, "out"),
    (1, "cfg"),
    (1, "name"),))

# Get the value of a string config variable.
#
# The value of the config will be copied into the buffer.
#
# All config files will be looked into, in the order of their
# defined level. A higher level means a higher priority. The
# first occurrence of the variable will be returned here.
#
# @param out buffer in which to store the string
# @param cfg where to look for the variable
# @param name the variable's name
# @return 0 or an error code
#
git_config_get_string_buf = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.POINTER(git_config),
    ct.c_char_p)(
    ("git_config_get_string_buf", dll), (
    (1, "out"),
    (1, "cfg"),
    (1, "name"),))

# Get each value of a multivar in a foreach callback
#
# The callback will be called on each variable found
#
# The regular expression is applied case-sensitively on the normalized form of
# the variable name: the section and variable parts are lower-cased. The
# subsection is left unchanged.
#
# @param cfg where to look for the variable
# @param name the variable's name
# @param regexp regular expression to filter which variables we're
# interested in. Use NULL to indicate all
# @param callback the function to be called on each value of the variable
# @param payload opaque pointer to pass to the callback
# @return 0 or an error code.
#
git_config_get_multivar_foreach = CFUNC(ct.c_int,
    ct.POINTER(git_config),
    ct.c_char_p,
    ct.c_char_p,
    git_config_foreach_cb,
    ct.c_void_p)(
    ("git_config_get_multivar_foreach", dll), (
    (1, "cfg"),
    (1, "name"),
    (1, "regexp"),
    (1, "callback"),
    (1, "payload"),))

# Get each value of a multivar
#
# The regular expression is applied case-sensitively on the normalized form of
# the variable name: the section and variable parts are lower-cased. The
# subsection is left unchanged.
#
# @param out pointer to store the iterator
# @param cfg where to look for the variable
# @param name the variable's name
# @param regexp regular expression to filter which variables we're
# interested in. Use NULL to indicate all
# @return 0 or an error code.
#
git_config_multivar_iterator_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_config_iterator)),
    ct.POINTER(git_config),
    ct.c_char_p,
    ct.c_char_p)(
    ("git_config_multivar_iterator_new", dll), (
    (1, "out"),
    (1, "cfg"),
    (1, "name"),
    (1, "regexp"),))

# Return the current entry and advance the iterator
#
# The pointers returned by this function are valid until the next call
# to `git_config_next` or until the iterator is freed.
#
# @param entry pointer to store the entry
# @param iter the iterator
# @return 0 or an error code. GIT_ITEROVER if the iteration has completed
#
git_config_next = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_config_entry)),
    ct.POINTER(git_config_iterator))(
    ("git_config_next", dll), (
    (1, "entry"),
    (1, "iter"),))

# Free a config iterator
#
# @param iter the iterator to free
#
git_config_iterator_free = CFUNC(None,
    ct.POINTER(git_config_iterator))(
    ("git_config_iterator_free", dll), (
    (1, "iter"),))

# Set the value of an integer config variable in the config file
# with the highest level (usually the local one).
#
# @param cfg where to look for the variable
# @param name the variable's name
# @param value Integer value for the variable
# @return 0 or an error code
#
git_config_set_int32 = CFUNC(ct.c_int,
    ct.POINTER(git_config),
    ct.c_char_p,
    ct.c_int32)(
    ("git_config_set_int32", dll), (
    (1, "cfg"),
    (1, "name"),
    (1, "value"),))

# Set the value of a long integer config variable in the config file
# with the highest level (usually the local one).
#
# @param cfg where to look for the variable
# @param name the variable's name
# @param value Long integer value for the variable
# @return 0 or an error code
#
git_config_set_int64 = CFUNC(ct.c_int,
    ct.POINTER(git_config),
    ct.c_char_p,
    ct.c_int64)(
    ("git_config_set_int64", dll), (
    (1, "cfg"),
    (1, "name"),
    (1, "value"),))

# Set the value of a boolean config variable in the config file
# with the highest level (usually the local one).
#
# @param cfg where to look for the variable
# @param name the variable's name
# @param value the value to store
# @return 0 or an error code
#
git_config_set_bool = CFUNC(ct.c_int,
    ct.POINTER(git_config),
    ct.c_char_p,
    ct.c_int)(
    ("git_config_set_bool", dll), (
    (1, "cfg"),
    (1, "name"),
    (1, "value"),))

# Set the value of a string config variable in the config file
# with the highest level (usually the local one).
#
# A copy of the string is made and the user is free to use it
# afterwards.
#
# @param cfg where to look for the variable
# @param name the variable's name
# @param value the string to store.
# @return 0 or an error code
#
git_config_set_string = CFUNC(ct.c_int,
    ct.POINTER(git_config),
    ct.c_char_p,
    ct.c_char_p)(
    ("git_config_set_string", dll), (
    (1, "cfg"),
    (1, "name"),
    (1, "value"),))

# Set a multivar in the local config file.
#
# The regular expression is applied case-sensitively on the value.
#
# @param cfg where to look for the variable
# @param name the variable's name
# @param regexp a regular expression to indicate which values to replace
# @param value the new value.
# @return 0 or an error code.
#
git_config_set_multivar = CFUNC(ct.c_int,
    ct.POINTER(git_config),
    ct.c_char_p,
    ct.c_char_p,
    ct.c_char_p)(
    ("git_config_set_multivar", dll), (
    (1, "cfg"),
    (1, "name"),
    (1, "regexp"),
    (1, "value"),))

# Delete a config variable from the config file
# with the highest level (usually the local one).
#
# @param cfg the configuration
# @param name the variable to delete
# @return 0 or an error code.
#
git_config_delete_entry = CFUNC(ct.c_int,
    ct.POINTER(git_config),
    ct.c_char_p)(
    ("git_config_delete_entry", dll), (
    (1, "cfg"),
    (1, "name"),))

# Deletes one or several entries from a multivar in the local config file.
#
# The regular expression is applied case-sensitively on the value.
#
# @param cfg where to look for the variables
# @param name the variable's name
# @param regexp a regular expression to indicate which values to delete
#
# @return 0 or an error code
#
git_config_delete_multivar = CFUNC(ct.c_int,
    ct.POINTER(git_config),
    ct.c_char_p,
    ct.c_char_p)(
    ("git_config_delete_multivar", dll), (
    (1, "cfg"),
    (1, "name"),
    (1, "regexp"),))

# Perform an operation on each config variable.
#
# The callback receives the normalized name and value of each variable
# in the config backend, and the data pointer passed to this function.
# If the callback returns a non-zero value, the function stops iterating
# and returns that value to the caller.
#
# The pointers passed to the callback are only valid as long as the
# iteration is ongoing.
#
# @param cfg where to get the variables from
# @param callback the function to call on each variable
# @param payload the data to pass to the callback
# @return 0 on success, non-zero callback return value, or error code
#
git_config_foreach = CFUNC(ct.c_int,
    ct.POINTER(git_config),
    git_config_foreach_cb,
    ct.c_void_p)(
    ("git_config_foreach", dll), (
    (1, "cfg"),
    (1, "callback"),
    (1, "payload"),))

# Iterate over all the config variables
#
# Use `git_config_next` to advance the iteration and
# `git_config_iterator_free` when done.
#
# @param out pointer to store the iterator
# @param cfg where to get the variables from
# @return 0 or an error code.
#
git_config_iterator_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_config_iterator)),
    ct.POINTER(git_config))(
    ("git_config_iterator_new", dll), (
    (1, "out"),
    (1, "cfg"),))

# Iterate over all the config variables whose name matches a pattern
#
# Use `git_config_next` to advance the iteration and
# `git_config_iterator_free` when done.
#
# The regular expression is applied case-sensitively on the normalized form of
# the variable name: the section and variable parts are lower-cased. The
# subsection is left unchanged.
#
# @param out pointer to store the iterator
# @param cfg where to ge the variables from
# @param regexp regular expression to match the names
# @return 0 or an error code.
#
git_config_iterator_glob_new = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_config_iterator)),
    ct.POINTER(git_config),
    ct.c_char_p)(
    ("git_config_iterator_glob_new", dll), (
    (1, "out"),
    (1, "cfg"),
    (1, "regexp"),))

# Perform an operation on each config variable matching a regular expression.
#
# This behaves like `git_config_foreach` with an additional filter of a
# regular expression that filters which config keys are passed to the
# callback.
#
# The regular expression is applied case-sensitively on the normalized form of
# the variable name: the section and variable parts are lower-cased. The
# subsection is left unchanged.
#
# The regular expression is applied case-sensitively on the normalized form of
# the variable name: the case-insensitive parts are lower-case.
#
# @param cfg where to get the variables from
# @param regexp regular expression to match against config names
# @param callback the function to call on each variable
# @param payload the data to pass to the callback
# @return 0 or the return value of the callback which didn't return 0
#
git_config_foreach_match = CFUNC(ct.c_int,
    ct.POINTER(git_config),
    ct.c_char_p,
    git_config_foreach_cb,
    ct.c_void_p)(
    ("git_config_foreach_match", dll), (
    (1, "cfg"),
    (1, "regexp"),
    (1, "callback"),
    (1, "payload"),))

# Query the value of a config variable and return it mapped to
# an integer constant.
#
# This is a helper method to easily map different possible values
# to a variable to integer constants that easily identify them.
#
# A mapping array looks as follows:
#
#  git_configmap autocrlf_mapping[] = {
#      {GIT_CVAR_FALSE, NULL, GIT_AUTO_CRLF_FALSE},
#      {GIT_CVAR_TRUE, NULL, GIT_AUTO_CRLF_TRUE},
#      {GIT_CVAR_STRING, "input", GIT_AUTO_CRLF_INPUT},
#      {GIT_CVAR_STRING, "default", GIT_AUTO_CRLF_DEFAULT}};
#
# On any "false" value for the variable (e.g. "false", "FALSE", "no"), the
# mapping will store `GIT_AUTO_CRLF_FALSE` in the `out` parameter.
#
# The same thing applies for any "true" value such as "true", "yes" or "1", storing
# the `GIT_AUTO_CRLF_TRUE` variable.
#
# Otherwise, if the value matches the string "input" (with case insensitive comparison),
# the given constant will be stored in `out`, and likewise for "default".
#
# If not a single match can be made to store in `out`, an error code will be
# returned.
#
# @param out place to store the result of the mapping
# @param cfg config file to get the variables from
# @param name name of the config variable to lookup
# @param maps array of `git_configmap` objects specifying the possible mappings
# @param map_n number of mapping objects in `maps`
# @return 0 on success, error code otherwise
#
git_config_get_mapped = CFUNC(ct.c_int,
    ct.POINTER(ct.c_int),
    ct.POINTER(git_config),
    ct.c_char_p,
    ct.POINTER(git_configmap),
    ct.c_size_t)(
    ("git_config_get_mapped", dll), (
    (1, "out"),
    (1, "cfg"),
    (1, "name"),
    (1, "maps"),
    (1, "map_n"),))

# Maps a string value to an integer constant
#
# @param out place to store the result of the parsing
# @param maps array of `git_configmap` objects specifying the possible mappings
# @param map_n number of mapping objects in `maps`
# @param value value to parse
# @return 0 or an error code.
#
git_config_lookup_map_value = CFUNC(ct.c_int,
    ct.POINTER(ct.c_int),
    ct.POINTER(git_configmap),
    ct.c_size_t,
    ct.c_char_p)(
    ("git_config_lookup_map_value", dll), (
    (1, "out"),
    (1, "maps"),
    (1, "map_n"),
    (1, "value"),))

# Parse a string value as a bool.
#
# Valid values for true are: 'true', 'yes', 'on', 1 or any
#  number different from 0
# Valid values for false are: 'false', 'no', 'off', 0
#
# @param out place to store the result of the parsing
# @param value value to parse
# @return 0 or an error code.
#
git_config_parse_bool = CFUNC(ct.c_int,
    ct.POINTER(ct.c_int),
    ct.c_char_p)(
    ("git_config_parse_bool", dll), (
    (1, "out"),
    (1, "value"),))

# Parse a string value as an int32.
#
# An optional value suffix of 'k', 'm', or 'g' will
# cause the value to be multiplied by 1024, 1048576,
# or 1073741824 prior to output.
#
# @param out place to store the result of the parsing
# @param value value to parse
# @return 0 or an error code.
#
git_config_parse_int32 = CFUNC(ct.c_int,
    ct.POINTER(ct.c_int32),
    ct.c_char_p)(
    ("git_config_parse_int32", dll), (
    (1, "out"),
    (1, "value"),))

# Parse a string value as an int64.
#
# An optional value suffix of 'k', 'm', or 'g' will
# cause the value to be multiplied by 1024, 1048576,
# or 1073741824 prior to output.
#
# @param out place to store the result of the parsing
# @param value value to parse
# @return 0 or an error code.
#
git_config_parse_int64 = CFUNC(ct.c_int,
    ct.POINTER(ct.c_int64),
    ct.c_char_p)(
    ("git_config_parse_int64", dll), (
    (1, "out"),
    (1, "value"),))

# Parse a string value as a path.
#
# A leading '~' will be expanded to the global search path (which
# defaults to the user's home directory but can be overridden via
# `git_libgit2_opts()`.
#
# If the value does not begin with a tilde, the input will be
# returned.
#
# @param out placae to store the result of parsing
# @param value the path to evaluate
# @return 0 or an error code.
#
git_config_parse_path = CFUNC(ct.c_int,
    ct.POINTER(git_buf),
    ct.c_char_p)(
    ("git_config_parse_path", dll), (
    (1, "out"),
    (1, "value"),))

# Perform an operation on each config variable in a given config backend,
# matching a regular expression.
#
# This behaves like `git_config_foreach_match` except that only config
# entries from the given backend entry are enumerated.
#
# The regular expression is applied case-sensitively on the normalized form of
# the variable name: the section and variable parts are lower-cased. The
# subsection is left unchanged.
#
# @param backend where to get the variables from
# @param regexp regular expression to match against config names (can be NULL)
# @param callback the function to call on each variable
# @param payload the data to pass to the callback
# @return 0 or an error code.
#
git_config_backend_foreach_match = CFUNC(ct.c_int,
    ct.POINTER(git_config_backend),
    ct.c_char_p,
    git_config_foreach_cb,
    ct.c_void_p)(
    ("git_config_backend_foreach_match", dll), (
    (1, "backend"),
    (1, "regexp"),
    (1, "callback"),
    (1, "payload"),))

# Lock the backend with the highest priority
#
# Locking disallows anybody else from writing to that backend. Any
# updates made after locking will not be visible to a reader until
# the file is unlocked.
#
# You can apply the changes by calling `git_transaction_commit()`
# before freeing the transaction. Either of these actions will unlock
# the config.
#
# @param tx the resulting transaction, use this to commit or undo the
# changes
# @param cfg the configuration in which to lock
# @return 0 or an error code
#
git_config_lock = CFUNC(ct.c_int,
    ct.POINTER(ct.POINTER(git_transaction)),
    ct.POINTER(git_config))(
    ("git_config_lock", dll), (
    (1, "tx"),
    (1, "cfg"),))

# GIT_END_DECL
