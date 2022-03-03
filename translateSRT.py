
from fileinput import filename
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
from wget import download
from requests import get
from subprocess import call
import random, termcolor

class TransSRT():
    def __init__(self):
        print(termcolor.colored("\n  =============== Программа запущена ===============\n", 'green'))
        # filename = input("Введите название файла: ")
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
        self.TranslateFile(filename)
        
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

    def TranslateFile(self, filename):
        file = open("file.srt", "r", encoding="UTF-8")
        file_write = open("file_.srt", "a", encoding="UTF-8")
        amountProxy = 0
        proxy = self.getRandom_proxy()
        print(termcolor.colored('Прокси изменен на ' + str(proxy), 'red', attrs=['underline']) ) 
        while True:
            if amountProxy >= 20:
                proxy = self.getRandom_proxy()
                print(termcolor.colored('Прокси изменен на ' + str(proxy), 'red', attrs=['underline']) ) 
                amountProxy = 0
            line = file.readline()     
            if not line:
                    break
            print(line.strip())
            if False == self.CheckWord(line):
                file_write.write(line)
                continue
            translated = GoogleTranslator(source='en', target='ru').translate(line)
            print(translated)
            file_write.write(str(translated) + "\n" )

            amountProxy += 1
        file.close()
        file_write.close()

    def CheckWord(self, s):
        lower = set('abcdefghijklmnopqrstuvwxyz')
        return lower.intersection(s.lower()) != set()

TransSRT()