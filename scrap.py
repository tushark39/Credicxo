from selenium import webdriver
from selenium.webdriver.common.by import By  
from selenium.common.exceptions import NoSuchElementException
jsonData = {}

# Function to scrap data from the URL
def scrap(assin,con):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    browser = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
    
    # Opening the URL with given Country Code and Asin number
    browser.get('https://www.amazon.'+con+'/dp/'+assin)
    
    # Flushing the value of variables
    productName = None
    productImageURL = None
    productPrice = None
    productDetails = None
    
    # Fnd Prodict Name
    try:
        productName = browser.find_element(By.ID,'productTitle').text  # Check if Product is available with given country and asin code
    except:
        # If product is not available then Append the link of Error URL and return
        file1 = open("failedLinks.txt", "a") 
        file1.write('https://www.amazon.'+con+'/dp/'+str(assin)+"\n")
        file1.close()
        browser.close()
        print("[*] Link Down")
        return
    
    # Find URL of Image 
    try:
        productImageURL = browser.find_element(By.ID,'imgBlkFront').get_attribute('src') # Check URL in first possible ID
    except NoSuchElementException:
        productImageURL = browser.find_element(By.ID,'landingImage').get_attribute('src') # Check URL in second possible ID
    except:
        productImageURL = None # If Product Image is missing

    # Find Price of Product
    try:
        productPrice = browser.find_element(By.ID,'price').text         # Check Price in first possible ID
    except NoSuchElementException:
        try:
            # Check Price in possible Path
            productPrice = browser.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[3]/div[1]/div[7]/div[14]/div[2]/div[2]/ul/li/span/span[1]/span/a/span[2]/span').text
        except NoSuchElementException:
            productPrice = None # If Product Price is missing

    # Find Product Details
    try:
         # Check Product Details in first possible PATH
        productDetails = browser.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[3]/div[22]/div/div[1]').text   
    except NoSuchElementException:
        try:
             # Check Product Details in second possible PATH
            productDetails = browser.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[5]/div[17]/div/div/div[2]').text
        except NoSuchElementException:
            try:
                 # Check Product Details in third possible PATH
                productDetails = browser.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[4]/div[23]/div/div[1]').text
            except NoSuchElementException:
                 # Check Product Details in fourth possible PATH
                productDetails = browser.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[4]/div[22]/div/div[1]').text
            except:
                productDetails = None   # If Product Details is missing

    # Appending the scrapped details to dict
    jsonData['https://www.amazon.'+con+'/dp/'+assin] = {
                                                        'Product Title':productName,
                                                        'Product Image URL':productImageURL,
                                                        'Price of the Product' : productPrice,
                                                        'Product Details' : productDetails
                                                        }

    # Closing the browser 
    browser.close()
    