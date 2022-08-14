from selenium import webdriver
import time
import shutil

def collect_data():
    print("[!] Starting Webdriver..")
    driver = webdriver.Edge(executable_path=r'C:\Users\banna\Downloads\edgedriver_win64\msedgedriver.exe')
    url = "https://public.tableau.com/views/SATCOVIDDashboard/1-dash-tiles?:embed=y&:showVizHome=no&:host_url=https%3A%2F%2Fpublic.tableau.com%2F&:embed_code_version=3&:tabs=no&:toolbar=no&:isGuestRedirectFromVizportal=y&:display_spinner=no&:loadOrderID=0"
    print("[!] Collecting New Data..")
    driver.get(url)
    time.sleep(10)
    driver.find_element_by_xpath("//div[@class='tabToolbarButton tab-widget download']").click()
    time.sleep(2)
    driver.find_element_by_xpath("//button[@data-tb-test-id='DownloadImage-Button']").click()
    time.sleep(10)
    driver.close()
    driver.quit()
    print("[!] Collect Data Complete!")
    path = "C:\\/path/\\Downloads\\1-dash-tiles.png" #/path/ mean your directory download folder from selenium browser
    destination = "D:\\/path/\\covid.png" #/path/ mean your program directory 
    shutil.move(path, destination)
    print(("[!] Move Data To Directory!"))
    return
