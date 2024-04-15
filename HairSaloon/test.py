import asyncio
from collections import deque

ip_list = ['192.168.100.1', '192.168.100.2', '192.168.100.5', '192.168.100.100', '192.168.100.92']


async def main_loop():
    a = 0
    while True:
        a += 1
        print(f"Main loop running for {a} seconds")
        await asyncio.sleep(1)


async def async_loop():
    while True:
        print(f"Async loop running in background...")
        await asyncio.sleep(3)


async def main():
    main_task = asyncio.create_task(main_loop())
    ping_task = asyncio.create_task(ping_ip(ip_list))

    await asyncio.gather(main_task, ping_task)


async def ping_ip(*args):
    ip_addresses = deque(*args)
    while True:
        ip_address = ip_addresses[0]
        process = await asyncio.create_subprocess_shell(
            f"ping -n 1 {ip_address}",
            stdout=asyncio.subprocess.PIPE)

        stdout = await process.communicate()
        if 'unreachable' in str(stdout[0]):
            print(f"{ip_address} is not reachable")
        else:
            print(f"{ip_address} is reachable")
        ip_addresses.rotate()
        await asyncio.sleep(1)


# ping_ip("127.0.0.1")
asyncio.run(main())
