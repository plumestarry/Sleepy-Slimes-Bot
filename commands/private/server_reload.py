import asyncio

global_time = 0

def reload(now_time):
    # with open("time.txt", "w", encoding="utf-8") as file:
    #     file.write(str(now_time))
    asyncio.get_event_loop().stop()
    print("Onebot stop")
    return None

