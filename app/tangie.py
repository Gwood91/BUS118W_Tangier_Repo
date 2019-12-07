# Tangie library
import sys
import base64
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# function for gathering headlines
from itertools import groupby
from profanity_check import predict, predict_prob


def fetch_headlines():
    news_url = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en"
    Client = urlopen(news_url)
    xml_page = Client.read()
    Client.close()

    soup_page = soup(xml_page, "xml")
    news_list = soup_page.findAll("item")
    # Print news title, url and publish date
    # for news in news_list:
        # print(news.title.text)
        # print(news.link.text)
        # print(news.pubDate.text)
        #print("-" * 60)
    return news_list


"""HERE IS A SOMEWHAT PRIMATIVE METHOD OF GENERATING DASHBOARD VISUALS"""  # TODO: REFINE


def generate_dashboard_vis(candidate_dataset, title):
    timestamp_data = []
    cand_count_data = [0]
    """Need to fix the dates and get a count by datetime to the hour"""
    for candidate in candidate_dataset:
        format_time = str(candidate.timestamp).split(" ")[0]
        timestamp_data.append(format_time)
    time_count = 0
    for time in timestamp_data:
        if time == format_time:
            time_count += 1
    # get canidate count by datetime
    cand_count_data = [0] + [len(list(group)) for key, group in groupby(timestamp_data)]
    # cand_count_data.append(time_count)
    timestamp_data = ["Dawn of Time"] + timestamp_data
    timestamp_unique = []
    for time_stamp in timestamp_data:
            # check if exists in unique_list or not
            if time_stamp not in timestamp_unique:
                timestamp_unique.append(time_stamp)
    plt.style.use('dark_background')  # change the color theme
    fig, ax = plt.subplots()
    ax.set_title(title)  # set the axis title
    # ax.plot(timestamp_data, cand_count_data)  # create the plot
    ax.fill_between(timestamp_unique, cand_count_data)
    print(cand_count_data, timestamp_unique, file=sys.stderr)
    ax.grid("on")
    img = plt.savefig("plt_img", format='png')  # save the plot as base64 string
    with open("plt_img", "rb") as img_file:
        raw_base64 = str(base64.b64encode(img_file.read()))
        plt_base64 = "src=" + "data:image/png;base64,{}"
        plt_base64 = plt_base64.format(raw_base64[2:-1])  # format the base 64 string for html rendering
    return plt_base64


def filter_content(content):
    # split the content string for SVM prediction
    content_split = content.split()
    filtered_content = []
    # add word to filtered content if not profane
    for word in content_split:
        x = predict([word])
        if x[0] == 0:  # profane is "false"
            filtered_content.append(word)
    s = " "
    filtered_string = s.join(filtered_content)
    return filtered_string
