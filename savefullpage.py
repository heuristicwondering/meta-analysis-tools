import math

def save_fullpage_screenshot(driver, output_path):
    """
    Scroll down a page taking screen shots.
    """

    # get dimensions
    window_height = driver.execute_script('return window.innerHeight')
    scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    num = int(math.ceil(float(scroll_height) / float(window_height)))

    # take screen shots
    for i in range(num):
        if i > 0:
            driver.execute_script('window.scrollBy(%d,%d)' % (0, window_height))
        driver.save_screenshot(output_path + '/screenshot-' + str(i) + '.png')

    return output_path