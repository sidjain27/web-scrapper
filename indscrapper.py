import scrapy
import mysql.connector
import random
import re
import datetime as dt
import datetime

postedOn = datetime.date.today()
expiredOn = datetime.date.today() + datetime.timedelta(1*365/12)
class IbmSpider(scrapy.Spider):
    name = "ibm"
    def start_requests(self):
        urls=['https://www.indeed.co.in/jobs?q=&l=Hyderabad']
        q=""
        page=2
        pages=50
        while(page<=pages):
            pagelink="https://www.indeed.co.in/jobs?q="+q+"&l=Hyderabad&start="+ str((page-1)*10)
            urls.append(pagelink)
            page += 1
        print("---------")
        [print(i,end="\n-------------\n") for i in urls]
        print("---------")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        link_cells = response.css('td.coloriginaljobtitle')
        job_links = []
        for link in link_cells:
            full_link = "https://careers.ibm.com" + link.css('a::attr(href)').extract_first()
            job_links.append(full_link)
        now = dt.datetime.now()
        todayDate = str(now.strftime("%Y-%m-%d"))
        for lnk in job_links:
            selectCursor = mydb.cursor(buffered=True)
            selectCursor.execute("SELECT * FROM scraper_urls WHERE url = '" + lnk + "'")
            if selectCursor.rowcount == 0:
                    insertCursor = mydb.cursor()
                    sql = "INSERT INTO scraper_urls (name, url) VALUES (%s, %s)"
                    val = ("ibm", lnk)
                    insertCursor.execute(sql, val)
                    mydb.commit()
            else:
                    mycursorUpdate= mydb.cursor()
                    sql = "UPDATE scraper_urls SET updated_date = '"+todayDate+"' WHERE url = '"+ lnk +"'"
                    mycursorUpdate.execute(sql)
                    mydb.commit()

            joblnk = lnk
            yield scrapy.Request(url=lnk, callback=self.job_detail, meta={'index':joblnk})

    def job_detail(self, response):
        jlink = response.meta['index']
        job_name = response.css('div.job-main h1::text').extract_first()
        job_description_raw = response.xpath('//*[@id="job-description"]').re('.+')
        job_des = "".join(job_description_raw)
        job_city = response.xpath('//*[@id="main-content"]/div[2]/aside/section/ul/li[3]/text()').extract_first()

        s = job_name.replace(" ", "-") + "-" + job_city.replace(" ", "-")
        sl = s.lower()
        slg = re.sub(r'\W+', '-', sl)
        seed = random.getrandbits(5)
        Slug = slg + "-" +str(seed)

        rht = re.sub('About IBM:', '', job_des)
        rhtag = re.sub('About IBM', '', rht)
        rhtags = re.sub('Job Description :', '', rhtag)
        rhtmltags = re.sub('Job Description:', '', rhtags)
        job_description= remove_html_tags(rhtmltags)

        try:
            selectCursor = mydb.cursor(buffered=True)
            selectCursor.execute("SELECT id FROM city_master WHERE LOWER(city_name) = LOWER('" + job_city + "')")
            record = selectCursor.fetchone()
            if selectCursor.rowcount == 0:

                insertCityCursor = mydb.cursor()
                sql = "INSERT INTO city_master (status, city_name) VALUES (%s, %s)"
                val = ('APPROVED',job_city)
                insertCityCursor.execute(sql, val)
                mydb.commit()

                insertCursor = mydb.cursor()
                sql = "INSERT INTO job_posting (job_title, job_description, location_hiring, company_id, link_job, posted_on, job_expired_on, slug,post$)"
                val = (job_name, job_description, insertCityCursor.lastrowid, 1, jlink, postedOn, expiredOn,Slug,1,176)
                insertCursor.execute(sql, val)
                mydb.commit()
            else:
                insertCursor = mydb.cursor()
                sql = "INSERT INTO job_posting (job_title, job_description, location_hiring, company_id, link_job, posted_on, job_expired_on, slug,post$)"
                val = (job_name, job_description, record[0], 1, jlink, postedOn, expiredOn,Slug,1,176)
                insertCursor.execute(sql, val)
                mydb.commit()
        except mysql.connector.Error as err:
            print("MySQL ERROR >>>>>>>>>>>>>>>>>")
            print(err)
            return None

spid=IbmSpider()
spid.start_requests()

def remove_html_tags(text):
    clean = re.compile('(?i)<(?!span|/span)(?!br).*?>')
    return re.sub(clean, '', text)