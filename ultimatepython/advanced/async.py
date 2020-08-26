import asyncio
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4


@dataclass
class TaskRecord:
    """Task record with useful metadata."""

    tid: int
    queued_at: datetime
    started_at: datetime


def current_time():
    """Return current time that is timezone-naive."""
    return datetime.now()


async def start_task(delay, task_id):
    """Start task_id after a certain delay in seconds."""
    queue_time = current_time()
    print(f"{queue_time} -> Queue task {task_id[:16]}...")
    await asyncio.sleep(delay)
    start_time = current_time()
    print(f"{start_time} -> Start task {task_id[:16]}...")
    return TaskRecord(task_id, queue_time, start_time)


async def start_batch():
    """Start a batch of tasks concurrently.

    Each item in the `tasks` list is a `Task` which is an instance of
    a `Future`. The `Task` instance was created by providing a coroutine
    instance from `start_task` into the `create_task` function.

    After awaiting the list of tasks, we get a list of `TaskRecord` items
    with characteristics that we expect.
    """
    print(f"{current_time()} -> Send kickoff email")

    tasks = [asyncio.create_task(start_task(i * .01, uuid4().hex))
             for i in range(1, 5)]

    # Gather all tasks for batch start
    task_records = await asyncio.gather(*tasks)
    for record in task_records:
        assert record.queued_at < record.started_at

    print(f"{current_time()} -> Send confirmation email")


def main():
    asyncio.run(start_batch())


if __name__ == "__main__":
    main()
