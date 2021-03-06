# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from logging import getLogger
import os
from subprocess import PIPE, Popen
import sys

from ..base.context import context
from ..utils import wrap_subprocess_call
from ..gateways.disk.delete import rm_rf


def execute(args, parser):
    on_win = sys.platform == "win32"

    call = " ".join(args.executable_call)
    prefix = args.prefix or os.getenv("CONDA_PREFIX") or context.root_prefix
    script_caller, command_args = wrap_subprocess_call(on_win, context.root_prefix, prefix, call)
    process = Popen(command_args, universal_newlines=True, stdout=PIPE, stderr=PIPE)
    for line in process.stdout:
        sys.stdout.write(line)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        log = getLogger(__name__)
        log.error("Subprocess for 'conda run' command failed.  Stderr was:\n{}".format(stderr))
    if script_caller is not None:
        rm_rf(script_caller)
