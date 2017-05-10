# -*- coding: utf8 -*-
from __future__ import unicode_literals
import os
import sys
import json
import time
import traceback
from multiprocessing import Process, Semaphore
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.job import Job, JOB_COMMIT, JOB_PROCESSING
from utils.job_utils import get_function_from_module_and_function_name


class Q(object):
    def __init__(self, name, semaphores):
        self.name = name
        self.semaphore = Semaphore(semaphores)
        self.last_check_at = 0
        self.is_popped = False

qs = [
    Q('queue', 3),  # 通用并行队列
    Q('queue-s-1', 1),  # 串行队列1
    Q('queue-s-2', 1),  # 串行队列2
    Q('queue-s-3', 1),  # 串行队列3
]


def worker(job_id, semaphore):
    start_at = time.time()
    job = Job.objects(id=job_id).first()
    module_name = job.module_name
    function_name = job.function_name
    func = get_function_from_module_and_function_name(module_name, function_name)
    arguments = json.loads(job.arguments)
    args = arguments.get('args')
    kwargs = arguments.get('kwargs')

    results = ''
    try:
        results = func(*args, **kwargs)
        job.finish()
    except Exception, ex:
        job.exception()
        exc = traceback.format_exc()
        job.exceptions = exc

    end_at = time.time()
    duration = end_at - start_at
    job.results = results
    job.duration = duration
    job.save()
    semaphore.release()


def cycle():
    while True:
        is_popped = False
        for q in qs:
            if q.is_popped or time.time() - q.last_check_at > 2:
                try:
                    jobs = Job.objects(status=JOB_COMMIT, deleted_at=None, queue_type=q.name).order_by('created_at').all()
                    q.is_popped = False
                    for job in jobs:
                        if q.semaphore.get_value() > 0:
                            job.status = JOB_PROCESSING
                            q.semaphore.acquire()
                            p = Process(target=worker, args=(job.id, q.semaphore))
                            job.process_id = p._parent_pid
                            job.save()
                            p.start()

                            q.is_popped = True
                        else:
                            q.is_popped = False
                            break
                except Exception, ex:
                    time.sleep(1)
                    print ex

                is_popped |= q.is_popped

        # 如果队列里有数据，
        if not is_popped:
            time.sleep(2)


if __name__ == '__main__':
    cycle()
