import random
import requests
from typing import List, Dict

class IPProxyPool:
    def __init__(self, proxies: List[str] = None):
        self.proxies = proxies or []
        self.verified_proxies = []
        
    def add_proxies(self, proxies: List[str]):
        self.proxies.extend(proxies)
        
    def verify_proxies(self, test_url: str = "http://httpbin.org/ip", timeout: int = 5):
        working_proxies = []
        for proxy in self.proxies:
            try:
                response = requests.get(test_url, 
                                      proxies={"http": proxy, "https": proxy},
                                      timeout=timeout)
                if response.status_code == 200:
                    working_proxies.append(proxy)
            except:
                continue
        self.verified_proxies = working_proxies
        return working_proxies
    
    def get_random_proxy(self) -> str:
        if not self.verified_proxies:
            raise ValueError("No verified proxies available")
        return random.choice(self.verified_proxies)
    
    def get_proxy_stats(self) -> Dict:
        return {
            "total": len(self.proxies),
            "verified": len(self.verified_proxies),
            "success_rate": len(self.verified_proxies)/len(self.proxies) if self.proxies else 0
        }
