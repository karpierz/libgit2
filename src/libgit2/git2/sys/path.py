# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa

# GIT_BEGIN_DECL

# The kinds of git-specific files we know about.
#
# The order needs to stay the same to not break the `gitfiles`
# array in path.c
#
git_path_gitfile = ct.c_int
(   # Check for the .gitignore file
    GIT_PATH_GITFILE_GITIGNORE,
    # Check for the .gitmodules file
    GIT_PATH_GITFILE_GITMODULES,
    # Check for the .gitattributes file
    GIT_PATH_GITFILE_GITATTRIBUTES,
) = range(0, 3)

# The kinds of checks to perform according to which filesystem we are trying to
# protect.
#
git_path_fs = ct.c_int
(   # Do both NTFS- and HFS-specific checks
    GIT_PATH_FS_GENERIC,
    # Do NTFS-specific checks only
    GIT_PATH_FS_NTFS,
    # Do HFS-specific checks only
    GIT_PATH_FS_HFS,
) =  range(0, 3)

# Check whether a path component corresponds to a .git$SUFFIX
# file.
#
# As some filesystems do special things to filenames when
# writing files to disk, you cannot always do a plain string
# comparison to verify whether a file name matches an expected
# path or not. This function can do the comparison for you,
# depending on the filesystem you're on.
#
# @param path the path component to check
# @param pathlen the length of `path` that is to be checked
# @param gitfile which file to check against
# @param fs which filesystem-specific checks to use
# @return 0 in case the file does not match, a positive value if
#         it does; -1 in case of an error
#
git_path_is_gitfile = CFUNC(ct.c_int,
    ct.c_char_p,
    ct.c_size_t,
    git_path_gitfile,
    git_path_fs)(
    ("git_path_is_gitfile", dll), (
    (1, "path"),
    (1, "pathlen"),
    (1, "gitfile"),
    (1, "fs"),))

# GIT_END_DECL
