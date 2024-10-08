import asyncio
import openai
import pandas as pd
import requests
from pyppeteer import launch

openai.api_key = 'YOUR_OPENAI_API_KEY'

with open('urls.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

# Function to fetch proxies from GeoNode API
def fetch_proxies():
    url = 'https://proxylist.geonode.com/api/proxy-list'
    params = {
        'limit': 500,
        'page': 1,
        'sort_by': 'lastChecked',
        'sort_type': 'desc',
        # You can add more parameters to filter proxies as needed
    }
    response = requests.get(url, params=params)
    data = response.json()
    proxies = pd.DataFrame(data['data'])
    return proxies

proxies = fetch_proxies()

def get_country_code(url):
    prompt = (
        f"From the URL '{url}', extract the country code if any. "
        "If the URL contains a country code or country name in any part "
        "(domain, subdomain, path), return ONLY the 2-letter country code "
        "(ISO Alpha-2 code). If no country code is found, return 'Unknown'."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that extracts country codes from URLs. "
                    "You output only the 2-letter country code or 'Unknown'."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    reply = response['choices'][0]['message']['content'].strip()
    return reply

def get_proxy_for_country(country_code):
    matching_proxies = proxies[proxies['country'] == country_code]
    if not matching_proxies.empty:
        # You can sort proxies by latency or uptime before selecting
        matching_proxies = matching_proxies.sort_values(by=['latency', 'upTime'], ascending=[True, False])
        proxy = matching_proxies.iloc[0]
        return proxy
    else:
        return None

async def take_screenshot(url, proxy_ip, proxy_port, proxy_protocol, output_file):
    proxy_url = f"{proxy_protocol}://{proxy_ip}:{int(proxy_port)}"
    browser = await launch(args=[f'--proxy-server={proxy_url}'])
    page = await browser.newPage()
    try:
        await page.goto(url, {'waitUntil': 'networkidle2', 'timeout': 60000})
        await page.screenshot({'path': output_file, 'fullPage': True})
        print(f"Screenshot saved to {output_file}")
    except Exception as e:
        print(f"Error loading {url}: {e}")
    finally:
        await browser.close()

async def main():
    for url in urls:
        print(f"\nProcessing URL: {url}")
        country_code = get_country_code(url).upper()
        print(f"Country code: {country_code}")
        if country_code == 'UNKNOWN':
            print("No country code found in URL. Skipping.")
            continue

        proxy = get_proxy_for_country(country_code)
        if proxy is None:
            print(f"No proxy found for country code {country_code}. Skipping.")
            continue

        proxy_ip = proxy['ip']
        proxy_port = proxy['port']
        proxy_protocols = proxy['protocols']
        # Use the first available protocol
        proxy_protocol = proxy_protocols[0] if isinstance(proxy_protocols, list) else proxy_protocols

        # Ensure protocol is in a format acceptable by Pyppeteer (e.g., 'http', 'socks5')
        if proxy_protocol not in ['http', 'https', 'socks4', 'socks5']:
            print(f"Unsupported proxy protocol {proxy_protocol}. Skipping.")
            continue

        output_file = f"screenshot_{url.replace('://', '_').replace('/', '_')}.png"

        try:
            await take_screenshot(url, proxy_ip, proxy_port, proxy_protocol, output_file)
        except Exception as e:
            print(f"Error taking screenshot of {url}: {e}")

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
