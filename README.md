# login-auth
A simple and quick login-authentication process.

## Basic Version
Connects to remote db.
User types in username and password to authentication page, sends you to a different page once authenticated.
If authentication fails, user is prompted to try again. 

## Possible Addendums
Ability to sign up via e-mail, maybe even using Google. 
Can reset password via sending e-mail.
Add 2FA as an option.
Currently storing passwords in an unsafe manner (not salted, not hashed). Store passwords salted and hashed.

## Tech
 - Built with Python and Flask, utilizing Flasks ability to run templates.

## Reason For This Project
I'd like to mess around with Python a little bit while staying within my comfort zone.
