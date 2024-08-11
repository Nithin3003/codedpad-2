from flask_pymongo import PyMongo
from flask import Flask,redirect,url_for,render_template,request,session,jsonify
# from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_urlsafe
import os
# import google.generativeai as genai
from datetime import datetime
import vertexai
from vertexai.generative_models import GenerativeModel, Part




app= Flask(__name__) 

os.environ["url"] = "mongodb+srv://msnithin84:Nithin@cluster0.wob2cfi.mongodb.net/coded"

app.config['MONGO_URI'] = os.environ.get('url')
app.config['SECRET_KEY'] = token_urlsafe(32)

mongo = PyMongo(app)
coded = mongo.db.codedpad

def check_password():
    db_password = coded.find_one({'password' : session['user_password'] })
    return db_password if db_password else False


def curr_date():
    date = datetime.now()
    return date if date else ""


def check_newdata():
    db_data = coded.find_one({'password' : session['user_password']})
    return db_data  if db_data else False


@app.route('/')
def home():
    return render_template("index.html" )


@app.route("/notes", methods=['POST'])
def display_data():
  if request.method == 'POST':
    try:
      session['user_password'] = request.form['password']
      result = check_password()
      return render_template('index.html', data=result if result else 'No data found')
    except Exception as e:
      # Log the error for further analysis
      app.logger.error(f'Error in display_data: {e}')
      return render_template('index.html', error='An error occurred. Please try again.')
  return 'get method'



@app.route('/save', methods=['POST', 'GET'] )
def save_data():
    if request.method =='POST':
        value = request.form['data']
        old_data  =check_newdata()
        if old_data and old_data['data'] != value:
            try:
                update= coded.find_one_and_update({'password' :session['user_password']}, { '$set':{ 'data': value }}) #session['user_password'] = None
                return redirect('/')
            except Exception as e:
                print('error '+e)

                return f"<h1>Internal Server Error</h1>"+e
                
    
        else:#new data / password 
            try:
                insert= coded.insert_one({'password' :session['user_password'],'data': value  } )
                return redirect('/')
            except Exception as e:
                print('error '+e)
                return f"<h1>Internal Server Error</h1>"+e
            # store_password.clear
            # session['user_password'] = None


    return 'get <a href="/"><button> Go back </button></a>'


@app.route('/gemini')
def gemini():
    return render_template('gemini.html')





def generates_text(prompt):
    project_id = "affable-hall-427403-u5"   
    try:
        vertexai.init(project=project_id, location="us-central1")

        model = GenerativeModel("gemini-1.5-flash")


        response = model.generate_content(prompt)
        return response.text.replace('**', '')
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error generating text"

@app.route('/chat',methods=['POST','GET'])
def chat():
    if request.method == 'POST':
        try:
            prompt= request.form['prompt']
            # text= generate_text(a).replace('*', '')
            # prompt = request.json['prompt']
            generated_text = generates_text(prompt)

            return render_template('gemini.html', use=generated_text.replace('##',''))
        except  Exception as e:
            return render_template('gemini.html', use=e)
            
    return redirect(url_for('gemini'))



@app.route('/amazonclone')
def amazon():
    return render_template('amazon.html')

# Initialize Vertex AI (usually done once per app instance)


@app.route('/ads.txt')
def ads():
    return send_from_directory("static", "ads.txt")




@app.route("/robots.txt")
def robots_dot_txt():
    return "User-agent: *\nDisallow: /"




@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/next')
def next():
    return render_template('nextpage.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.errorhandler(404)  
def not_found(e):  
    print(e)
    return "<h1>Page not found 404 error</h1>" 

@app.errorhandler(500)
def internal_server_error(e):
    print(e)
    return "<h1>Internal Server Error 500</h1>", 500

@app.errorhandler(Exception)
def handle_error(e):
    print(e)
    return f"<h1>Internal Server Error Exception</h1>", 500




if __name__=='__main__':
    app.run(host="127.0.0.1", port=8080,debug=True)