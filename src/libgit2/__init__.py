# Copyright (c) 2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib

from .__about__ import * ; del __about__  # noqa
from . import __config__ ; del __config__
from .__config__ import set_config as config

from ._git2 import * ; del _git2  # noqa
