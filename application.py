from flask import Flask,render_template,request
from flask_mail import Mail
from flask_mail import Message 
from validate_email import validate_email
#from config import Config
from decorators import require_appkey
import json
import pprint

#initialize app
application = Flask(__name__)
#import configurations
application.config.from_pyfile('config.cfg')
#initialize mail for the application
mail = Mail(application)

#POST request for sending email with a decorator to check for API key.
@application.route('/sendEmail',methods=['POST','GET'])
@require_appkey
def sendEmail(): 
    responseList= []
    if request.method=='POST':
        
        defaultMessage="This is to notify you."
        defaultSubject="Notification"
        emailData = request.json.get('Email_Data')
        for row in emailData:
            
            #and validate_email(row['to'])
            if 'to' in row :
                emailTo=row['to']
                
                if validate_email(emailTo):                   
                    if 'message' in row:
                        message=row['message']
                    else:
                        message=defaultMessage


                    if 'subject' in row:
                        subject=row['subject']                    
                    else:
                        subject=defaultSubject

                    msg = Message(subject,
                              sender="dhruvbabbar349@gmail.com",
                              recipients=[emailTo])
                    msg.html = render_template('mailTemplate.html',message=message)

                    try:
                        mail.send(msg)
                    except Exception as err:
                         response={"Email To":emailTo,
                                    "Code":"301",
                                    "Status":"Not Delivered"
                                    }#exception
                    else:
                        response={"Email To":emailTo,
                                    "Code":"200",
                                    "Status":"Delivered"
                                    }#success
                    responseList.append(response)
                else:
                    response={"Email To":emailTo,
                            "Code":"303",
                            "Status":"Not Delivered"
                            }#no email id present
                    responseList.append(response)
                    
            else:                
                response={"Email To":"None",
                            "Code":"302",
                            "Status":"Not Delivered"
                            }#no email id present
                responseList.append(response)
               

    else:
        response={  "Email To":"N.A",
                    "Code":"315",
                      "Status":"GET requests are not allowed."
                    }#no get requests
        responseList.append(response)
       
    pprint.pprint(json.dumps(responseList))
    return (json.dumps(responseList))
    


if __name__ == "__main__":
   
    application.debug = True
    application.run()