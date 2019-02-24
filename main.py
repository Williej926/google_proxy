import argparse
import subprocess
import requests
import time
proxies = {}

instance_create_template="gcloud compute instances create-with-container {} " \
                         "--container-image gcr.io/tactile-shelter-224523/my-squid-image:latest  --zone {}"

def main(num_instances=5, zone="us-east4-a"):
    list_of_instances = ["proxy-{:02d}".format(i) for i in range(num_instances)]
    cmd = instance_create_template.format(" ".join(list_of_instances), zone)
    print(cmd)
    output = subprocess.check_output(cmd, shell=True)
    print(output)
    for line in output.splitlines():
        if line.startswith('Created'):
            continue
        tokens = line.split()
        if tokens[0].startswith("proxy"):
            proxies[tokens[0]] = "http://test:password@{}:3128".format(tokens[-2])
    # for i, instance in enumerate(list_of_instances):
    #     cmd = "gcloud compute ssh {} -- -D {} -Nf".format(instance, 20000+i)
    #     print(cmd)
    #     # subprocess.check_call(cmd, shell=True)
    #     proxies[instance] = 20000+i

def test_proxy():
    global proxies
    print(proxies)
    for proxy, proxy_url in proxies.items():
        proxies = {
            'http': proxy_url,
            'https': proxy_url,
        }

        resp = requests.get("http://ifconfig.me", proxies=proxies)
        print("test proxy {}: {}".format(proxy, resp.text))

if __name__=="__main__":
    main()
    print(proxies)
    time.sleep(60)
    test_proxy()