import pytest
from base_spidernet.base_resolver import BaseResolver
from DNS.dns_resolver import DNSResolver

class TestDNSResolver:
    @pytest.fixture
    def resolver(self):
        return DNSResolver()

    def test_normal_resolution(self, resolver):
        result = resolver.resolve('example.com')
        assert len(result) > 0

    def test_invalid_domain(self, resolver):
        with pytest.raises(ValueError):
            resolver.resolve('nonexistentdomain123456.com')

    def test_custom_dns(self):
        custom_resolver = DNSResolver(['8.8.8.8'])
        result = custom_resolver.resolve('google.com')
        assert len(result) > 0

    def test_batch_resolve(self, resolver):
        domains = ['baidu.com', 'qq.com', '163.com']
        results = resolver.batch_resolve(domains)
        assert len(results) == 3
        for domain, ips in results.items():
            assert len(ips) > 0
