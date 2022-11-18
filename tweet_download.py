#!/usr/bin/python3

import os
import re
import argparse
import json
import os.path
from os import path

#NOTE: install snscrape with pip before running

#usage: ./tweet_download [user] [-r]
#-r includes replies in output

def main():

    parser = argparse.ArgumentParser(
            description='Downloads tweets to a csv format')
    parser.add_argument(
            'user', help='Twitter account to scrape', type=str)
    parser.add_argument('-r', '--replies', help='Include replies in output', action='store_true')
    args = parser.parse_args()

    #exclude replies if -r arg not present
    exclude = ''
    if not args.replies :
        exclude = 'exclude:replies'        

    #scrape tweets with snscrape
    os.system(f"snscrape --jsonl --progress twitter-search 'from:{args.user} {exclude}' > ./tmp.json")

    #read json file produced by snscrape
    if path.exists('./tmp.json') :
        #write to csv
        with open(f'./{args.user}.csv', 'w') as o:
            o.write('Date,Tweet,URL\n')
            with open("./tmp.json") as f:
                for line in f:
                    record = json.loads(line)
                    date = record['date']
                    #double quotes replaced with single so they don't interfere with csv parsing
                    tweet = re.sub('"', '\'', record['renderedContent'])
                    url = record['url']
                    o.write(f'{date},"{tweet}",{url}\n')
        #clean up temp file
        os.system('rm ./tmp.json')
    else :
        message = f'{args.path} not found'
        raise Exception(message)

if __name__ == '__main__':
    main()

