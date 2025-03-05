import pytest
from base_spidernet.base_resolver import BaseResolver
from IP.ip_resolver import IPProxyPool
from unittest import mock

class TestIPProxyPool:
    @pytest.fixture
    def pool(self):
        return IPProxyPool(["http://proxy1:8080", "http://proxy2:8080"])
        
    def test_add_proxies(self, pool):
        pool.add_proxies(["http://proxy3:8080"])
        assert len(pool.proxies) == 3
        
    def test_verification(self, pool):
        with mock.patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            working = pool.verify_proxies()
            assert len(working) == 2
        
    def test_random_proxy(self, pool):
        pool.verified_proxies = ["http://good:8080"]
        assert pool.get_random_proxy() == "http://good:8080"
        
    def test_stats(self, pool):
        stats = pool.get_proxy_stats()
        assert stats["total"] == 2
        assert stats["verified"] == 0
