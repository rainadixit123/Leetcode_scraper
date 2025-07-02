# Leetcode_scraper
A powerful Selenium-based Python script that automatically scrapes editorials and/or community solutions from the top 100 LeetCode problems. If an editorial is unavailable for a problem, it intelligently falls back to extract the most relevant community solution instead. All extracted content is saved in organized .txt files and finally zipped into a single archive.

## 📦 Requirements

- **Python 3.8+**
- **Microsoft Edge Browser** installed
- **Edge WebDriver** downloaded and placed at:
  
C:\Tools\edgedriver\msedgedriver.exe


> 🔗 Download WebDriver: [https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

- **Python Packages**:

Install using:

```bash
pip install -r requirements.txt
