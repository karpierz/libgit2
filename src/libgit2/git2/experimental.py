# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

# Copyright (C) the libgit2 contributors. All rights reserved.
#
# This file is part of libgit2, distributed under the GNU GPL v2 with
# a Linking Exception. For full terms see the included COPYING file.

# This file exists to support users who build libgit2 with a bespoke
# build system and do not use our cmake configuration. Normally, cmake
# will create `experimental.h` from the `experimental.h.in` file and
# will include the generated file instead of this one. For non-cmake
# users, we bundle this `experimental.h` file which will be used
# instead.
