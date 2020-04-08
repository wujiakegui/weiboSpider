from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

class WeiboLogin():
    def __init__(self, username="0331_ee6ebc@163.com", password="cua633476"):
        self.url = "https://passport.weibo.cn/signin/login"
        # self.browser = webdriver.PhantomJS(executable_path=r"D:\迅雷下载\phantomjs-2.1.1-windows\bin\phantomjs.exe")    # 可编程的无头浏览器
        self.option = Options()
        self.option.add_argument("--headless")
        self.option.add_argument("--disable-gpu")
        self.browser = webdriver.Firefox()
        self.browser.set_window_size(1050,840)
        self.wait = WebDriverWait(self.browser,20)
        self.username = username
        self.password = password
        self.uids = ['1743951792']  # 美国大使馆的uid
        self.ids = ['usembassy'] # 美国驻华大使馆的id

        self.id_url = 'http://weibo.cn/'
        print("初始化完成")

    def open(self):
        '''
        打开网页输入用户名密码并点击
        :return:
        '''
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID,'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID,'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID,'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()
    def getCookies(self):
        '''
        破解入口
        :return:
        '''
        self.open()

        try:
            WebDriverWait(self.browser,30).until(
                EC.presence_of_element_located((By.CLASS_NAME,"geetest_radar_tip"))
            )
            print('当前页面的url', self.browser.current_url)
            f_test = self.browser.find_element_by_id('message-p')
            print("f_test", f_test.text)
            check_input = self.browser.find_element_by_class_name('geetest_radar_tip')
            check_input.click() # 点击
            print("按钮点击验证完成")
        except Exception as e:
            print("验证失败")
            print(e)

        try:
            WebDriverWait(self.browser,30).until(
                EC.title_is("微博")
            )

            cookies = self.browser.get_cookies()
            print(cookies)
            cookie = [item["name"] + "=" + item["value"] for item in cookies]
            cookie_str = '; '.join(item for item in cookie)
            # self.browser.quit()
        except Exception as e:
            print("获取cooie失败")
            print(e)
        return cookie_str

    def getUserInfoAndWeibo(self):
        for id in self.ids:
            id_url = self.id_url+id
            print(id_url)
            self.browser.get(id_url)
            try:
                WebDriverWait(self.browser,3).until(
                    EC.title_is("美国驻华大使馆的微博")
                )
                # 使用BeautifulSoup解析网页的HTML
                soup = BeautifulSoup(self.browser.page_source,'lxml')
                # 爬取最大页码数目
                pageSize = soup.find('div', attrs={'id': 'pagelist'})
                pageSize = pageSize.find('div').getText()
                pageSize = (pageSize.split('/')[1]).split('页')[0]

                # 爬取微博数量
                divMessage = soup.find('div', attrs={'class': 'tip2'})
                weiBoCount = divMessage.find('span').getText()
                weiBoCount = (weiBoCount.split('[')[1]).replace(']', '')
                # 爬取微博数量
                divMessage = soup.find('div', attrs={'class': 'tip2'})
                weiBoCount = divMessage.find('span').getText()
                weiBoCount = (weiBoCount.split('[')[1]).replace(']', '')
                # 爬取关注数量和粉丝数量
                a = divMessage.find_all('a')[:2]
                guanZhuCount = (a[0].getText().split('[')[1]).replace(']', '')
                fenSiCount = (a[1].getText().split('[')[1]).replace(']', '')
                print("最大页码 {} 微博数量 {} 粉丝数量 {} 关注数量 {}".format(pageSize,weiBoCount, fenSiCount, guanZhuCount))

            except Exception as e:
                print("抓取id为：{} 的信息失败".format(id))

if __name__ == '__main__':
    # try:
    loginer = WeiboLogin()
    cookie_str = loginer.getCookies()
    # print('获取cookie成功')
    # print('Cookie:', cookie_str)
    loginer.getUserInfoAndWeibo()