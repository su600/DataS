# 异步程序 test
import asyncio
global i
i=0
async def count():

    while 1:
        global i
        i+=1
        print(i)
        await asyncio.sleep(1)


async def count2():
    pass
    # try:
    #     while 1:
    #         await asyncio.sleep(1)
    # except KeyboardInterrupt:
    #     print(i)


async def main():
    await asyncio.gather(count(), count2())

asyncio.run(main())