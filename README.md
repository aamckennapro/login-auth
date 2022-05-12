# login-auth
A simple and quick login-authentication process.

## Current Features
Sign up with a 5-16 character username, email address, 8-16 character password. Password requires at least 1 letter, number, and symbol.
Authentication is required upon login <strong>every time</strong> a login attempt occurs. The authentication code is sent to the email address
the user signs up with. Authentication code is generated after a <strong>successful</strong> login attempt and is six characters in length. Everything is
currently stored in a local database written in Postgres but could be adapted into another DB. 

## Future Addendums
- Passwords are <strong>not</strong> currently salted or hashed, which is obviously dangerous for a real implementation. Neither are the auth codes,
  which are less important but still a security risk.
- None of the input fields are safe from SQL injections <i>to my knowledge</i> as I have yet to test it, obviously not ideal. 
- A few of the source files need to be refactored for readability.
- Documentation.

## Tech
 - Built with Python and Flask, utilizing Flasks ability to run templates.
 - All required libraries can be found in `requirements.txt`

## How Can This Be Used?
It could be very realistically implemented as a website backend for a simple authentication service. The sign-up, login, and 2fa service are all fully
written and working.
