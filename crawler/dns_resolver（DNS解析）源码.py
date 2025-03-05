import random
import dns.resolver

class DNSResolver:
    def __init__(self, custom_dns=None):
        self.resolver = dns.resolver.Resolver()
        if custom_dns:
            self.resolver.nameservers = custom_dns
            
    def resolve(self, domain, record_type='A'):
        try:
            answers = self.resolver.resolve(domain, record_type)
            return [str(r) for r in answers]
        except dns.resolver.NoAnswer:
            return []
        except dns.resolver.NXDOMAIN:
            raise ValueError(f"Domain {domain} does not exist")
        except Exception as e:
            raise RuntimeError(f"DNS resolution failed: {str(e)}")

    def batch_resolve(self, domains):
        return {domain: self.resolve(domain) for domain in domains}
