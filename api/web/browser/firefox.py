from selenium.webdriver import Firefox, FirefoxOptions

# Set up the driver in headless mode
options = FirefoxOptions()
options.add_argument("--headless")

# Create a new instance of the Firefox driver
firefox = Firefox(options=options)
