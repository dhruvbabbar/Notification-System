#import main application
from application import application

#decorator to check for API key
from emailService import require_appkey

from flask import render_template,request

#email address validator
from validate_email import validate_email

#flask mail module
from flask_mail import Mail
from flask_mail import Message 
#initialize mail for the application
mail = Mail(application)

import json

#HTTP error codes
from enumCodes import Codes

#POST request for sending email with a decorator to check for API key.
@application.route('/sendEmail',methods=['POST'])
@require_appkey
def sendEmail(): 
    responseList= []
    if request.method=='POST':
        emailData = request.json.get('data')
        for row in emailData:            
            #and validate_email(row['to'])
            if 'recipients' in row :
                recipients=row['recipients']
                recipientRowResponse=[]
                for recipient in recipients:
                    if (validate_email(recipient)):
                        if 'subject' in row:
                            subject=row['subject']
                            if 'messageBody' in row:
                                messageBody=row['messageBody']
                                msg = Message(subject,
                                  sender="dhruvbabbar349@gmail.com",
                                  recipients=[recipient])
                                msg.html = render_template('mailTemplate.html',message=messageBody)
                                try:                                    
                                    mail.send(msg)
                                except Exception as err:
                                    response={"To":recipient,
                                                "Code":Codes.exceptionWhileSending.value,
                                                "Status":"Unsuccessfull"
                                                }#exception
                                else:
                                    response={"To":recipient,
                                            "Code":Codes.success.value,
                                            "Status":"Success"
                                            }#success                                
                            else:
                                response={"To":recipient,
                                        "Code":Codes.unprocessable.value,
                                        "Status":"Unsuccessfull"
                                        }#no message body   
                        else:
                            response={"To":recipient,
                                        "Code":Codes.unprocessable.value,
                                        "Status":"Unsuccessfull"
                                        }#no message subject  
                    else:
                        response={"To":recipient,
                                    "Code":Codes.unprocessable.value,
                                    "Status":"Unsuccessfull"
                                    }#invalid email
                        
                    recipientRowResponse.append(response)
                responseList.append(recipientRowResponse)
            else:       
                response={"To":"None",
                            "Code":Codes.unprocessable.value,
                            "Status":"Unsuccessfull"
                            }#no email id present
                responseList.append(response)
                
    return (json.dumps(responseList))