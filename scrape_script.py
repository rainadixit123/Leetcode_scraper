import os
import re
import sys
import time
import zipfile
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def safe_wait(css_selector, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
    )

def strip_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def extract_solution_links(base_url):
    driver.get(base_url)
    safe_wait("a.no-underline[href*='/solutions/']")
    anchors = driver.find_elements(By.CSS_SELECTOR, "a.no-underline[href*='/solutions/']")
    return [anchor.get_attribute('href') for anchor in anchors[1:5]]

def extract_editorial_content(h3_elements):
    all_content = []
    for index, h3 in enumerate(h3_elements):
        h3_text = h3.text.strip()
        if "Approach" not in h3_text:
            continue
        approach_content = {"approach": h3_text, "html_between_h3_iframe": "", "solutions": []}
        try:
            siblings = h3.find_elements(By.XPATH, "following-sibling::*")
            html_chunks = []
            for sibling in siblings:
                if sibling.tag_name.lower() == "iframe":
                    break
                outer_html = driver.execute_script("return arguments[0].outerHTML;", sibling)
                html_chunks.append(outer_html)
            approach_content["html_between_h3_iframe"] = "\n".join(html_chunks)
        except:
            pass
        try:
            iframe = h3.find_element(By.XPATH, "following-sibling::iframe")
            driver.switch_to.frame(iframe)
            button_list = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.lang-btn-set button'))
            )
            language_content = {}
            for button in button_list:
                button.click()
                time.sleep(1)
                try:
                    textarea = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "textarea"))
                    )
                    language_content[button.text] = textarea.get_attribute('value')
                except:
                    language_content[button.text] = "No content found"
            approach_content["solutions"].append(language_content)
        except:
            pass
        driver.switch_to.default_content()
        all_content.append(approach_content)
    return all_content

def scrape_solutions(links, file):
    with open(file, "w", encoding="utf-8") as f:
        f.write("LeetCode Solution Codes\n" + "=" * 80 + "\n")
        for count, link in enumerate(links, start=1):
            f.write(f"\nOpening link {count}: {link}\n")
            driver.get(link)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='intuition' or @id='-intuition']"))
                )
                elem = driver.find_element(By.XPATH, "//*[@id='intuition' or @id='-intuition']")
                for sib in elem.find_elements(By.XPATH, "following-sibling::*"):
                    text = sib.text.strip()
                    if text:
                        f.write(text + "\n")
            except:
                f.write("Intuition not found\n")
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='approach' or @id='-approach']"))
                )
                elem = driver.find_element(By.XPATH, "//*[@id='approach' or @id='-approach']")
                for sib in elem.find_elements(By.XPATH, "following-sibling::*"):
                    text = sib.text.strip()
                    if text:
                        f.write(text + "\n")
            except:
                f.write("Approach not found\n")
            divs = driver.find_elements(By.CSS_SELECTOR, "div.font-menlo.relative.flex.h-10")
            for div in divs:
                lang = div.text.strip()
                div.click()
                time.sleep(2)
                try:
                    parent = div.find_element(By.XPATH, "parent::div")
                    code_div = parent.find_element(By.XPATH, "following-sibling::div")
                    code_block = code_div.find_element(By.XPATH, ".//pre//code")
                    f.write(f"\nLanguage: {lang}\nCode:\n{code_block.text.strip()}\n{'='*80}\n")
                except:
                    continue

def zip_folder(folder_path, zip_name):
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, folder_path)
            zipf.write(full_path, arcname)
    zipf.close()

# ------------ Main ------------

def main(problem):
    global driver
    problem = problem.strip().lower().replace(" ", "-")
    base_url = f"https://leetcode.com/problems/{problem}/editorial/"
    safe_name = problem.replace("-", "_")
    output_dir = "leetcode_solutions"
    os.makedirs(output_dir, exist_ok=True)
    file_editorial = os.path.join(output_dir, f"{safe_name}_editorial.txt")
    file_solutions = os.path.join(output_dir, f"{safe_name}_solutions.txt")

    options = Options()
    options.use_chromium = True
    options.add_argument("--start-maximized")
    EDGE_DRIVER_PATH = r"C:\Tools\edgedriver\msedgedriver.exe"
    driver = webdriver.Edge(service=Service(EDGE_DRIVER_PATH), options=options)

    try:
        driver.get(base_url)
        time.sleep(5)
        h3_elements = driver.find_elements(By.TAG_NAME, "h3")
        if any("Approach" in h3.text for h3 in h3_elements):
            print("📘 Scraping editorial...")
            data = extract_editorial_content(h3_elements)
            with open(file_editorial, "w", encoding="utf-8") as f:
                for content in data:
                    f.write(f"\n{content['approach']}\n{'-'*40}\n")
                    f.write(strip_html_tags(content['html_between_h3_iframe']) + "\n")
                    for lang, code in content['solutions'][0].items():
                        f.write(f"\nLanguage: {lang}\nCode:\n{code}\n{'='*80}\n")
        else:
            print("🔍 No editorial found, scraping solutions...")
            sol_links = extract_solution_links(f"https://leetcode.com/problems/{problem}/solutions/")
            scrape_solutions(sol_links, file_solutions)
    finally:
        driver.quit()

# ------------ Entry Point ------------

if __name__ == "__main__":
    # Replacing command-line arg with user input
    problem_input = input("🔍 Enter LeetCode problem name (e.g., Two Sum): ").strip()
    
    if not problem_input:
        print("❗ Please provide a valid problem name.")
        sys.exit(1)
    
    main(problem_input)

    # Always zip after running
    zip_folder("leetcode_solutions", "leetcode_solutions.zip")
    print("✅ Zipped as leetcode_solutions.zip")
    subprocess.Popen(f'explorer "{os.path.abspath("leetcode_solutions")}"')

