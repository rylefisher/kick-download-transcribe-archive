from more_itertools import first
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import sys
import ctypes
from datetime import datetime
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
import time
import traceback

def get_my_documents_folder():
    # get the path to the "My Documents" folder
    CSIDL_PERSONAL = 5
    SHGFP_TYPE_CURRENT = 0
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    return buf.value

class VideoAutomation:
    def __init__(self, path):
        self.env_loader = self.EnvLoader(path)
        self.first_video = None
        if 'true' in self.env_loader.get_value("monitor").lower().strip():
            while self.first_video is None:
                self.first_video = self.find_first_video()
                if self.first_video:
                    self.perform_upload(self.first_video)
                    time.sleep(30)
                    break
        else:
            try:
                self.first_video = self.find_first_video()
                self.perform_upload(self.first_video)
                time.sleep(30)
            except Exception as e:
                self.logger(e)

    class EnvLoader:
        def __init__(self, env_file_path=".env"):
            self.env_file_path = env_file_path
            self.env_template_path = f"{env_file_path}.template"
            self.check_env_file_exists()
            self.load_env()

        def check_env_file_exists(self):
            # create .env from template if it doesn't exist
            if not os.path.exists(self.env_file_path):
                if os.path.exists(self.env_template_path):
                    with open(self.env_template_path, 'r') as template:
                        template_content = template.read()
                    with open(self.env_file_path, 'w') as env_file:
                        env_file.write(template_content)
                else:
                    print(f"No .env file or template ({self.env_template_path}) found.")
                    with open(self.env_file_path, 'w') as env_file:
                        default_env = '''folder_path=C:\\Videos
email=myemail@gmail.com
password=123456Password
video_title=default_title
delete_video_when_done=False
open_log_when_done=True
monitor=True
headless_browser=False
'''
                        env_file.write(default_env)

        def load_env(self):
            # load environment variables
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
                env_path = os.path.join(base_path, self.env_file_path)
                load_dotenv(env_path)
            else:
                load_dotenv(self.env_file_path)

        def get_value(self, key):
            # retrieve environment variable value
            return os.getenv(key).strip()

    def find_first_video(self, file_extensions=None):
        if file_extensions is None:
            file_extensions = ['.mp4', '.mov']
        folder_path = self.env_loader.get_value('folder_path')
        # search for the first video file
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in file_extensions):
                    return os.path.join(root, file)
        return None

    @staticmethod
    def logger(e):
        # log errors
        with open('error.txt', 'w') as f:
            f.write(str(e))
            f.write(traceback.format_exc())

    def perform_upload(self, video_path):
        uploader = self.VideoUploader(video_path, self.env_loader)
        uploader.perform_upload()

    class VideoUploader:
        def __init__(self, video_path, env_loader):
            self.video_path = video_path
            self.env_loader = env_loader
            self.driver = None
            self.headless = self.string_to_binary(env_loader.get_value('headless_browser'))

        def string_to_binary(self, input_string):
            normalized_string = input_string.lower()
            return 0 if normalized_string in ["0", "false"] else 1

        def execute_selenium_operations(self, url):
            # initialize selenium webdriver
            options = Options()
            if self.headless:
                options.headless = True
            chrome_driver_service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=chrome_driver_service, options=options)
            self.driver.get(url)
            time.sleep(1)

        def perform_upload(self):
            try:
                self.execute_selenium_operations("https://rumble.com/upload.php")
                self.login()
                self.prepare_video_upload()
                self.fill_video_details()
                self.upload_and_finalize()
            except Exception as e:
                VideoAutomation.logger(e)
            self.cleanup()

        def login(self):
            # perform login operation
            email = self.env_loader.get_value('email')
            password = self.env_loader.get_value('password')
            self.driver.find_element(By.CSS_SELECTOR, "#login-username").send_keys(email)
            self.driver.find_element(By.CSS_SELECTOR, "#login-password").send_keys(password)
            self.driver.find_element(By.CSS_SELECTOR, ".login-button").click()
            time.sleep(5)

        def prepare_video_upload(self):
            # prepare video upload via hidden input
            self.driver.execute_script("""
                var fileInput = document.createElement('input');
                fileInput.type = 'file';
                fileInput.id = 'seleniumFileInput';
                fileInput.style.display = 'none';
                document.body.appendChild(fileInput);
            """)
            file_input = self.driver.find_element(By.ID, "seleniumFileInput")
            file_input.send_keys(self.video_path)
            target_element = self.driver.find_element(By.CSS_SELECTOR, "#Filedata")
            time.sleep(2)
            if not (target_element.tag_name.lower() == 'input' and target_element.get_attribute('type') == 'file'):
                print("The target element is not an input of type 'file'. Unable to set the file path directly.")
            else:
                target_element.send_keys(self.video_path)
            time.sleep(2)

        def fill_video_details(self):
            # fill video details
            current_day_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            title = self.env_loader.get_value('video_title')
            self.driver.find_element(By.CSS_SELECTOR, "#title").send_keys(f'{title} - {current_day_time}')
            self.driver.find_element(By.CSS_SELECTOR, "#description").send_keys(f"{title} stream archive")
            self.set_category("Entertainment", "Entertainment Life")

        def set_category(self, primary, secondary):
            # set video category
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            primary_input = self.driver.find_element(By.XPATH, "//input[@data-default-placeholder='- Primary category -']")
            primary_input.click()  # Focus on primary input
            primary_input.send_keys(f"{primary}\n")  # Send keys to primary input
            secondary_input = self.driver.find_element(By.XPATH, "//input[@data-default-placeholder='- Secondary category -']")
            secondary_input.click()  # Focus on secondary input
            secondary_input.send_keys(f"{secondary}\n")  # Send keys to secondary input

        def upload_and_finalize(self):
            # upload video and finalize
            time.sleep(10)
            found = False
            counter = 100
            while not found and counter > 0:
                try:
                    upload_complete_indicator = self.driver.find_element(By.CSS_SELECTOR, ".upload-percent > h2")
                    if "100%" in upload_complete_indicator.text:
                        submit_button = self.driver.find_element(By.CSS_SELECTOR, "#submitForm")
                        submit_button.click()
                        found = True
                    else:
                        time.sleep(10)
                except Exception as e:
                    print(str(e))
                    time.sleep(10)
                    counter -= 1
                time.sleep(5)
            self.interact_with_checkboxes()
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "#submitForm2")
            submit_button.click()
            time.sleep(2)
            self.get_url()

        def interact_with_checkboxes(self):
            # interact with checkboxes
            try:
                self.with_scroll()
            except Exception as e:
                print(str(e))
            try:
                self.with_javascript()
            except Exception as e:
                print(str(e))
            try:
                self.with_sel()
            except Exception as e:
                print(str(e))

        def with_scroll(self):
            # scroll to and click checkboxes
            for checkbox_id in ["crights", "cterms"]:
                checkbox = self.driver.find_element(By.ID, checkbox_id)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                checkbox.click()

        def with_javascript(self):
            # javascript click checkboxes
            for checkbox_id in ["crights", "cterms"]:
                self.driver.execute_script(f"document.getElementById('{checkbox_id}').click();")

        def with_sel(self):
            # use selenium to click checkboxes
            from selenium.common.exceptions import ElementNotInteractableException
            for checkbox_id in ["crights", "cterms"]:
                retries = 3
                for _ in range(retries):
                    try:
                        checkbox = self.driver.find_element(By.ID, checkbox_id)
                        checkbox.click()
                        break
                    except ElementNotInteractableException:
                        time.sleep(1)

        def get_url(self):
            # retrieve video url
            a_element = self.driver.find_element(By.CLASS_NAME, "round-button")
            href = a_element.get_attribute("href")
            full_href = self.driver.current_url + href if not href.startswith("http") else href
            docs = get_my_documents_folder()
            log_file_path = docs + "\\href_log.txt"
            href_exists = False
            try:
                with open(log_file_path, "r") as file:
                    if href in file.read():
                        href_exists = True
            except FileNotFoundError:
                pass
            if not href_exists:
                current_date = datetime.now().strftime("%Y-%m-%d")
                if os.path.exists(log_file_path):
                    with open(log_file_path, "r+") as file:
                        content = file.read()
                        file.seek(0, 0)
                        file.write(f"{current_date}, {full_href}\n{content}")
                else:
                    with open(log_file_path, "w") as file:
                        file.write(f"{current_date}, {full_href}\n")
            else:
                print("Href already exists in the log file.")
            if self.env_loader.get_value('open_log_when_done'):
                os.system(log_file_path)

        def cleanup(self):
            pass
            # cleanup resources
            # if self.env_loader.get_value('delete_video_when_done'):
            #    os.remove(self.video_path)
            # if self.driver:
            #    self.driver.quit()

if __name__ == "__main__":
    app = VideoAutomation(".env")
