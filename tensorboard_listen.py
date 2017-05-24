from selenium import webdriver
from PIL import Image
import time
from cStringIO import StringIO

binary = './chromedriver'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(binary, chrome_options=options)
driver.get('http://127.0.1.1:6006/')

def open_and_init_driver():
    time.sleep(1)

    scalars_n = 1
    while(1):
        try:
            dash = driver.find_element_by_xpath('//*[@id="center"]/div/tf-panes-helper/tf-collapsable-pane[' + str(scalars_n) + ']/button')
            dash.click()
        except:
            break
        scalars_n += 1
    scalars_n -= 1

    time.sleep(0.5)

    for i in range(1, scalars_n+1):
        dash = driver.find_element_by_xpath('//*[@id="center"]/div/tf-panes-helper/tf-collapsable-pane[' + str(i) +']/iron-collapse/div/div/div/div[3]/paper-icon-button')
        dash.click()
    
    time.sleep(0.5)

    driver.find_element_by_xpath('//*[@id="center"]/div/tf-panes-helper/tf-collapsable-pane[1]/iron-collapse').click()
    time.sleep(0.5)

    driver.execute_script("window.scrollTo(0, %s);" % -987654321)
    time.sleep(0.5)

def save_screenshot():
    slices = []
    driver.save_screenshot("screenshot1.png")
    img = Image.open(StringIO(driver.get_screenshot_as_png()))
    first_scalar_location = driver.find_element_by_xpath('//*[@id="center"]/div/tf-panes-helper/tf-collapsable-pane[1]/iron-collapse/div/div').location
    first_scalar_size = driver.find_element_by_xpath('//*[@id="center"]/div/tf-panes-helper/tf-collapsable-pane[1]/iron-collapse/div/div').size
    img = img.crop((int(first_scalar_location['x']), int(first_scalar_location['y']), int(first_scalar_location['x'] + first_scalar_size['width']), int(first_scalar_location['y'] + first_scalar_size['height'])))
    slices.append(img)

    block_y_size = driver.find_element_by_xpath('//*[@id="center"]/div/tf-panes-helper/tf-collapsable-pane[1]').size['height']
    for i in range(2, scalars_n+1):
        driver.find_element_by_xpath('//*[@id="center"]/div/tf-panes-helper/tf-collapsable-pane[' + str(i) + ']/iron-collapse').click()
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, %s);" % (block_y_size))
        time.sleep(0.5)
        driver.save_screenshot("screenshot" + str(i) + ".png")
        img = Image.open(StringIO(driver.get_screenshot_as_png()))
        scalar_location = driver.find_element_by_xpath('//*[@id="center"]/div/tf-panes-helper/tf-collapsable-pane[' + str(i) + ']/iron-collapse/div/div').location
        scalar_size = driver.find_element_by_xpath('//*[@id="center"]/div/tf-panes-helper/tf-collapsable-pane[' + str(i) + ']/iron-collapse/div/div').size
        img = img.crop((int(scalar_location['x']), int(scalar_location['y']), int(scalar_location['x'] + scalar_size['width']), int(scalar_location['y'] + scalar_size['height'])))
        slices.append(img)

    for i in range(0, scalars_n):
        slices[i].save('./' + str(i) + '.png')

def merge_screenshot(slices):
    first_size = driver.find_element_by_xpath('//*[@id="center"]/div/tf-panes-helper/tf-collapsable-pane[1]/iron-collapse/div/div').size

    screenshot = Image.new('RGB', (first_size['width'], scalars_n*first_size['height']))
    offset = 0
    for img in slices:
        screenshot.paste(img, (0, int(offset)))
        offset += img.size[1]

    screenshot.save('./test.png')
