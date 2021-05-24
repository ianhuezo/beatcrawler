[![Build Status](https://travis-ci.com/ianhuezo/beatcrawler.svg?token=RjjacHpzdoW51tzGskcD&branch=main)](https://travis-ci.com/ianhuezo/beatcrawler)
---

Beatcrawler is a simple way to retrieve songs from specific users on https://scoresaber.com using https://beatsaver.com as the download reference site.  

Simply fill out your userid, download folder path, and how many pages to download from scoresaber using python.

I strictly follow their api path, so the time to download files is slow

***
Example user id and page number:
![Alt text](resources/example.png?raw=true "Title")

***
To run this python script, download the requirements.txt and run like below with your local version of python installed
```bash
pip install -r requirements.txt
python beatsaber.py "your_user_id" "page_number" "/your/download/path"
