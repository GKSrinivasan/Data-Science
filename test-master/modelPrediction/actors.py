# using python 3
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from data import ACTORS
from sklearn.externals import joblib
from werkzeug import secure_filename
from collections import Counter
import json
from textblob import TextBlob


app = Flask(__name__)
# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'some?bamboozle#string-foobar'
# Flask-Bootstrap requires this line
Bootstrap(app)
# this turns file-serving to static, using Bootstrap files installed in env
# instead of using a CDN
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    name = StringField('Find the topic of the Review?', validators=[Required()])
    submit = SubmitField('Submit')

# define functions to be used by the routes (just one here)


def predict_label_ori(text,nmf,vectorizer,level):
        my_dict = {}
        x = nmf.transform(vectorizer.transform([text]))[0]
        #print(x, x.sum())

        for index, item in enumerate(x):
            my_dict[index] = x[index]

        #print(my_dict)

        a1_sorted_keys = sorted(my_dict, key=my_dict.get, reverse=True)
        i = 1
        res=[]
        num =3
        print(a1_sorted_keys)
        if((my_dict[a1_sorted_keys[0]]-my_dict[a1_sorted_keys[1]])>0.001):
            num = 2
        for r in a1_sorted_keys:
            if(i<num and my_dict[r]>0.0):
            #if(i<num):

                print(r, my_dict[r])

                data = level[r]
                percent = (round(my_dict[r]*100,2))
                if(data!=None):
                    data = level[r]
                    #data = str(level[r] +" "+ str(round(my_dict[r]*100,2))+ "%")
                    #print(data)
                    i=i+1
                    res.append(data)
        return res

def predict_label(text,nmf,vectorizer,level):
        my_dict = {}
        x = nmf.transform(vectorizer.transform([text]))[0]
        #print(x, x.sum())

        for index, item in enumerate(x):
            my_dict[index] = x[index]

        #print(my_dict)

        a1_sorted_keys = sorted(my_dict, key=my_dict.get, reverse=True)
        i = 1
        res=[]
        num=3
        minMax = normalize(list(my_dict.values()))
        flag=False
        print((minMax[a1_sorted_keys[1]]-minMax[a1_sorted_keys[2]]))
        if((minMax[a1_sorted_keys[0]]-minMax[a1_sorted_keys[1]])>0.50):
            num = 2
            flag=True
        elif(flag==False & ((minMax[a1_sorted_keys[1]]-minMax[a1_sorted_keys[2]])<0.40)):
            num = 4
        print(num)
        for r in a1_sorted_keys:
            if(i<num and my_dict[r]>0.0):
                #print(r, my_dict[r])

                data = level[r]
                percent = (round(my_dict[r]*100,2))
                if(data!=None):
                    data = level[r]
                    #data = str(level[r] +" "+ str(round(my_dict[r]*100,2))+ "%")
                    #print(data)
                    i=i+1
                    res.append(data)
        return res

def normalize(x): 
    #x = list(my_dict.values())
    #Normalized Data
    normalized = (x-min(x))/(max(x)-min(x))
    print(x)
    print(normalized)
    return normalized





def topic_prediction(review):
    """msg = []
    x = nmf.transform(vectorizer.transform([review]))[0]
    print(x, x.sum())
    my_dict = {}
    for index, item in enumerate(x):
        my_dict[index] = x[index]
    IssueMap={0: "Other issue", 1:"Other issue",2: "Camera Issue", 3: "Other Issue", 4: "Other Issue", 5: "OS / Software Issue", 6: "Other issue", 7: "Other issue", 8: "Other issue", 
    9: "Other Issue", 10: "Physical Damage/Broken Issue", 11: 15,12: 10, 13: "Broken Issue", 14: 18, 15: 18, 16: "Payment Issue", 
    17: "Button Issue", 18: "Battery Issue", 19: 21, 20: 8,21: "Audio Issue", 22: "Connectivity Issue", 
    23: "Cursor/Tracking issue", 24: "Video Issue", 25: 24, 26: "Modify subscription/ Payment issue", 
    27: "Wifi Internet Connectivity issue", 28: "Password/Reset issue", 29: "other"
    }
    a1_sorted_keys = sorted(my_dict, key=my_dict.get, reverse=True)
    i = 1
    for r in a1_sorted_keys:
        if(i<3 and my_dict[r]>0.0):
            #print(r, my_dict[r])
            str = (IssueMap[r],round(my_dict[r]*100,2),"%")
            msg.append(str)
            i=i+1
    return msg"""
    res1 = predict_label(review,nmf,vectorizer,IssueMap_level_1)
    res2 = predict_label(review,nmf_26,vectorizer_26,IssueMap_nmf_26_level_1)
    res3 = predict_label(review,nmf_40,vectorizer_40,IssueMap_nmf_40_level_1)

    res = res1+res2+res3
    print(res)
    result_dict =  dict(Counter(res))
    sum=0
    for key, value in result_dict.items():
        result_dict[key] = str(round(value/len(res),2)*100)
        sum += round(value/len(res),2)*100
    print(sum)

    return json.dumps(result_dict)

