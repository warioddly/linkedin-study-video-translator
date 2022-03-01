
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, InvalidSelectorException, NoSuchElementException
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
from wget import download
from requests import get
from subprocess import call
import threading, random, termcolor

class MyCaption:
    def __init__(self):
        # link = 'https://www.linkedin.com/learning/learning-vue-js-8602681/what-you-should-know?autoAdvance=true&autoSkip=false&autoplay=true&contextUrn=urn%3Ali%3AlyndaLearningPath%3A5d94ce0a498e93731fbb8711&resume=false'
        link = input("Input link: ")
        self.__url = 'https://www.sslproxies.org/'
        self.__headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
            }
        self.random_ip = []
        self.random_port = []
        opt = Options()
        opt.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver=webdriver.Chrome(executable_path="inlcudes\chromedriver.exe", chrome_options=opt)
        self.driver.get(link)
        self.getCaptions()
    
    def getRandom_proxy(self):
        r = get(url=self.__url, headers=self.__headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        for x in soup.findAll('td')[::8]:
            self.random_ip.append(x.get_text())

        for y in soup.findAll('td')[1::8]:
            self.random_port.append(y.get_text())

        z = list(zip(self.random_ip, self.random_port))

        number = random.randint(0, len(z)-50)
        ip_random = z[number]

        ip_random_string = "{}:{}".format(ip_random[0],ip_random[1])
        proxy = {'https':ip_random_string}

        return proxy

    def getCaptions(self):
        old_caption = 'i am subParser'; captionTime = '00:00'; old_time = '1:00'
        captionWriteTime = []; captions = []
        i = 0; amountProxy = 0; proxy = ''; flag = False
        while True:    
            if amountProxy >= 70:
                proxy = self.getRandom_proxy() 
                print(termcolor.colored('Прокси изменен на ' + str(proxy), 'red', attrs=['underline']) )
                amountProxy = 0
            try:
                caption = self.driver.find_element(By.XPATH, '//*[@id="vjs_video_3"]/div[5]/div/div/div').text
            except StaleElementReferenceException:
                try:
                    caption = self.driver.find_element(By.XPATH, '//3+*[@id="vjs_video_3"]/div[5]/div/div/div/font/font/').text
                except InvalidSelectorException:
                    continue
            except NoSuchElementException:
                try:
                    caption = self.driver.find_element(By.XPATH, '//3+*[@id="vjs_video_3"]/div[5]/div/div/div/font/font/').text
                except InvalidSelectorException:
                    continue

            if False == self.CheckWord(caption):
                continue
            
            menuUnhide = self.driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div/div/section/section[2]/div[1]')
            self.driver.execute_script("arguments[0].setAttribute('class', 'classroom-layout__stage classroom-layout__stage--large')", menuUnhide)
            captionTime = self.driver.find_element_by_xpath('//*[@id="vjs_video_3"]/div[3]/div[3]/div[1]/span[2]').text 
            PlaybackProgress = str((self.driver.find_element(By.XPATH, '//*[@id="vjs_video_3"]/div[3]/div[1]/div').get_attribute("aria-valuenow"))) 

            if flag == False:    
                proxy = self.getRandom_proxy()
                try:
                    video = str(self.driver.find_element(By.XPATH, '//*[@id="ember38"]/div/div[1]').text)
                except Exception:
                    try:
                        video = str(self.driver.find_element(By.XPATH, '//*[@id="ember53"]/div/div[1]/font/font').text)
                    except Exception:
                        video = str(self.driver.find_element(By.XPATH, '//*[@id="vjs_video_3"]/div[5]/div/div/div/font/font').text)

                video = video.replace("\n(Просмотрено)", "")
                self.nameVideo = str(video.translate({ord(i): None for i in '?%;!*(),.'}))
                self.nameVideoKg = GoogleTranslator(source='ru', target='ky').translate(video)
                self.nameVideoKg = str(self.nameVideoKg.translate({ord(i): None for i in '?%;!*(),.'}))
                self.driver.execute_script("arguments[0].setAttribute('class', 'classroom-layout__stage classroom-layout__stage--large')", menuUnhide)
                captionTimeEnd = self.driver.find_element_by_xpath('//*[@id="vjs_video_3"]/div[3]/div[3]/div[3]/span[2]').text 
                tempTimeEnd = int(captionTimeEnd[-1])
                tempTimeEnd -= 2
                
                l = len(captionTimeEnd)
                captionTimeEndTemp = captionTimeEnd[:l-1]
                captionTimeEndTemp += str(tempTimeEnd)
                call("cls", shell=True)
                print(termcolor.colored("\n  =============== Данные о видео ===============\n", 'green'))
                print(termcolor.colored(video + "\t\n" + GoogleTranslator(source='ru', target='ky').translate(video) + " \t\t" + captionTimeEnd, 'cyan') )
                print(termcolor.colored("\n=============== Программа запущена ===============\n", 'green'))
                flag = True

            if old_caption != caption:
                if old_time != captionTime:
                    old_time = captionTime
                    captionWriteTime.append(captionTime)

                translation = GoogleTranslator(source='ru', target='ky').translate(caption)
                print("Время: " + termcolor.colored(captionTime, 'green' , attrs=['underline']) + "\tПрокси: " + termcolor.colored(str(proxy), 'green', attrs=['underline']) + "\tПрогресс: " + termcolor.colored(PlaybackProgress + "%", 'green' , attrs=['underline']))
                print("\n-" + caption + "\n-" + translation + "\n\n")

                captions.append(caption)
                captions.append(translation)
                old_caption = caption 

            if (PlaybackProgress >= '95.90' or captionTimeEndTemp <= captionTime):
                self.ExportsCaption(captions, captionWriteTime, captionTimeEnd)
                self.VideoDownload()
                th = threading.Thread(target=self.EmbeddingSubtitle, args=('kg', self.nameVideo, self.nameVideoKg, self.nameVideoKg))
                th.start()
                self.EmbeddingSubtitle("ru", self.nameVideo, self.nameVideo, self.nameVideo)
                th.join()
                print(termcolor.colored("=============== Выход из программы ===============", 'green'))
                break

            i += 1
            amountProxy += 1
        
    def VideoDownload(self):
        url = self.driver.find_element(By.XPATH, '//*[@id="vjs_video_3_html5_api"]').get_attribute("src")
        #urllib.request.urlretrieve(url, "Files/" + self.nameVideo + ".mp4") 
        download(url,  "Files/" + self.nameVideo + ".mp4")

    def CheckWord(self, s):
        lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        return lower.intersection(s.lower()) != set()

    def ExportsCaption(self, caption, captionTime, captionTimeEnd):
        i = 0; j = 0; k = 1
        f_ru = open("Files/" + self.nameVideo + "_ru.srt", "a", encoding="utf-8")
        f_kg = open("Files/" + self.nameVideoKg + "_kg.srt", "a", encoding="utf-8")

        while i < len(caption):
            f_ru.write(str(k) + '\n')
            f_kg.write(str(k) + '\n')
            while j < k:
                f_ru.write('00:0' + captionTime[j] + ",100" + " --> ")
                f_kg.write('00:0' + captionTime[j] + ",100" + " --> ")
                j += 1
                try:
                    f_ru.write('00:0' +captionTime[j] + ",100")
                    f_kg.write('00:0' +captionTime[j] + ",100")
                except Exception:
                    f_ru.write('00:0' + captionTimeEnd + ",000")
                    f_kg.write('00:0' + captionTimeEnd + ",000")
            f_ru.write('\n' + caption[i] + '\n\n\n')
            i += 1
            f_kg.write('\n' + caption[i] + '\n\n\n')
            i += 1
            k += 1
        f_ru.close()
        f_kg.close()

    def EmbeddingSubtitle(self, language, nameVideo, subtitle, nameOutputVideo):
        args = "inlcudes/ffmpeg.exe -i" +  ' "Files/' + nameVideo + '.mp4"'  + ' -vf ' + '"subtitles=' + 'Files/' + subtitle + '_' + language + '.srt:force_style=' + "'OutlineColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=17'" + '"' + ' "Files/' + nameOutputVideo + "_" + language + '_sub.mp4"'
        print(args)
        call(args, shell=False)

MyCaption()

