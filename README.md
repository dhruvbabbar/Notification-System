# ReadMe

>This repository has a structure of a generic Notification Email System . 
>

## To setup dev environment
```sh
 virtualenv env
 cd env/bin/activate
 pip install -r requirements.txt
```
=======

## Run
``` sh
application.py 
```
## API details are mentioned in the Rest API Documentation.word file.

>process flow: application.py----calls-->emailController.py--->calls--->emailService.py
>
>Application assumtions/restrictions:
>1. SMTP user details have to be mentioned beforehand in the config file, therefore sender can only be the person/persons listed in the > config file. A special token is generated in Gmail manually, which is used as the password. 
>2. SMTP server details are static- Gmail in my example
>3. SMTP exceptions are not handled but can be used for logging.
>4. Slack implementation requires API token and Channel key, therefore not implemented in this service.




