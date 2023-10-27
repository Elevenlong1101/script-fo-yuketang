# 雨课堂刷课脚本2.0 不同思路进行重构
# 学习：静音开启浏览器
# 学习：切换窗口
# 学习：根据文本定位
# 学习：文本输入
# 学习：要取相对路径不要自己写，直接复制就好了！！！驱动和浏览器路径写错selenium不会报错，只会找默认路径的驱动和浏览器！
# 学习：导包的时候要注意路径问题，写的是edge还是chrome
# 学习：在哪里运行这个文件也很重要，这关系到文件中需要读取的文件的相对路径能否被找到

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import time

# 事先声明

print("本脚本仅支持雨课堂平台\n")
print("牛魔雨课堂不得好死！！！\n")
name = input("请输入您想刷的课程名称:\n")
time.sleep(2)
print("接下来请在弹出的浏览器页面中扫码登陆,登陆后等待一段时间程序会自动开始运行\n")
print("想要退出刷课，只要退出浏览器窗口即可\n")
time.sleep(2)

# 隐藏爬虫机器人特征

option = webdriver.EdgeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
prefs = {'credentials_enable_service': False, 'profile.password_manager_enabled': False}
option.add_experimental_option('prefs', prefs)
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument('--mute-audio')
option.binary_location = 'selenium\edge117\msedge.exe'

# 浏览器实例

s = Service("selenium\msedgedriver117.exe")
driver = webdriver.Edge(service= s,options= option)
driver.get("https://xxxxx.yuketang.cn/web")

# 开始登陆

time.sleep(10)# 给时间扫码

# 找到课程

tab_student = driver.find_element(By.ID, 'tab-student')
tab_student.click()
time.sleep(1)
class_btn = driver.find_element(By.XPATH, f'//*[@id="pane-student"]//h1[contains(text(),{name})]')
class_btn.click()

time.sleep(1)
# 点击成绩单页面

grade = driver.find_element(By.XPATH, '//div[@id="tab-student_school_report"]/span')
grade.click()
time.sleep(1)
# 刷课

def study():
    lessons = driver.find_elements(By.XPATH, '//li[@class="study-unit"]')
    for lesson in lessons:
        statistic = lesson.find_element(By.CSS_SELECTOR, 'div.complete-td span').text
        if statistic == "已完成" or statistic == "已发言" or statistic == "未发言" or  statistic == "未开始":
            continue # 判断课程状态
        else:
            lesson_btn = lesson.find_element(By.CSS_SELECTOR, '.name-text')
            driver.execute_script("$(arguments[0]).click()", lesson_btn)# 点击进入课程按钮
            time.sleep(2)

            driver.switch_to.window(driver.window_handles[-1])# 切换到课程窗口

            #volume_btn = driver.find_element(By.XPATH, '//xt-icon')
            #driver.execute_script("$(arguments[0]).click()", volume_btn)# 静音播放

            finish_bar = driver.find_element(By.XPATH, '//span[@class="text"]').text
            while finish_bar != "完成度：100%":
                time.sleep(5)
                finish_bar = driver.find_element(By.XPATH, '//span[@class="text"]').text# 每五秒刷新状态值
                
            driver.close()
            driver.switch_to.window(driver.window_handles[0])# 关闭刷课窗口并回到成绩单窗口

            driver.refresh()# 刷新窗口获得课程完成状态
            time.sleep(1)
            
            grade = driver.find_element(By.XPATH, '//div[@id="tab-student_school_report"]/span')
            grade.click()
            time.sleep(1)# 点击转换到成绩单窗口

            study()

study()

time.sleep(5)