from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import time, csv

from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

driver.get('https://web.whatsapp.com/')

#wait 60 secs to allow for the user to manually scan the Whatsapp Web QR code to log on
el_side = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "side")))

#locate the search box
el_search = el_side.find_element(By.XPATH, "//div[contains(@title, 'Search')]")
print("Logged in and located search box:", el_search)


def split_to_list(numbers_string):
    
    # Remove the triple quotes and any surrounding whitespace
    numbers_string = numbers_string.strip("'''").strip()

    # Split the string by commas and convert it into a list of numbers
    number_list = numbers_string.split(", ")
    return number_list


#define a function that adds contact_to_add to group_name
def remove_from_group(user_names, group_name):
    #find chat with the correct title
    el_target_chat = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@title='%s']" % (group_name))))
    el_target_chat.click()
        
    # #wait for it to load by detecting that the header changed with the new title
    # el_header_title = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//header//span[@title='%s']" % (group_name))))
    
    #click on the menu button
    el_menu_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//div[@data-testid='conversation-menu-button']")))
    el_menu_button.click()
    
    #click on the Group Info button
    el_group_info = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='app']//li//div[@aria-label='Group info']")))
    el_group_info.click()    
    


    for user_name in user_names:
        try:
            print('Attempting to remove in ', user_name.replace('\n', ''), ":")
            # Locate and click on the user's name in the group
            user_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@title="'+user_name+'"]')))
            time.sleep(1)
            # Create an instance of ActionChains
            actions = ActionChains(driver)

            # Perform the right-click action
            actions.context_click(user_element).perform()
            # user_element.click()
        except Exception as e:
            print(e)
            continue
        
        remove_option = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//li[@data-testid="mi-grp-remove-participant"]')))
        
        remove_option.click()
        print('clicked')
        # Confirm the removal in the popup dialog
        remove_confirm = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="content" and text()="Remove"]')))
        remove_confirm.click()

def read_csv(file_path):
    mobile_numbers = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            mobile_number = row[30]
            mobile_numbers.append(mobile_number)
    return mobile_numbers

start_time = datetime.now()

csv_file_path = 'numbers.csv'

# Sample list of numbers
user_names = read_csv(csv_file_path)

    
chat_name = 'Your Whatsapp Group Name'
el_search.clear()
el_search.send_keys(chat_name)

try:
    remove_from_group(user_names, chat_name)
    
except Exception as exception:
    print("Exception: {}".format(type(exception).__name__))
    print("Exception message: {}".format(exception))
    
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))