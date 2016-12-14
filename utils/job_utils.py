# -*- coding: utf8 -*-
from __future__ import unicode_literals
from functools import wraps
from sys import modules
import json

from models.job import Job


def do_job(queue_key):
    def decorate(func):
        module_name, function_name = get_module_and_function_name(func)
        module = modules.get(module_name)
        module.__dict__[function_name] = func

        @wraps(func)
        def _decorate(*args, **kwargs):
            arguments = json.dumps(dict(args=args, kwargs=kwargs))  # 简单参数类型，不用过于复杂

            # 任务放入mongodb
            job = Job()
            job.module_name = module_name
            job.function_name = function_name
            job.arguments = arguments
            job.queue_type = queue_key
            job.save()

        return _decorate
    return decorate


def get_module_and_function_name(func):
    module_name = func.__module__
    function_name = 'origin_{0}'.format(func.__name__)
    return module_name, function_name


def get_function_from_module_and_function_name(module_name, function_name):
    __import__(module_name)
    module = modules.get(module_name)
    function = module.__dict__.get(function_name)
    return function