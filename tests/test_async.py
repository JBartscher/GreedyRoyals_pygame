import asyncio
import time
import sys


async def countdown(time_left):
    t = time.localtime(time_left)
    print(t.tm_sec)
    time.sleep(0.5)  # im spiel besser weglassen
    print("\n")


async def do_other_stuff():
    print("other stuff is done")


async def loop_it():
    endtime = time.time() + 10

    while time.time() < endtime:
        time_left = endtime - time.time()
        await asyncio.gather(countdown(time_left), do_other_stuff())
    print("done")


if __name__ == "__main__":
    print(sys.version_info)
    s = time.perf_counter()

    if sys.version_info.major == 3 and sys.version_info.minor < 7:
        # python 3.6
        loop = asyncio.get_event_loop()
        loop.run_until_complete(loop_it())
    else:
        # python 3.8
        asyncio.run(loop_it())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
