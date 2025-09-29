# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import time

from flask import Flask, render_template, request, render_template_string, redirect
import json

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index():
    return render_template('index.html')



@app.route('/check',  methods=['POST'])
def check_sentences():
    data = request.form.to_dict()
    sentences = data['sentences'].split('\n')
    answer = [
        { 'input': "This is correct.", 'correct': True, 'corrected': "This is correct." },
        { 'input': "He go to school.", 'correct': False, 'corrected': "He goes to school." }
    ]
    time.sleep(2)
    return render_template_string("""
        <h2>Results</h2>
        <form hx-post="/final"
              hx-target="#main"
              hx-swap="innerHTML">
          <table border="1" cellpadding="5">
            <tr>
              <th>Input</th>
              <th>Status</th>
              <th>Corrected</th>
              <th>Agree?</th>
            </tr>
            {% for row in answer %}
            <tr>
              <td>{{ row.input }}</td>
              <td>{{ 'Correct' if row.correct else 'Incorrect' }}</td>
              <td>{{ row.corrected }}</td>
              <td>
                <select name="agree_{{ loop.index }}" required>
                  <option value="" selected disabled></option>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
              </td>
            </tr>
            {% endfor %}
          </table>
          <br>
          <button type="submit">Submit Feedback</button>
          <button type="button"
                  hx-get="/"
                  hx-target="#main"
                  hx-swap="innerHTML">Back</button>
        </form>
        """, answer=answer)

@app.route("/final", methods=["POST"])
def final():
    data = dict(request.form)
    print(data)
    return redirect('/')

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
