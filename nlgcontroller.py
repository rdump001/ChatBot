#importing requiremts
from flask import Flask, request, make_response, jsonify
app = Flask(__name__)



#import pandas as pd
import json
from nlg.nlgprocess import nlgprocess



@app.route('/ask',methods=["POST"])
def data():
     
    # here we want to get the value of user (i.e. ?user=some-value)
    query_from_user = request.args.get('query')
    query = query_from_user
    # print(query)
    np = nlgprocess()
    answer_from_nlp = np.nlg_main(query)
    query_answer = {
        "answer" : answer_from_nlp
    }
    
    return make_response(jsonify(query_answer))

    
if __name__ == '__main__':
   app.run(port=7875,debug=True)
