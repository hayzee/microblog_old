rem Email server environment vars - see app.__init__.py

rem Google server settings example
rem set MAIL_SERVER=smtp.googlemail.com
rem set MAIL_PORT=587
rem set MAIL_USE_TLS=1
rem set MAIL_USERNAME=<your-gmail-username>
rem set MAIL_PASSWORD=<your-gmail-password>

rem Dev/Test server email settings
rem run "python -m smtpd -n -c DebuggingServer localhost:8025" in a separate window
set MAIL_SERVER=localhost
set MAIL_PORT=8025

rem Allows the app to be run in debug mode from the command line

rem **** DEBUG MODE = 1 - DO NOT SET THIS IN A PRODUCTION ENVIRONMENT ****
set FLASK_DEBUG=1

rem Set the app to run and invoke
set FLASK_APP=microblog.py
flask run
