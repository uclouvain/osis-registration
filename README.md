# osis-registration
OSIS Registration is a django application to handle external account management. It provides a publish-subscribe mecanism to enable applications (subscribers) to request user account creation. OSIS Registration enable subscribers to poll an API endpoint in order for them to catch up on the last requested results.

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
cd osis_registration
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

`POST /create_account`

Create new user account creation request

> Body parameter

```json
{
  "uuid": "abcd-efgh-ijkl-mnop-1234-5678",
  "person_uuid": "abcd-efgh-ijkl-mnop-1234-5678",
  "first_name": "John",
  "last_name": "Doe",
  "birth_date": "1989-01-01",
  "email": "john.doe@mail.xyz"
}
```
-----

#### Poll

`GET /poll`

List last updated request results for a given subscriber

> Example response 200

```json
{
  "uuid": "abcd-efgh-ijkl-mnop-1234-5678",
  "person_uuid": "abcd-efgh-ijkl-mnop-1234-5678",
  "email": "john.doe@mail.xyz",
  "request_type": "CREATION",
  "status": "SUCCESS",
  "app": "internship",
  "updated_at": "2021-08-31T09:51:14.622461"
}
```
-------

#### Acknowledge

`PUT /acknowledge`

Update subscriber's last poll request to acknowledge poll has been sucessfully retrieved

> Body parameter

```json
{
  "last_poll_requested": "2021-08-31T09:51:14.622461"
}
```
------

## Espeak
For the sake of accessibility, an audio captcha file is read by synthetic voice. In order to generate this file, espeak has to be installed with english and french voices through the following commands:
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
