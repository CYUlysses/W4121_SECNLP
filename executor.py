import pandas as pd
import urllib.request
import codecs
import os
import re
from bs4 import BeautifulSoup


edgar = pd.read_csv('edgar.csv').values
edgar_link = 'https://www.sec.gov/Archives/'


def clean_html(saved_name, file_url):
    with urllib.request.urlopen(file_url) as response:
        html_file = response.read()
    soup = BeautifulSoup(html_file, 'lxml')
    for table in soup.find_all("table"):
        table.extract()
    temp_file = codecs.open('data/' + saved_name + '.txt', 'w', 'utf-8')
    temp_file.write(soup.get_text())
    temp_file.close()


def nlp_extract(file_name):
    key_start = '. MANAGEMENTS DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS'.lower()
    if file_name.split('-')[2] == '10K':
        item = 7
    else:
        item = 2
    key_end = ('Item ' + str(item + 1)).lower()
    file_in = codecs.open('data/' + file_name, 'r', 'utf-8')
    text_lines = file_in.readlines()
    file_in.close()
    file_out = codecs.open('data_nlp/' + file_name, 'w', 'utf-8')
    write_str = ''
    for line in text_lines:
        temp_line = re.sub('[^a-z0-9 .,?!:-]+', '', line.rstrip().lower())
        if temp_line == '' or 'Table of Contents' in temp_line or temp_line.isdigit():
            continue
        write_str += ' ' + temp_line
    try:
        start_index = write_str.index(key_start) + len(key_start)
    except:
        start_index = write_str.index(key_start[1:]) + len(key_start[1:])
    write_str = write_str[start_index:]
    try:
        end_index = write_str.index(key_end)
    except:
        end_index = write_str.index(key_end[:-1])
    file_out.write(write_str[:end_index])
    file_out.close()


for file_name in os.listdir('data'):
    try:
        nlp_extract(file_name)
    except:
        continue


for i in range(62412, len(edgar)):
    temp_file_name = (edgar[i][6] + '-' + str(edgar[i][1])).replace('/', '')
    temp_file_url = edgar_link + edgar[i][4]
    if edgar[i][2] == '10-K':
        clean_html(temp_file_name + '-10K', temp_file_url)
    elif edgar[i][2] == '10-Q':
        clean_html(temp_file_name + '-10Q', temp_file_url)

file_data = []
for file_name in os.listdir('data_nlp'):
    temp_file_nlp = codecs.open('data_nlp/' + file_name, 'r', 'utf-8')
    if len(temp_file_nlp.read()) > 10:
        file_data.append(file_name)
    temp_file_nlp.close()


file_csv = pd.DataFrame(file_data, columns=['file_name'])
file_csv.to_csv('valid_file.csv', index=True)

