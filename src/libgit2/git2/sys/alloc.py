# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

from ..common import *  # noqa

# GIT_BEGIN_DECL

# An instance for a custom memory allocator
#
# Setting the pointers of this structure allows the developer to implement
# custom memory allocators. The global memory allocator can be set by using
# "GIT_OPT_SET_ALLOCATOR" with the `git_libgit2_opts` function. Keep in mind
# that all fields need to be set to a proper function.
#
class git_allocator(ct.Structure):
    _fields_ = [
    # Allocate `n` bytes of memory
    ("gmalloc",  GIT_CALLBACK(ct.c_void_p,
                     ct.c_size_t,  # n
                     ct.c_char_p,  # file
                     ct.c_int)),   # line

    # This function shall deallocate the old object `ptr` and return a
    # pointer to a new object that has the size specified by `size`.
    # In case `ptr` is `NULL`, a new array shall be allocated.
    #
    ("grealloc", GIT_CALLBACK(ct.c_void_p,
                     ct.c_void_p,  # ptr
                     ct.c_size_t,  # size
                     ct.c_char_p,  # file
                     ct.c_int)),   # line

    # This function shall free the memory pointed to by `ptr`.
    # In case `ptr` is `NULL`, this shall be a no-op.
    #
    ("gfree",    GIT_CALLBACK(None,
                     ct.c_void_p)),  # ptr
]

# Initialize the allocator structure to use the `stdalloc` pointer.
#
# Set up the structure so that all of its members are using the standard
# "stdalloc" allocator functions. The structure can then be used with
# `git_allocator_setup`.
#
# @param allocator The allocator that is to be initialized.
# @return An error code or 0.
#
# ct.c_int git_stdalloc_init_allocator(ct.POINTER(git_allocator) allocator)

# Initialize the allocator structure to use the `crtdbg` pointer.
#
# Set up the structure so that all of its members are using the "crtdbg"
# allocator functions. Note that this allocator is only available on Windows
# platforms and only if libgit2 is being compiled with "-DMSVC_CRTDBG".
#
# @param allocator The allocator that is to be initialized.
# @return An error code or 0.
#
# ct.c_int git_win32_crtdbg_init_allocator(ct.POINTER(git_allocator) allocator)

# GIT_END_DECL
