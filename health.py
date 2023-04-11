import yaml
import requests
import time


class HealthCheck:
    def __init__(self):
        self.data = {}

    def check(self, site: dict):
        name = site['name']
        url = site['url']
        method = site['method'] if 'method' in site else 'GET'
        headers = site['headers'] if 'headers' in site else None
        body = site['body'] if 'body' in site else None
        result = self.request(url,method,headers=headers,body=body)
        if name not in self.data:
            self.data[name] = {'total':0, 'healthy':0}
        if result:
            self.data[name]['healthy'] += 1
        self.data[name]['total'] += 1
        print('URL {} has {}% availability percentage'.format(url, round(100 * self.data[name]['healthy'] / self.data[name]['total'])))
        return

    def request(self, url: str, method:str, headers: dict=None, body: str=None):
        try:
            r = requests.request(
                method=method,
                url=url,
                data=body,
                headers=headers
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
            time.sleep(15)
    
if __name__ == "__main__":
    health_check = HealthCheck()
    health_check.start()