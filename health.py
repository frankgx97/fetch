import yaml
import requests
import time
from urllib.parse import urlparse


class HealthCheck:
    def __init__(self):
        self.data = {}

    def check(self, site: dict):
        url = site['url']
        method = site['method'] if 'method' in site else 'GET'
        headers = site['headers'] if 'headers' in site else None
        body = site['body'] if 'body' in site else None
        result = self.request(url, method, headers=headers, body=body)
        domain = urlparse(url).netloc
        if domain not in self.data:
            self.data[domain] = {'total':0, 'healthy':0}
        if result:
            self.data[domain]['healthy'] += 1
        self.data[domain]['total'] += 1
        return

    def request(self, url: str, method:str, headers: dict=None, body: str=None):
        try:
            r = requests.request(
                method=method,
                url=url,
                data=body,
                headers=headers,
                timeout=10
                )
            time_ms = r.elapsed.total_seconds() * 1000
            if 200 <= r.status_code <= 299 and time_ms <= 500:
                return True
        except:
            return False
        return False

    def read_config(self):
        try:
            f = open('config.yaml')
            content = f.read()
            config = yaml.safe_load(content)
            return config
        except:
            raise Exception('Error reading config file')
        
    def start(self):
        config = self.read_config()
        while True:
            for site in config:
                self.check(site)
            for domain in self.data:
                print('{} has {}% availability percentage'.format(domain, round(100 * self.data[domain]['healthy'] / self.data[domain]['total'])))
            time.sleep(15)
    
if __name__ == "__main__":
    health_check = HealthCheck()
    health_check.start()