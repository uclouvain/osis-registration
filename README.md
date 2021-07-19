# osis-registration
OSIS Registration is a django application to handle external account management

Espeak
------
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