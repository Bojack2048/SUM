
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
import time, json, random, os,sys

#设置全局变量
def __init__():
    global options, driver

    # 指定位置驱动
    path = os.getcwd()
    driver_path = path + r"\msedgedriver.exe"

    options = EdgeOptions()
    options.use_chromium = True
        #options.headless = True
    driver = Edge(driver_path,options = options)


# 更换请求头
def head():
    list_header = ['Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.1 (KHTML, like Gecko)', 'Mozilla/5.0 (Windows NT 6.1; WOW64)\
     AppleWebKit/536.11 (KHTML, like Gecko)', 'Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11','Mozilla/5.0\
      (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0', 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
      AppleWebKit/537.36 (KHTML, like Gecko)', 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
      AppleWebKit/537.36 (KHTML, like Gecko)'
    ]

    options.add_argument('user-agent=%s'%list_header[random.randint(0,len(list_header) - 1)])

# 登录筹备
def write_cookie():
    input("请先扫码登录，登录完成按回车键！")

    with open('cookies.txt', 'w') as file:
        #保存 cookie为 json格式
        file.write(json.dumps(driver.get_cookies()))

    print("cookie写入完成！")

def check_cookie():
    print("正在检测登录状态...")

    try:
        driver.find_element_by_xpath("/html/body/div/div/div[1]/header/div[2]/div[2]/span/a")
    except:
        login()

def login():
    driver.find_element_by_xpath("/html/body/div/div/div[1]/header/div[2]/div[2]/a[2]").click()
    write_cookie()

    #句柄切换到最新页面
    driver.implicitly_wait(60)
    driver.switch_to_window(driver.window_handles[-1])
    driver.implicitly_wait(60)

#浏览器启动
def driver_launch():
    #初始化
    __init__()
    #请求头
    head()

    # 进入学习强国首页
    driver.get("https://www.xuexi.cn")
    driver.delete_all_cookies()
    driver.implicitly_wait(60)

    try:
        with open('cookies.txt', 'r') as file:
            #使用json读取cookies  读取的是文件而不是数据 用 load
            cookies_list = json.load(file)
            for cookie in cookies_list:
                if 'expiry' in cookie:
                    del cookie['expiry']

                driver.add_cookie(cookie)

    except FileNotFoundError:
        login()

    driver.implicitly_wait(60)
    driver.get("https://www.xuexi.cn")
    driver.implicitly_wait(60)

    # 检查cookie
    driver.implicitly_wait(60)
    check_cookie()
    driver.implicitly_wait(60)

# MENU
def READING12():
    MENU = ['强军兴军', '习近平文汇', '环球视野']
    x = random.randint(0,2)

    driver.implicitly_wait(60)
    time.sleep(2)
    Go_reading_button = driver.find_element_by_link_text(f"{MENU[x]}")
    Go_reading_button.click()
    driver.implicitly_wait(60)

    #句柄切换到最新页面
    driver.switch_to_window(driver.window_handles[-1])
    driver.implicitly_wait(60)
    time.sleep(2)

    #句柄切换到最新页面
    if x == 0 :
        Strong_army()
    elif x == 1:
        XI()
    else:
        GLOBAL()

def READING12_PLUS():
    NEWS()


def Strong_army():
    #XPATH文章设置
    default_articl1 = "/html/body/div/div/div[2]/section/div/div/div/div/div[1]/section/div/div/div/div/div/section[3]/div/div/div/div/div[2]/section/div/div/div/div[1]/div/section/div/div/div/div/div/section/div/div/div/div/div[2]/section/div/div/div/div["
    default_articl2 =  "]/div[1]/div/div/div[2]/span"
    article_list = [default_articl1 + str(file) + default_articl2 for file in range(1,7)]

    n = 0
    for article in article_list:

        n += 1
        num = random.randint(60,100)

        driver.find_element_by_xpath(article).click()
        driver.implicitly_wait(10)
        driver.switch_to_window(driver.window_handles[-1])
        driver.implicitly_wait(20)

        #滚动页面
        time.sleep(2)
        js = 'var q=document.body.scrollTop=50000'
        driver.execute_script(js)
        driver.implicitly_wait(10)

        print(f"正在读第{n}篇文章，预计{num}秒后结束.")
        time.sleep(num)

        # 标签退出
        driver.close()
        driver.implicitly_wait(10)
        driver.switch_to_window(driver.window_handles[-1]) # 强军兴军

