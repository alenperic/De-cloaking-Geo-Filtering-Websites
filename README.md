# De-cloaking Scammer & Fake Websites Using Geo-Filtering Detection

The script accepts a list of URLs, each on one line. For each URL, it queries the ChatGPT API to determine if the URL includes any geolocation data, then returns **ONLY** the country code. The country code is then compared against a list of proxies, and the matching country code proxy is used to take a screenshot of the website through **Pyppeteer**. This script is intended to be used for de-cloaking websites that are using geo-filtering.

## Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.7+**
- Required Python packages:
  ```bash
  pip install asyncio openai pandas requests pyppeteer
  ```
- An **OpenAI API Key**: You can get one by signing up at [OpenAI](https://platform.openai.com/).

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/geo-filtering-detection.git
   cd geo-filtering-detection
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API Key**:

   - Open the script file (e.g., `script.py`).
   - Replace `'YOUR_OPENAI_API_KEY'` with your actual OpenAI API key.

## Usage

1. **Prepare your list of URLs**:

   - Create a file named `urls.txt`.
   - Add the URLs you want to process, each on its own line.

2. **Run the script**:

   ```bash
   python script.py
   ```

3. **How the script works**:

   - Reads the list of URLs from `urls.txt`.
   - For each URL:
     - Queries the ChatGPT API to extract any country code from the URL.
     - Fetches a list of proxies from [GeoNode's free proxy list](https://geonode.com/free-proxy-list).
     - Matches the extracted country code with the proxies' country codes.
     - Uses a matching proxy to take a screenshot of the website using Pyppeteer.
     - Saves the screenshot in the current directory with a filename based on the URL.

## Notes

- **Proxy Source**: The proxies are obtained from [GeoNode](https://geonode.com/free-proxy-list).
- **Proxy Reliability**: Free proxies can be unreliable. If a proxy fails, the script will skip that URL.
- **Error Handling**: The script includes basic error handling, but you can enhance it as needed.
- **Customization**: Feel free to modify the script to improve proxy selection, add logging, or adjust the screenshot settings.

## Troubleshooting

- **OpenAI API Errors**: Ensure your API key is correct and that you have sufficient quota.
- **Pyppeteer Issues**: If you encounter issues with Pyppeteer, it might be due to missing dependencies or issues with Chromium download. Refer to the [Pyppeteer documentation](https://pyppeteer.github.io/pyppeteer/) for help.
- **Proxy Connectivity**: Some proxies might be dead or not support the required protocols. You may need to adjust the proxy selection logic.

## License

This project is open-source. You're free to use and modify it according to your needs.

## Contact

If you have any questions or suggestions, feel free to reach out.

---

*Happy de-cloaking!*
