from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import pandas as pd
import argparse 
import datetime
import time

# in order to scrape StubHub we need to do the following tasks
# 1. enter the event name into the search bar
# 2. pick the search result that is correct
# 3. parse each entry for its price, quantity, ticket type ("section")
# 4. compare to the data that was present before and show the diffs

def argument_parse():
	arg_parser = argparse.ArgumentParser()
	# input link
	arg_parser.add_argument("-l", "--link", default="https://www.google.com/", help="Specify link to jump to")
	# weblink page identifier - used to name the output .csv
	arg_parser.add_argument("-p", "--page", default="Scrape", help="Unique name used to identify the output data file")
	# run in "headless" mode, meaning the browser gui won't appear
	arg_parser.add_argument("-hl", "--headless", action="store_true", help="Run in \"headless\" mode, meaning the browser gui won't appear")
	args = arg_parser.parse_args()
	return args

# read args
args = argument_parse()

# options to pass to the chrome driver
chrome_options = Options()
if args.headless:
	chrome_options.add_argument("--headless")

# initialize driver
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)
driver.wait = WebDriverWait(driver, 5)
driver.get(args.link)

# Scrolling to 5 * i th elements for every 1 second -- to display them all
# before we can use jQuery in js we have to include its library
#driver.execute_script("import * from \"https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js\"")
#jquery_script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js';
#driver.execute_script("""var jquery_script = document.createElement('script'); 
#jquery_script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js';
#document.getElementsByTagName('head')[0].appendChild(jquery_script);""")

time.sleep(0.5) # time to load jQuery library
driver.execute_script('$ = window.jQuery;')

# all tickets are now shown in #div by the above scrolling, let's get all statistics
ticket_section_elems   = driver.find_elements_by_css_selector(".SectionRowSeat__sectionTitle")
ticket_row_elems     = driver.find_elements_by_css_selector(".rowcell")
ticket_price_elems = driver.find_elements_by_css_selector(".AdvisoryPriceDisplay__content")
ticket_num__elems    = driver.find_elements_by_css_selector(".RoyalTicketListPanel__SecondaryInfo")

# This transformation is heavy
price_list = []
for item in ticket_price_elems:
	if len(item.text):
		itemStr = item.text
		while( "\n" in itemStr ):
			itemStr = itemStr.replace("\n", " ")
		price_list.append(itemStr)
section_list = []
for item in ticket_section_elems:
	if len(item.text):
		itemStr = item.text
		while( "\n" in itemStr ):
			itemStr = itemStr.replace("\n", " ")
		section_list.append(itemStr)
ticket_num_list = []
for item in ticket_num__elems:
	if len(item.text):
		itemStr = item.text
		while( "\n" in itemStr ):
			itemStr = itemStr.replace("\n"," ")
		ticket_num_list.append(itemStr)
		
# Example 
[print(elem) for elem in price_list]
[print(elem) for elem in section_list]
[print(elem) for elem in ticket_num_list]

print(len(price_list))
print(len(section_list))
print(len(ticket_num_list))

mydf = pd.DataFrame(
    {'price':    price_list,
     'section':    section_list,
     'ticket_num': ticket_num_list
    })

print(mydf)
mydf.to_csv( path_or_buf= "Data/"+args.page+"_"+datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")+".csv", index=False)
driver.close()
