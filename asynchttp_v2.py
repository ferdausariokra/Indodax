import aiohttp
import asyncio
import time
import ast
import json

pairs =    ['btc_idr', 'bts_idr','doge_idr','eth_idr','ltc_idr','nxt_idr','sumo_idr','ten_idr','xrp_idr',
                      'bts_btc','doge_btc','eth_btc','ltc_btc','nxt_btc','sumo_btc','ten_btc','xrp_btc', 'summaries']
"""
async def notify_channel(session, text):
    proxy = None
    url = 'https://api.telegram.org/bot[YOUR TELEGRAM BOT TOKEN]/sendMessage?chat_id=@[YOUR TELEGRAM CHANNEL]&text=' + text
    async with session.get(url, proxy=proxy) as response:
        if response.status != 200:
            response.raise_for_status()
        return await response.json()
"""

async def idx_fetch(session, pair, param):
    proxy = None
    url = 'https://indodax.com/api/' + pair + '/' + param
    async with session.get(url, proxy=proxy) as response:
        if response.status != 200:
            response.raise_for_status()
        return await response.json()

async def idx_fetch_all(session, pairs, param):
    results = await asyncio.gather(*[asyncio.create_task(idx_fetch(session, pair, param)) for pair in pairs])
    return results

async def main():    
    async with aiohttp.ClientSession() as session:
        htmls = await idx_fetch_all(session, pairs, 'depth')
        [print(pairs[i], "->", htmls[i]['buy'][0], htmls[i]['sell'][0]) for i in range(16)]
        
if __name__ == '__main__':
    while(1):
        s = time.perf_counter()
        asyncio.run(main())
        elapsed = time.perf_counter() - s
        print("time to fetch data %.2f" %elapsed, "seconds.")
        time.sleep(3)
