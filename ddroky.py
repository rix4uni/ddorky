import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import argparse

parser = argparse.ArgumentParser(description='DDROKY Dorks Hunter')
parser.add_argument('-d', '--domain', type=str, help='Domain to scan')
args = parser.parse_args()

if args.domain:
    domain = args.domain
else:
    print("Please provide a domain using the -d or --domain option.")
    exit()

num_pages = 3
results_per_page = 100

dorks = [
    f'site:{domain} ext:php',
    f'site:{domain} inurl:"phpinfo.php"',
    f'site:{domain} intitle:phpinfo "published by the PHP Group"',
    f'site:{domain} intitle:index.of',
    f'site:{domain} inurl:login | inurl:signin | intitle:Login | intitle:"sign in" | inurl:auth | inurl:signup | inurl:register | intitle:Signup"',
    f'site:{domain} ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup"',
    f'site:{domain} ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv',
    f'inurl:"{domain}" not for distribution | confidential | \"employee only\" | proprietary | top secret | classified | trade secret | internal | private filetype:xls OR filetype:csv OR filetype:doc OR filetype:pdf',
    f'site:{domain} ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:env | ext:ini | ext:xls | ext:yml | ext:log',
    f'site:{domain} ext:sql | ext:dbf | ext:mdb"',
    f'site:{domain} intext:\"sql syntax near\" | intext:\"syntax error has occurred\" | intext:\"incorrect syntax near\" | intext:\"unexpected end of SQL command\" | intext:\"Warning: mysql_connect()\" | intext:\"Warning: mysql_query()\" | intext:\"Warning: pg_connect()\"',
    f'site:{domain} \"PHP Parse error\" | \"PHP Warning\" | \"PHP Error\"',
    f'site:{domain} inurl:wp-content | inurl:wp-includes',
    f'site:{domain} intitle:"Index of" wp-admin',
    f'site:s3.amazonaws.com confidential OR "top secret" "{domain}"',
    f'site:blob.core.windows.net | site:googleapis.com | site:drive.google.com | site:docs.google.com/spreadsheets | site:groups.google.com "{domain}"',
    f'site:{domain} jdbc:sqlserver://localhost:1433 + username + password ext:yml | ext:java',
    f'site:{domain} inurl:"/content/dam" ext:txt',
    f'site:{domain} intext:"index of /.git"',
    f'site:{domain} allintext:username filetype:log',
    f'site:{domain} inurl:/proc/self/cwd',
    f'site:{domain} intitle:"index of" inurl:ftp',
    f'site:{domain} intitle:"Apache2 Ubuntu Default Page: It works"',
    f'site:{domain} "Index of" inurl:phpmyadmin',
    f'site:{domain} inurl:Dashboard.jspa intext:"Atlassian Jira Project Management Software"',
    f'allintitle:restricted filetype:doc site:{domain}',
    f'site:{domain} inurl:"server-status" intitle:"Apache Status" intext:"Apache Server Status for"',
    f'site:{domain} intitle:"Airflow: Sign In"',
    f'site:{domain} inurl:"/sym404/" | inurl:"/wp-includes/sym404/"',
    f'site:{domain} inurl:"wp-content/debug.log"',
    f'site:{domain} inurl:"/app_dev.php"',
    f'site:{domain} inurl:"phpMyAdmin/setup/index.php"',
    f'site:{domain} inurl:/webmail/ intext:Powered by IceWarp Server',
    f'site:{domain} ext:env "db_password"',
    f'site:{domain} intext:APIKey ext:js | xml | yml | txt | conf | py -github -stackoverflow intitle:"index of"',
    f'site:{domain} inurl:"/printenv" "REMOTE_ADDR"'
]

for dork in dorks:
    print(f"Scanning dork: {dork}")
    for page in range(num_pages):
        start_index = page * results_per_page
        url = f"https://www.google.com/search?q={dork}&num={results_per_page}&start={start_index}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        search_re = soup.select('.egMi0 a')

        for se in search_re:
            url = unquote(se['href'])
            start_index = url.index('/url?q=') + len('/url?q=')
            end_index = url.index('&sa=')
            print(url[start_index:end_index])
