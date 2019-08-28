#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import sys
import yaml
reload(sys)
sys.setdefaultencoding('utf-8')
SLEEPSEC = 1

with open(unicode('config.txt'), 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

HOMEPAGE = cfg['system']['url'] + '/st_lec/lists/sn/' + cfg['system']['school']
RESULT = cfg['system']['url'] + '/st_app/lists/sn/' + cfg['system']['school']
def lectureURL(lectureCode):
    return cfg['system']['url'] + '/st_lec/view/num/' + lectureCode + '/p/1/sn/' + cfg['system']['school']

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
	
def login(driver):
    driver.find_element_by_xpath("//select[@name='login_stu_grade']").send_keys(cfg['user']['grade'])
    driver.find_element_by_xpath("//select[@name='login_stu_course']").send_keys(unicode(cfg['user']['course']))
    driver.find_element_by_xpath("//select[@name='login_stu_class']").send_keys(cfg['user']['class'])
    driver.find_element_by_xpath("//select[@name='login_stu_bunho']").send_keys(cfg['user']['bunho'])
    driver.find_element_by_xpath("//input[@name='login_stu_name']").send_keys(unicode(cfg['user']['name']))
    driver.find_element_by_xpath("//input[@name='login_stu_passwd']").send_keys(cfg['user']['password'])
    driver.find_element_by_xpath("//input[@class='login_user_grp2']").click()
    print unicode('[INFO] 로그인 되었습니다.')

def checkStatus(driver):
    driver.get(HOMEPAGE)
    if (check_exists_by_xpath("//*[@id=\"contents\"]/div[1]/div[2]/table/tbody/tr/td/strong/span")):
        return False 
    else:
        return True
		
def applyLecture(driver):
    for lecture in cfg['user']['lectures']:
        print unicode('[INFO] '+ lecture + '번 강좌를 신청 중 입니다.')
        driver.execute_script("return chk_sin('"+lecture+"');")
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(0.8)
        driver.get(HOMEPAGE)
    return True

def getResult(driver):
    driver.get(RESULT)
    lectures = driver.find_elements_by_xpath("//a[@class='link_type']")
    for lecture in lectures:
	    print (lecture.text)
    return True
		
if __name__ == "__main__":
    print unicode('[방과후학교 매크로]')
    print unicode('[INFO] Chrome을 실행 중 입니다.')
    print unicode('[INFO] 최대 10초 까지 걸릴 수 있습니다.')
    driver = webdriver.Chrome()
    driver.get(HOMEPAGE)
    login(driver)

    for lecture in cfg['user']['lectures']:
        driver.execute_script("window.open('" + lectureURL(lecture) + "');")

    driver.switch_to.window(driver.window_handles[0])
    
    print unicode('[INFO] 임시용으로 해당 강좌 세부정보 페이지를 실행 하였습니다.')
    print unicode('[INFO] 문제 발생시 직접 수강신청 해 주시기 바랍니다.')

    print unicode('[INFO] 상태확인을 시작합니다.')
    while(True):
        isOpened = checkStatus(driver)
        if (isOpened):
            print unicode('[INFO] 수강신청이 가능 합니다.')
            break
        else:
            print unicode('[INFO] 대기')
        time.sleep(SLEEPSEC)

    applyLecture(driver)
	
    print unicode('[INFO] 수강신청이 완료 되었습니다.')
    print unicode('[INFO] 신청 결과를 확인하시기 바랍니다.')
    
    getResult(driver)
	
    print unicode('[INFO] 20초 후에 자동으로 종료됩니다.')
    time.sleep(20)
    sys.exit(0)
