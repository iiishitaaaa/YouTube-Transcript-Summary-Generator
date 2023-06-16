from flask import Flask, jsonify, request
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from urllib.parse import urlparse, parse_qs
from flask_cors import CORS, cross_origin


# define a variable to hold your app
app = Flask(__name__)
CORS(app)

# define your resource endpoints
@app.route('/')
def index_page():
    return "Hello world"

@app.route('/api/summarize', methods=['GET'])
@cross_origin(origin='*')
def extr_yturl():
    args = request.args
    
    args = args.to_dict()
    print(args)
    url = str(args['youtube_url'])
    print(url)
    variable = transc(get_vid(url))
    return transcript_summary(variable)

# http://[hostname]/api/summarize?youtube_url=<url>
# https://www.youtube.com/watch?v=8EPJiFfWRfw

def transc(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en-US', 'en'])
    strr = ""
    for t in transcript :
        strr = strr + t["text"] + " "
    
    return(strr)

def transcript_summary(transcript):
    summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="pt")

    num_iters = int(len(transcript)/1000)
    summarized_text = []
    summ_t = ""
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        out = summarizer(transcript[start:end])
        out = out[0]
        out = out['summary_text']
        summarized_text.append(out)
        
    for s in summarized_text :
        summ_t = summ_t + s + " "
    
    print(str(summ_t))
    return str(summ_t)


# http://[hostname]/api/summarize?youtube_url=<url>
def get_vid(url) -> str:
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname == 'www.youtube.com':
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
    if query.path[:3] == '/v/':
        return query.path.split('/')[2]


# server the app when this file is run
if __name__ == '__main__':
    app.run(host='0.0.0.0')