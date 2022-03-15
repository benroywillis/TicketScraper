from selenium import webdriver

# in order to scrape StubHub we need to do the following tasks
# 1. enter the event name into the search bar
# 2. pick the search result that is correct
# 3. parse each entry for its price, quantity, ticket type ("section")
# 4. compare to the data that was present before and show the diffs
