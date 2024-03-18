#!/usr/bin/env python3
import asyncio
import cowsay

clients: dict[str, asyncio.Queue] = {}

def handle_login(me: str | None, name: str) -> tuple[bool, str]:
    if me is None:
        if name not in cowsay.list_cows():
            return False, 'There is no such cow name.'
        if name in clients:
            return False, 'This name has already been taken by someone else.'
        clients[name] = asyncio.Queue()
        return True, 'Logged in successfully!'
    else:
        return False, 'You have already been logged in. You have to quit first to log in again.'


async def chat(reader, writer):
    me = None
    receive = None
    send = asyncio.create_task(reader.readline())
    quit_flag = False
    while not reader.at_eof() and not quit_flag:
        tasks = [send, receive] if receive else [send]
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            if task is send:
                input_text = task.result().decode().strip()
                match input_text.split():
                    case ['login', name]:
                        logged_in_flag, response = handle_login(me, name)
                        if logged_in_flag:
                            me = name
                            receive = asyncio.create_task(clients[me].get())
                        writer.write(f"{response}\n".encode())
                        await writer.drain()
                    case ['who']:
                        writer.write(f"Registered users: {' '.join(list(clients.keys()))}\n".encode())
                        await writer.drain()
                    case ['cows']:
                        available_names = set(cowsay.list_cows()) - set(clients.keys())
                        writer.write(f"Available cow names: {' '.join(available_names)}\n".encode())
                        await writer.drain()
                    case ['quit']:
                        writer.write("Farewell!\n".encode())
                        await writer.drain()
                        quit_flag = True
                        break
                send = asyncio.create_task(reader.readline())
            elif task is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{task.result()}\n".encode())
                await writer.drain()
    send.cancel()
    if receive:
        receive.cancel()
    print(me, "DONE")
    if me:
        del clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())