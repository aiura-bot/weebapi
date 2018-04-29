# -*- coding: utf-8 -*-

import logging
import sys
import traceback

import aiohttp

from weebapi import __version__
from .errors import *

logger = logging.getLogger()


class krequest(object):
    def __init__(self, return_json=True, global_headers={}, **kwargs):
        self.bot = kwargs.get("bot", None)
        self.headers = {
            "User-Agent": "{}WeebAPI.py/{} (Github: AndyTempel) KRequests/alpha "
                          "(Custom asynchronous HTTP client)".format(
                f"{self.bot.user.username}/{self.bot.user.discriminator} " if self.bot else "", __version__),
            "X-Powered-By": "{}".format(sys.version)
        }
        self.return_json = return_json
        for name, value in global_headers:
            logger.info(f"WEEB.SH Added global header {name}")
            self.headers.update({
                name: value
            })

        logger.debug(f"Here are global headers: {str(self.headers)}")

    async def _proc_resp(self, response):
        logger.debug(f"Request {response.method}: {response.url}")
        logger.debug(f"Response headers: {str(response.headers)}")
        if self.return_json:
            try:
                resp = await response.json()
                logger.debug(f"Response content: {str(resp)}")
                return resp
            except Exception:
                print(traceback.format_exc())
                print(response)
                resp = await response.text()
                logger.debug(f"Response content: {str(resp)}")
                return {}
        else:
            resp = await response.text()
            logger.debug(f"Response content: {str(resp)}")
            return resp

    async def get(self, url, params=None, headers=None, verify=True):
        headers = headers or {}
        headers.update(self.headers)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=verify)) as session:
            async with session.get(url, params=params, headers=headers) as resp:
                return await self._proc_resp(resp)

    async def delete(self, url, params=None, headers=None, verify=True):
        headers = headers or {}
        headers.update(self.headers)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=verify)) as session:
            async with session.delete(url, params=params, headers=headers) as resp:
                return await self._proc_resp(resp)

    async def post(self, url, data=None, json=None, headers=None, verify=True):
        headers = headers or {}
        headers.update(self.headers)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=verify)) as session:
            if json is not None:
                async with session.post(url, json=json, headers=headers) as resp:
                    return await self._proc_resp(resp)
            else:
                async with session.post(url, data=data, headers=headers) as resp:
                    return await self._proc_resp(resp)

    async def download_get(self, url, filename, params=None, headers=None, verify=True):
        headers = headers or {}
        headers.update(self.headers)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=verify)) as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status != 200:
                    raise Forbidden
                with open(filename, 'wb') as f_handle:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f_handle.write(chunk)
                await response.release()

    async def download_post(self, url, filename, data=None, json=None, headers=None, verify=True):
        headers = headers or {}
        headers.update(self.headers)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=verify)) as session:
            if json is not None:
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=verify)) as session:
                    async with session.post(url, json=json, headers=headers) as response:
                        if response.status != 200:
                            raise Forbidden
                        with open(filename, 'wb') as f_handle:
                            while True:
                                chunk = await response.content.read(1024)
                                if not chunk:
                                    break
                                f_handle.write(chunk)
                        await response.release()
            else:
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=verify)) as session:
                    async with session.post(url, data=data, headers=headers) as response:
                        if response.status != 200:
                            raise Forbidden
                        with open(filename, 'wb') as f_handle:
                            while True:
                                chunk = await response.content.read(1024)
                                if not chunk:
                                    break
                                f_handle.write(chunk)
                        await response.release()
