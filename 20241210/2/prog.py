import asyncio
import random
from math import log2, ceil

async def merge(A, B, start, middle, finish, event_in1, event_in2, event_out):
    await event_in1.wait()
    if middle < finish:
        await event_in2.wait()
    
    i, j, k = start, middle, start
    while i < middle and j < finish:
        if A[i] <= A[j]:
            B[k] = A[i]
            i += 1
        else:
            B[k] = A[j]
            j += 1
        k += 1
    while i < middle:
        B[k] = A[i]
        i += 1
        k += 1
    while j < finish:
        B[k] = A[j]
        j += 1
        k += 1
    event_out.set()

async def mtasks(A):
    N = len(A)
    B = [0] * N
    tasks = []
    events = [asyncio.Event() for _ in range(N)]
    
    for e in events: e.set()

    l = 1
    src, res = A.copy(), B
    
    while l < N:
        next_events = [asyncio.Event() for _ in range((N + 2 * l - 1) // (2 * l))]
        for i in range(0, N, 2 * l):
                task = merge(src, res, i, min(i + l, N), min(i + 2 * l, N), events[i // l], events[min(i + l, N) // l] if min(i + l, N) < N else asyncio.Event(), next_events[i // (2 * l)])
                tasks.append(asyncio.create_task(task))
    
        events = next_events
        src, res = res, src
        l *= 2
    
    return tasks, src


import sys
exec(sys.stdin.read())