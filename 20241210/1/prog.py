import asyncio
import itertools

async def writer(queue, delay, event, writer_id):
    for number in itertools.count():
        await asyncio.sleep(delay)
        await queue.put(f"{number}_{writer_id}")
        if event.is_set():
            break

async def stacker(queue, stack, event):
    while not event.is_set() or not queue.empty():
        item = await queue.get()
        stack.append(item)
        queue.task_done()

async def reader(stack, count, delay, event):
    await asyncio.sleep(delay)
    for _ in range(count):
        while not stack:
            await asyncio.sleep(0.01)
        item = stack.pop(0)
        print(item)
        await asyncio.sleep(delay)
    event.set()

async def main():
    delay1, delay2, delay3, count = eval(input())
    queue = asyncio.Queue()
    stack = []

    event = asyncio.Event()

    writer1_task = asyncio.create_task(writer(queue, delay1, event, delay1))
    writer2_task = asyncio.create_task(writer(queue, delay2, event, delay2))
    stacker_task = asyncio.create_task(stacker(queue, stack, event))
    reader_task = asyncio.create_task(reader(stack, count, delay3, event))

    await asyncio.gather(writer1_task, writer2_task, stacker_task, reader_task)

if __name__ == "__main__":
    asyncio.run(main())