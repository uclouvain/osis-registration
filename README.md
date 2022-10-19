# osis-registration
OSIS Registration is a django application to request external account. 

<!-- It provides a publish-subscribe mecanism to enable applications (subscribers) to request user account creation. OSIS Registration enable subscribers to poll an API endpoint in order for them to catch up on the last requested results. -->

Currently, it provides a form to request account creation and propagate the request to LDAP.

## Getting started
Clone the repository
```
git clone git@github.com:uclouvain/osis-registration.git
```

Create the database (assuming you already have postgresql installed)
```
createdb osis_registration_local
createuser osis -P //provide password of your choice
psql -d osis_registration_local
  =# grant connect on database osis_registration_local to osis;
  =# revoke connect on database osis_registration_local from public;
  =# alter user osis createdb;
  =# \q
```

Enter the repository
```
cd osis-registration
```

Make sure you have some python tools needed for creating your virtual environment
```
sudo apt-get install build-essential python3-venv libjpeg-dev libpng-dev gettext
```

Create and activate venv
```
python3 -m venv venv
source venv/bin/activate
```

Install required dependencies
```
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example`:

```
cp .env.example .env
```

Create the data structre in db:
```
python3 manage.py migrate
```

Create the superuser (will later be used to access /admin page):
```
python3 manage.py createsuperuser
```

Compile translation files
```
python3 manage.py compilemessages
```

Run the server
```
python3 manage.py runserver
```

To enable 'audio captcha', please refer to the 'Espeak and Sox' section below.

That's all folks !

## API
OSIS Registration provides subscribers with a RESTful API enabling apps to request user account creation and poll the requests results. The subscribers are registered as Django users and are identified by a token.

An authorization header with the registered app token must be provided with the request.

> Authorization header
```json
{"Authorization": "Token cf4e903f8cc6cb81ae753d137bfa77cdfe1b8b37"}
```
### Endpoints

#### Create

`POST /create_account/`

Create new user account creation request

> Body parameter

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "birth_date": "1989-01-01",
  "email": "john.doe@mail.xyz",
  "password": "secret"
}
```
-----

#### Delete

`POST /delete_account/`

Create new user account deletion request

> Body parameter

```json
{
  "email": "john.doe@mail.xyz",
}
```
-----

#### Renewal

`POST /renew_account/`

Create new user account renewal request

> Body parameter

```json
{
  "email": "john.doe@mail.xyz",
  "validity_days": 365
}
```
-----

## Espeak and Sox
For the sake of accessibility, an audio captcha file is read by synthetic voice. 

### Espeak
In order to generate this file, espeak has to be installed with english and french voices through the following commands:
```
apt-get install espeak
```
Once installed, english is available as a default voice, french should be too. You can verify this with:
```
espeak --voices=fr
```
The output should include this line:
```
 5  fr-fr          M  french               fr            (fr 5)
```
If it is the case, then you are good to go. Otherwise, you will need to install voices.
http://espeak.sourceforge.net/languages.html

### Sox
Sox adds some noise to the generated audio to complexify the process of computerized captcha solving.
You may install Sox with the following command:
```
apt-get install sox
```