def stringToDict(data):
    json_acceptable_string = data.replace("'", "\"")
    msg_dict = json.loads(json_acceptable_string)
    return msg_dict
# all Flask routes below

# two decorators using the same function
@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = " "
    if form.validate_on_submit():
        name = form.name.data
        blob = TextBlob(name)
        name = str(blob.correct())
        msg = topic_prediction(name)
        print(msg)
        

        
        msg_dict = stringToDict(msg)
        #word_dict = dict.fromkeys(msg_dict.keys(),[])
        word_dict = {k:[] for k in list(msg_dict.keys())}
        print("word_dict+++++++++++++++++++++++++++++",word_dict)
        for word in name.split():
            print("$$$$$$$$$$$$$$$$$$$$")
            print(word)
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",topic_prediction(word))
            print("********************")
            wordRes = topic_prediction(word)
            wordRes = stringToDict(wordRes)

            print("**************************************",wordRes)
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&7",word_dict)
            for key,value in wordRes.items():
                     #word_dict[key] = word_dict[key].append(word)
                     print("Key:::::::::::::::::",key)
                     a = word_dict.get(key, [])
                     a.append(word)
                     word_dict[key] = a
                     print("!@#$%^&*(((((((()",word_dict)
        if len(word_dict)>0:
            word_dict = json.dumps(word_dict)
        if len(msg)>0:
            message = msg
            # empty the form field
            form.name.data = ""
        else:
            message = " "
    # notice that we don't need to pass name or names to the template
    #context={'message':message,'word_dict':word_dict}
    context={'message':message,'word':word_dict}
    return render_template('index.html', form=form, **context)


#@app.route('/upload')
#def upload_file():
#   return render_template('upload.html')
    
#@app.route('/uploader', methods = ['GET', 'POST'])
#def upload_file():
#   if request.method == 'POST':
#      f = request.files['file']
#      f.save(secure_filename(f.filename))
#      return 'file uploaded successfully'

