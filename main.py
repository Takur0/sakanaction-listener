import urllib3
from bs4 import BeautifulSoup
from datetime import datetime
import setup_mail
import smtplib
from email.mime.text import MIMEText
import html5lib


# アクセスするURL
url = "https://ticket-trade.emtg.jp/artists/sakanaction/tickets"

# URLにアクセスする htmlが帰ってくる → <html><head><title>hogehoge</title></head><body....
http = urllib3.PoolManager()

html = http.request('GET', url)

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(html.data, "html5lib")

# print(soup)

p = soup.find_all("p")

# print時のエラーとならないように最初に宣言しておきます。
isAvailable = ""

for tag in p:
# classの設定がされていない要素は、tag.get("id")を行うことのできないでエラーとなるため、tryでエラーを回避する
    try:
        # tagの中からclass="n"のnの文字列を摘出します。複数classが設定されている場合があるので
        # get関数では配列で帰ってくる。そのため配列の関数pop(0)により、配列の一番最初を摘出する
        # <span class="hoge" class="foo">  →   ["hoge","foo"]  →   hoge
        string_ = tag.get("class")
        # 摘出したclassの文字列にbtc_jpy_top_bidと設定されているかを調べます
        for string in string_:
            if string in "venue":
                # btc_jpy_top_bidが設定されているのでtagで囲まれた文字列を.stringであぶり出します
                venue = tag.string
                # 摘出が完了したのでfor分を抜けます
                # print(tag)
                if tag.contents[1] == "佐賀市文化会館【一般プレイガイド販売分】\n                                                                " or tag.contents[1] == "福岡サンパレス【一般プレイガイド販売分】\n                                                                ":
                # if True:
                    if list(tag.parent)[11].contents[0] != '\n\t\t\t\t\t\t\t出品待ち\n\t\t\t\t\t':
                        print(tag.contents[1].strip())
                        print(list(tag.parent)[11].contents[1].string)
                        try:
                            msg = MIMEText(tag.contents[1].strip() + "の" + list(tag.parent)[11].contents[1].string + "枚のチケットの売り出しがあります！\n詳しくは " + url + " まで")
                            msg['Subject'] = "サカナクションの新しいチケット情報です！"
                            msg['From'] = "yt1997kt@icloud.com"
                            msg['To'] = "yt1997kt@gmail.com"
                            #下記のパラメータは https://support.apple.com/ja-jp/HT202304 によった
                            s = smtplib.SMTP('smtp.mail.me.com',587)
                            s.ehlo()
                            s.starttls()
                            s.login(setup_mail.name,setup_mail.pw)
                            s.send_message(msg)
                            s.quit()
                        except:
                            print("MailError")

                        # print("<p class=\"count\">\n\t\t\t\t\t\t\t出品待ち\n\t\t\t\t\t</p>")
                        break
    except:
        # パス→何も処理を行わない
        pass



