from flask import Flask, request, render_template, jsonify
import disease
import pickle
app = Flask(__name__)

with open("my_dict.pkl", "rb") as f:
    disease_list = pickle.load(f)

@app.route('/')
def hello(name=None):
    return render_template('website.html', name=name)

@app.route('/submitdata', methods=['POST'])
def process_symptoms():
    global description,precaution1,precaution2,precaution3,precaution4
    try:
        symptoms = request.json
        separator=','
        string_symptoms = separator.join(symptoms)
        output1 = "You selected: " + ", ".join(symptoms)
        predicted=disease.predictDisease(string_symptoms)
        output=f"{predicted}"
        disease1 = output
        description,precaution=disease.get_disease(disease1,disease_list)
        precaution1,precaution2,precaution3,precaution4=precaution[0],precaution[1],precaution[2],precaution[3]
        return jsonify(output=output)
    except Exception as e:
        app.logger.error(e)
        return jsonify(msg="Sorry, The inputs you selected did not result in any predicted disease. Please make sure to select proper symptoms."), 500
        print("error sent")
@app.route('/results')
def results():
    # get all the parameters from the query string
    output = request.args.get('output')
    
    
    # pass all the parameters to the template
    return render_template('result.html', output=output, description=description, precaution1=precaution1, precaution2=precaution2, precaution3=precaution3, precaution4=precaution4)

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(msg="Sorry, The inputs you selected did not result in any predicted disease. Please make sure to select proper symptoms. "), 500

if __name__ == '__main__':
    app.run()

