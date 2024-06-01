import os
import time
import argparse
import requests
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def download_image(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        response.raise_for_status()

        file_name = os.path.basename(url)
        with open(file_name, 'wb') as file:
            file.write(response.content)

        end_time = time.time()
        print(f"Downloaded {file_name} in {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

async def download_image_async(url, session):
    try:
        start_time = time.time()
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.read()

        file_name = os.path.basename(url)
        with open(file_name, 'wb') as file:
            file.write(content)

        end_time = time.time()
        print(f"Downloaded {file_name} in {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

async def main_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [download_image_async(url, session) for url in urls]
        await asyncio.gather(*tasks)

def main():
    parser = argparse.ArgumentParser(description="Download images from given URLs.")
    parser.add_argument('urls', nargs='+', help='List of image URLs')
    parser.add_argument('--threads', type=int, default=4, help='Number of threads')
    parser.add_argument('--processes', type=int, default=4, help='Number of processes')
    parser.add_argument('--async', action='store_true', help='Use asynchronous downloading')
    args = parser.parse_args()

    urls = args.urls
    use_async = args.async

    start_time = time.time()

    if use_async:
        asyncio.run(main_async(urls))
    else:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            executor.map(download_image, urls)

        with ProcessPoolExecutor(max_workers=args.processes) as executor:
            executor.map(download_image, urls)

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

if name == 'main':
    main()