def GLOBAL(): # 环球视野
    #article_global = driver.find_elements_by_xpath("//span[@class=\"text\"]")
    article_global =  driver.find_elements_by_class_name("text")

    n = 0
    for article in article_global[0:6]:
        #等待页面元素加载
        time.sleep(1)

        # 滚动至该元素
        driver.execute_script("arguments[0].scrollIntoView();",article)

        # 阅读区
        n += 1
        num = random.randint(60,100)

        article.click()
        driver.implicitly_wait(60)
        driver.switch_to_window(driver.window_handles[-1])
        driver.implicitly_wait(60)

        #滚动页面
        time.sleep(2)
        js = 'document.documentElement.scrollTop=10000'
        #document.documentElement.scrollTop=10000
        driver.execute_script(js)
        driver.implicitly_wait(60)

        #阅读等待
        print(f"正在读第{n}篇文章，预计{num}秒后结束.")
        time.sleep(num)

        # 标签退出
        driver.close()
        driver.implicitly_wait(60)
        driver.switch_to_window(driver.window_handles[-1])
        driver.implicitly_wait(60)

def XI(): # 习近平文汇
    #指定文章
    x = random.randint(0,10)
    #一级目录
    driver.implicitly_wait(60)
    article_list = driver.find_elements_by_xpath("//span[@class=\"text\"]")

    # 页面点击
    article_list[x].click()
    driver.implicitly_wait(60)
    driver.switch_to_window(driver.window_handles[-1])
    driver.implicitly_wait(60)

    # 二级目录
    article_list2 = driver.find_elements_by_xpath("//span[@class=\"text\"]")

    n = 0
    for article2 in article_list2[0:6]:
        n += 1
        num = random.randint(60,100)

        article2.click()
        driver.implicitly_wait(60)
        driver.switch_to_window(driver.window_handles[-1])
        driver.implicitly_wait(60)

        #滚动页面
        time.sleep(2)
        js = 'document.documentElement.scrollTop=10000'
        driver.execute_script(js)
        driver.implicitly_wait(60)

        #阅读等待
        print(f"正在读第{n}篇文章，预计{num}秒后结束.")
        time.sleep(num)

        # 标签退出
        driver.close()
        driver.implicitly_wait(10)
        driver.switch_to_window(driver.window_handles[-1])
        driver.implicitly_wait(10)

def NEWS(): # 新闻阅读
    driver.implicitly_wait(10)
    new_button = driver.find_element_by_xpath("/html/body/div/div/div[2]/section/div/div/div/div/div[1]/section/div/div/div/div/div/section[12]/div/div/div/div[1]/div/section/div/div/div/div/div/section/div/div/div/div/div[1]/div/div/div[1]/span")

    # 滚动至该元素
    driver.execute_script("arguments[0].scrollIntoView();",new_button)
    driver.implicitly_wait(10)

    # 点击按钮
    new_button.click()

    #二级界面文章阅读
    driver.implicitly_wait(60)
    driver.switch_to_window(driver.window_handles[-1])
    driver.implicitly_wait(60)

    article_new =  driver.find_elements_by_class_name("text-wrap")

    n = 0
    for article in article_new[0:6]:
        #等待页面元素加载
        time.sleep(1)

        # 滚动至该元素
        driver.execute_script("arguments[0].scrollIntoView();",article)

        # 阅读区
        n += 1
        num = random.randint(60,100)

        # 进入文章页面
        article.click()
        driver.implicitly_wait(60)
        driver.switch_to_window(driver.window_handles[-1])
        driver.implicitly_wait(60)

        #滚动页面
        time.sleep(2)
        js = 'document.documentElement.scrollTop=10000'
        #document.documentElement.scrollTop=10000
        driver.execute_script(js)
        driver.implicitly_wait(60)

        #阅读等待
        print(f"正在读第{n}篇文章，预计{num}秒后结束.")
        time.sleep(num)

        # 标签退出
        driver.close()
        driver.implicitly_wait(60)
        driver.switch_to_window(driver.window_handles[-1])
        driver.implicitly_wait(60)


