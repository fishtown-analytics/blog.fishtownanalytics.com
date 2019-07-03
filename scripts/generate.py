
import yaml
import requests
import sys

if len(sys.argv) != 2:
    print("Usage: {} [validate (0 or 1)]".format(sys.argv[0]))
    sys.exit(1)

VALIDATE = int(sys.argv[1]) != 0

def validate_url(url):
    resp = requests.get(url)
    print("Validating url: {}".format(url))
    if resp.status_code != 200:
        msg = "Bad code ({}) for url: {}".format(resp.status_code, url)
        print("ERROR: {}".format(msg))
        raise RuntimeError(msg)

with open('urls.yml') as fh:
    contents = fh.read()
    urls = yaml.safe_load(contents)

from_domain = urls['domain']

bad_urls = []
all_urls = []
for i, url in enumerate(urls['urls']):
    from_path = url['from']
    from_url = "{}{}".format(from_domain, from_path)
    to_url = url['to']

    if VALIDATE:
        try:
            validate_url(from_url)
        except RuntimeError as e:
            bad_urls.append(from_url)

        try:
            validate_url(to_url)
        except RuntimeError as e:
            bad_urls.append(to_url)

    all_urls.append((from_path, to_url, "301"))

if len(bad_urls) > 0:
    raise RuntimeError("bad urls:\n -{}".format("\n -".join(bad_urls)))


with open("_redirects", "w") as fh:
    lines = ("      ".join(line) for line in all_urls)
    doc = "\n".join(lines)
    fh.write(doc)
