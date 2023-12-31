from transformers import pipeline
from flask import Flask
app = Flask(__name__)

text_example = '''The tower is 324 meters (1,063 ft) tall, about the same height 
as an 81-storey building, and the tallest structure in Paris. Its base is square, 
measuring 125 meters (410 ft) on each side. During its construction, the Eiffel 
Tower surpassed the Washington Monument to become the tallest man-made structure 
in the world, a title it held for 41 years until the Chrysler Building in New York
City was finished in 1930. It was the first structure to reach a height of 300 meters. 
Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is 
now taller than the Chrysler Building by 5.2 meters (17 ft). Excluding transmitters, 
the Eiffel Tower is the second tallest free-standing structure in France
after the Millau Viaduct.'''

@app.route('/')
def summarise_text_eg():
    summarizer = pipeline("summarization", model = "facebook/bart-large-cnn")
    return summarizer(text_example)

if __name__ == '__main__':
    app.run(host='0.0.0.0')