import requests # http requests

from bs4 import BeautifulSoup # web scraping
# De email verzenden
import smtplib
# Email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Systeem datum en tijd
import datetime

now = datetime.datetime.now()

# Email content placeholder

content = ''


#Uitpakken van Hacker News Stories


def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt +=('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content,'html.parser')
    for i,tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1)+' :: '+ '<a href="' + tag.a.get('href') + '">' + tag.text + '</a>' + "\n" + '<br>') if tag.text!='More' else '')
        #print(tag.prettify) #find_all('span',attrs={'class':'sitestr'}))
    return(cnt)
    
cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content +=('<br><br>End of Message')


#De email word hier verzonden

print('Composing Email...')


SERVER = 'smtp.gmail.com' # "jouw smtp server"
PORT = 587 # jouw port number
FROM =  'automatedpythontutorial@gmail.com' # "Jouw email id"
TO = 'automatedpythontutorial@gmail.com' # "Nogmaals jouw email id"  # (Kan ook een lijst zijn)
PASS = 'Python123!' # "Het wachtwoord van jouw email id"

# fp = open(file_name, 'rb')
# Een leeg bericht creeëren
# msg = MIMEText('')
msg = MIMEMultipart()

# msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(
    now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
# fp.close()

print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
#server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
#server.ehlo
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()






