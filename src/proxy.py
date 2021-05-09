import requests
import json
import random


def get_proxy(country: str):
    # country = "DE"
    proxy_list_raw = requests.get(
        "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list"
    ).text.splitlines()
    proxy_list = [json.loads(raw_proxy) for raw_proxy in proxy_list_raw]
    proxy_list = list(
        filter(lambda proxy: proxy["type"] == "https", proxy_list))
    proxy_list = list(
        filter(lambda proxy: proxy["country"] == country, proxy_list))
    proxy_list.sort(key=lambda x: x["response_time"])
    # print(proxy_list[0])
    proxy = random.choice(proxy_list)
    # proxy = proxy_list[0]
    proxy_url = proxy["host"]+":"+str(proxy["port"])
    proxy_url = "103.213.213.22:83"
    print(proxy_url)
    return {
        "https": f"http://{proxy_url}",
        "http": f"http://{proxy_url}",
    }
