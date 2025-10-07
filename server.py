# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import time

from flask import Flask, render_template, request, render_template_string, redirect
import json

logfile = 'requests_log.jsonl'

REAL = False

if REAL:
    from llama_cpp import Llama
    from llm_response import get_response
    model_src = '../models/roLl31I-Corrector-RRT_PRESS-0007-EP1-1per-F16.gguf'
    llm = Llama(model_src)
else:
    import random
    llm = None
    def get_response(s : str, _):
        if random.random() < 0.5:
            return s
        return s + ' bork! bork!'

answer = []


# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.

special_chars=['ă','î','â', 'ț', 'ș', 'Ă','Î','Â','Ș','Ț']

@app.route('/')
def index():
    return render_template('index.html', special_chars=special_chars)

@app.route('/check',  methods=['POST'])
def check_sentences():
    data = request.form.to_dict()
    sentences = data['sentences'].split('\n')
    sentences = [s.strip() for s in sentences if s.strip()]
    responses = [get_response(s, llm) for s in sentences]
    
    answer = [
        {'index':i,
         'input': s,
         'corrected':r if r!=s else '-',
         'correct': (s==r)}
        for i, (s,r) in enumerate(zip(sentences, responses))
    ]
    

    return render_template("result_table.html", answer=answer)

@app.route("/final", methods=["POST"])
def final():
    data = dict(request.form)
    i = 0
    in_out = []
    while f'original{i}' in data:
        in_out.append({'input':data[f'original{i}'], 'response':data[f'response{i}']})
        i += 1
    data_dump = {'ip':request.remote_addr, 'eval':data['submit_button'],
                 'data':in_out}
    # print(data_dump)
    with open(logfile, 'a') as handle:
        handle.write(json.dumps(data_dump) + '\n')

    return render_template("sentence_form.html",
                           special_chars=special_chars)

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    if REAL:
        app.run(host='0.0.0.0', port=8081, threaded=False)
    else:
        app.run(threaded=False)