#看视频
def WATCHING12():
    # 进入学习电视台
    driver.implicitly_wait(60)
    time.sleep(2)
    Strong_army_button = driver.find_element_by_xpath("/html/body/div/div/div[1]/header/div[2]/div[1]/div[2]/a[2]")
    driver.implicitly_wait(60)

    Strong_army_button.click()
    driver.implicitly_wait(60)
    driver.switch_to_window(driver.window_handles[-1])
    driver.implicitly_wait(60)

    # 进入学习电视台内二级目录
    time.sleep(2)
    Strong_army_button2 = driver.find_elements_by_class_name("textWrapper")


    #抛出非观看频道
    Strong_army_button2.pop(3) # 抛出全国卫视联播
    Strong_army_button2.pop(-1)
    Strong_army_button2.pop(-2)
    Strong_army_button2.pop(-3)
    Strong_army_button2.pop(-4)


    Strong_army_button2[random.randint(0,2)].click()
    driver.implicitly_wait(60)
    driver.switch_to_window(driver.window_handles[-1])
    driver.implicitly_wait(60)

    # 选择要看的视频
    Vedio_Click()

def Vedio_Click():
    # 学习电视台内 列表
    vedio_list =  driver.find_elements_by_class_name("textWrapper")

    n = 0
    for vedio in vedio_list[0:6]:
        n += 1
        num = random.randint(60,100)

        vedio.click()
        driver.implicitly_wait(60)
        driver.switch_to_window(driver.window_handles[-1])
        driver.implicitly_wait(60)

        #滚动页面
        time.sleep(2)
        js = 'document.documentElement.scrollTop=5000'
        driver.execute_script(js)
        driver.implicitly_wait(60)

        #视频观看等待
        print(f"正在观看第{n}个视频，预计{num}秒后结束.")
        time.sleep(num)

        # 标签退出
        driver.close()
        driver.implicitly_wait(10)
        driver.switch_to_window(driver.window_handles[-1])
        driver.implicitly_wait(10)

def mouseClick_Vedio():
    driver.implicitly_wait(60)
    time.sleep(1)
    WATCHING12()
    print("视频观看完毕!")

def mouseClick_article():
    X = random.randint(0,1)

    if X == 0:
        READING12()
    else:
        READING12_PLUS()

    print("阅读完毕!")

# 功能区：视频、阅读

def RV():
    driver_launch()
    print("开始阅读自强！")
    mouseClick_article()

def VV():
    driver_launch()
    print("开始视频自强！")
    mouseClick_Vedio()


# 操作面板区域
message = input("1.看视频   2.看文章   3.看视频＋文章\n -->> ")

if message == '1':
    VV()
    driver.implicitly_wait(60)
    driver.quit()
    print("自强全部结束，请首长放心(^^ゞ！（3秒后自动退出）")
    time.sleep(3)

elif message == '2':
    RV()
    driver.implicitly_wait(60)
    driver.quit()
    print("自强全部结束，请首长放心(^^ゞ！（3秒后自动退出）")
    time.sleep(3)
else:
    # 视频
    VV()
    driver.implicitly_wait(60)
    driver.quit()

    time.sleep(2)
    # 阅读
    RV()
    driver.implicitly_wait(60)
    driver.quit()

    print("自强全部结束，请首长放心(^^ゞ！（3秒后自动退出）")
    time.sleep(3)