# keep this as is
if __name__ == '__main__':
    nmf = joblib.load('nmfModel.pkl')
    vectorizer = joblib.load('vectorizer.bin')
    nmf_26 = joblib.load('nmfModel_26.pkl')
    vectorizer_26 = joblib.load('vectorizer_26.bin')
    nmf_40 = joblib.load('nmfModel_40.pkl')
    vectorizer_40 = joblib.load('vectorizer_40.bin')
    IssueMap_level_1={0: "Charging", 1:"Button/Key Issue",2: "Charging", 3: "Button/Key Issue", 4: "Functionality Issue", 
                  5: "Button/Key Issue", 6: "Sound / Audio Issue", 7: "Cursor/Tracking/Movement Issue", 
                  8: "Connectivity Other Issue", 
    9: "Defect", 10: "Charging", 11: "User Assistance",12: "Connectivity Other Issue", 13: "Charging", 14: "Button/Key Issue",
                  15: "Order", 16: "Functionality Issue", 
    17: "Button/Key Issue", 18: "Battery Issue", 19: "Charging", 20: "Connectivity Other Issue",21: "Charging", 
                  22: "Sound / Audio Issue", 
    23: "Software / Firmware", 24: "Inquiries", 25: "Ticket Management", 26: "Charging", 
    27: "Connectivity Other Issue", 28: "Charging", 29: "Charging"
    }
    IssueMap_level_2={0: "Sound / Audio Issue", 1:"Button/Key Issue",2: "Sound / Audio Issue", 3: "Button/Key Issue", 4: "Charging", 
                  5: "Defect", 6: "Defect", 7: "Button/Key Issue", 8: "Charging", 
    9: "Connectivity Other Issue", 10: "Charging", 11: "Remote or Hub HW",12: "Connectivity Other Issue", 13: "Connectivity Other Issue", 14: "Defect",
                  15: "Ticket Management", 16: "Charging", 
    17: "Defect", 18: "Spare Parts", 19: "Connectivity Other Issue", 20: "Software / Firmware",21: "Connectivity Other Issue",
                  22: "Sound / Audio Issue", 
    23: "Connectivity Other Issue", 24: "Connectivity Other Issue", 25: "Defect", 26: "Connectivity Other Issue", 
    27: "Connectivity Other Issue", 28: "Sound / Audio Issue", 29: "Connectivity Other Issue"
    }

    IssueMap_level_3={0: "Connectivity Other Issue", 1:None,2: "Connectivity Other Issue", 3: None, 4: "Spare Parts", 
                  5: "Ticket Management", 6: "Connectivity Other Issue", 7: "Connectivity Other Issue", 8: "Spare Parts", 
    9: "Ticket Management", 10: None, 11: "App Issue",12: None, 13: "Sound / Audio Issue", 14: "Ticket Management", 
                  15: "Returns / Refund", 16: "Spare Parts", 
    17: None, 18: "Inquiries", 19: None, 20: "Button/Key Issue",21: None, 22: None, 
    23: "Inquiries", 24: "Wifi", 25: "Charging", 26: "Button/Key Issue", 
    27: None, 28: "Connectivity Other Issue", 29: "Button/Key Issue"
    }
    IssueMap_nmf_26_level_1={0: "Charging", 1:"Connectivity Other Issue",2: "Charging", 3: "Button/Key Issue", 
                             4:       "Functionality Issue", 
                  5: "Charging", 6: "Sound / Audio Issue", 7: "Cursor/Tracking/Movement Issue", 8: "Button/Key Issue", 
    9: "Defect", 10: "Ticket Management", 11: "User Assistance",12: "Connectivity Other Issue", 13: "Charging", 
                             14: "Button/Key Issue",
                  15: "Order", 16: "Functionality Issue", 
    17: "Charging", 18: "Connectivity Other Issue", 19: "Charging", 20: "Connectivity Other Issue",21: "Charging", 
                  22: "Sound / Audio Issue", 
    23: "Connectivity Other Issue", 24: "Charging", 25: "Charging"
    }
    IssueMap_nmf_26_level_2={0: "Sound / Audio Issue", 1:"Button/Key Issue",2: "Sound / Audio Issue", 3: "Ticket Management", 
                         4: "Charging", 
                  5: "Charging", 6: "Defect", 7: "Button/Key Issue", 8: "Defect", 
    9: "Connectivity Other Issue", 10: "Charging", 11: "Remote or Hub HW",12: "Connectivity Other Issue", 13: "Connectivity Other Issue", 
                         14: "Defect",
                  15: "Ticket Management", 16: "Charging", 
    17: "Connectivity Other Issue", 18: "Spare Parts", 19: "Connectivity Other Issue", 20: "Spare Parts",
                         21: "Connectivity Other Issue",
                  22: "Sound / Audio Issue", 
    23: "Inquiries", 24: "Connectivity Other Issue", 25: "Connectivity Other Issue"
    }

    IssueMap_nmf_26_level_3={0: "Functionality Issue", 1:'Software / Firmware',2: "Connectivity Other Issue", 
                         3: "Connectivity Other Issue", 4: "Spare Parts", 
                  5: None, 6: "Connectivity Other Issue", 7: None, 8: None, 
    9: "Ticket Management", 10: "Defect", 11: "App Issue",12: None, 13: "Sound / Audio Issue", 14: "Ticket Management", 
                  15: "Returns / Refund", 16: "Spare Parts", 
    17: "Button/Key Issue", 18: "Inquiries", 19: "Button/Key Issue", 20: "Charging",21: None, 22: None, 
    23: "Software / Firmware", 24: "Button/Key Issue", 25: "Button/Key Issue"
    }
    IssueMap_nmf_40_level_1={0: "Charging", 1:"Button/Key Issue",2: "Charging", 3: "Button/Key Issue", 4: "Ticket Management", 
                  5: "Button/Key Issue", 6: "Sound / Audio Issue", 7: "Cursor/Tracking/Movement Issue", 
                             8: "Connectivity Other Issue", 
    9: "Defect", 10: "Charging", 11: "User Assistance",12: "Connectivity Other Issue", 13: "Charging", 14: "Button/Key Issue",
                  15: "Order", 16: "Functionality Issue", 
    17: "Button/Key Issue", 18: "Connectivity Other Issue", 19: "Charging", 20: "Software / Firmware",21: "Charging", 
                  22: "Sound / Audio Issue", 
    23: "Inquiries", 24: "Sound / Audio Issue", 25: "Charging",26: "Connectivity Other Issue", 27:"Charging",
    28:"Connectivity Other Issue", 29: "Functionality Issue", 30: "Charging",31:"Connectivity Other Issue", 32: "Charging",
    33:"Functionality Issue",34:"Button/Key Issue",35:"Connectivity Other Issue",36:"Charging",37:"Connectivity Other Issue",
                         38:"Button/Key Issue",39:"Connectivity Other Issue"
    }
    IssueMap_nmf_40_level_2={0: "Sound / Audio Issue", 1:"Ticket Management",2: "Sound / Audio Issue", 
                             3: "Ticket Management", 4: "Charging", 
                  5: 'Defect', 6: "Connectivity Other Issue", 7: "Button/Key Issue", 8: "Connectivity Other Issue", 
    9: "Connectivity Other Issue", 10: "Charging", 11: "Remote or Hub HW",12: "Connectivity Other Issue", 13: "Connectivity Other Issue", 14: "Button/Key Issue",
                  15: "Order", 16: "Charging", 
    17: "Button/Key Issue", 18: "Spare Parts", 19: "Charging", 20: "Connectivity Other Issue",21: "Connectivity Other Issue",
                  22: "Sound / Audio Issue", 
    23: "Software / Firmware", 24: "Connectivity Other Issue", 25: "Connectivity Other Issue", 26: "Connectivity Other Issue", 27:"Charging",
    28:"Charging", 29: "Sound / Audio Issue", 30:"Connectivity Other Issue",31:"Charging",32:"Connectivity Other Issue",
                         33:"Charging",34:"Defect",35:"Button/Key Issue",36:"Connectivity Other Issue",37:"Button/Key Issue",
                         38:"Connectivity Other Issue",39:"Software / Firmware"
                    
                         
    }

    IssueMap_nmf_40_level_3={0: "Functionality Issue", 1:'Connectivity Other Issue',2: "Connectivity Other Issue", 
                             3: "Connectivity Other Issue", 4: "Defect", 
                  5: 'Ticket Management', 6: "Defect", 7: None, 8: None, 
    9: "Ticket Management", 10: None, 11: "App Issue",12: None, 13: "Sound / Audio Issue", 14: "Ticket Management", 
                  15: None, 16: "Spare Parts", 
    17: None, 18: "Ticket Management", 19: None, 20: "Button/Key Issue",21: None, 22: None, 
    23: "Connectivity Other Issue", 24: "Charging", 25: "Button/Key Issue", 26: None, 27: None, 28: "Button/Key Issue",
    29: "Defect",30:"Button/Key Issue",31:"Sound / Audio Issue",32:"Defect",33:"Spare Parts",34:"Sound / Audio Issue"
           ,35:"Inquiries",36:"Sound / Audio Issue",37:"Sound / Audio Issue",38:"Defect",39:"Button/Key Issue"
    }
    app.run(debug=True)
