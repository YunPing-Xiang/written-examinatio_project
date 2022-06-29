import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class spider:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='spider')
        self.cur = self.conn.cursor()

    # mysql数据库连接
    def mysql_execute(self, sql):
        self.cur.execute(sql)
        data = self.cur.fetchall()
        self.cur.close()
        return data

    # 获取collection下所以的url，存贮到mysql的url_data表中
    def gt_url(self, index_url):
        url_list = []
        for i in range(7, 300):
            driver_path = Service('../Drivers/chromedriver.exe')
            driver = webdriver.Chrome(service=driver_path)
            driver.get(index_url)
            click_xpath = '//*[@id="main"]/div/div/div[5]/div/div[3]/div[3]/div[3]/div[3]/div[2]/div/div/div[' \
                          '{}]/div/article/a/div[2] '.format(i)
            driver.find_element(By.XPATH, click_xpath).click()
            driver.switch_to.window(driver.window_handles[1])
            url_list.append(driver.current_url)
            driver.quit()
        for j in url_list:
            insert_index_sql = 'insert into url_data(url) values ({})'.format(j)
            self.mysql_execute(sql=insert_index_sql)

    # 点击刷新按钮，将clicke或queued或erro 写入数据库的url_data表中
    def event(self):
        select_sql = 'select url from url_data'
        sql_data = self.mysql_execute(select_sql)
        for i in sql_data:
            url = i[0]
            # 点击刷新按钮
            driver_path = Service('../Drivers/chromedriver.exe')
            driver = webdriver.Chrome(service=driver_path)
            try:
                driver.get(url)
                driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/div[1]/div/div[1]/div[2]/section[1]/div/div['
                                              '2]/div/button[1]').click()
                # 更新mysql的url_data的status字段状态为clicked
                update_sql = 'update url_data set status = "clicked" where url = {}'.format(url)
                # 弹窗检测等待提示,更新数据库status字段
                if driver.find_element(By.XPATH,
                                       '/div/div/div[1]').get_attribute() == "We've queued this item for an update! Check back in a minute...":
                    update_sql = 'update url_data set status = "queued" where url = {}'.format(url)
                else:
                    pass
            except Exception as e:
                # 更新mysql的url_data的status字段状态为error
                update_sql = 'update url_data set status = "error" where url = {}'.format(url)
            self.mysql_execute(update_sql)


if __name__ == '__main__':
    create_sql = "create table url_data(" \
                 "id INT(11) NOT NULL AUTO_INCREMENT," \
                 "url VARCHAR(255) NOT NULL," \
                 "status VARCHAR(255) NULL," \
                 "PRIMARY KEY (`id`))ENGINE=InnoDB AUTO_INCREMENT 1 DEFAULT CHARSET=utf8; "

