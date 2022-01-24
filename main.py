import asyncio, random
 
async def rnd_sleep(t):
    await asyncio.sleep(t * random.random() * 2)
 
async def producer(queue):
    while True:
        token = random.random()
        print(f'produced {token}')
        if token < .05:
            break
        await queue.put(token)
        await rnd_sleep(.1)
 
async def consumer(queue):
    while True:
        token = await queue.get()
        await rnd_sleep(.3)
        queue.task_done()
        print(f'consumed {token}')

async def main():
    queue = asyncio.Queue()
    producers = [asyncio.create_task(producer(queue))
    for _ in range(3)]
    consumers = [asyncio.create_task(consumer(queue))for _ in range(10)]
    await asyncio.gather(*producers)
    print('---- done producing ----')
    await queue.join()
    for i in consumers:
      i.cancel()
 
asyncio.run(main())
