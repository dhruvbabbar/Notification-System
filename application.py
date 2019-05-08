#flask modules
from flask import Flask,render_template,request

#flask mail module
from flask_mail import Mail
from flask_mail import Message 

#email address validator
from validate_email import validate_email

from decorators import require_appkey
import json
import os

#initialize app
application = Flask(__name__)

#import configurations
application.config.from_pyfile('config.cfg')

application.secret_key=os.urandom(24)
#initialize mail for the application
mail = Mail(application)

#POST request for sending email with a decorator to check for API key.
@application.route('/sendEmail',methods=['POST'])
@require_appkey
def sendEmail(): 
    responseList= []
    if request.method=='POST':
        
        defaultMessage="This is to notify you."
        defaultSubject="Notification"
        emailData = request.json.get('data')
        for row in emailData:
            
            #and validate_email(row['to'])
            if 'to' in row :
                emailTo=row['to']
                
                if validate_email(emailTo):                   
                    if 'messageBody' in row:
                        message=row['messageBody']
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
                         response={"To":emailTo,
                                    "Code":"301",
                                    "Status":"Not Delivered"
                                    }#exception
                    else:
                        response={"To":emailTo,
                                    "Code":"200",
                                    "Status":"Delivered"
                                    }#success
                    responseList.append(response)
                else:
                    response={"To":emailTo,
                            "Code":"303",
                            "Status":"Not Delivered"
                            }#no email id present
                    responseList.append(response)
                    
            else:                
                response={"To":"None",
                            "Code":"302",
                            "Status":"Not Delivered"
                            }#no email id present
                responseList.append(response)
               

   
    return (json.dumps(responseList))

if __name__ == "__main__":
   
    application.debug = True
    application.run()