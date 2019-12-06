# Fill in the blanks solver

  
This is a project to answer fill in the blanks questions by extracting the image of a question with Google Vision API and converting to text, it tries to solve the question using word2vec using the model provided by Google News.

### Input Image

![Input image](https://github.com/ufrpe-mineracao-textos/projeto-de-mineracao-20192-rockboyz/raw/master/images/015.png)

### Output


## Install

 *This project requires Python 3*

* Clone this repo
`` git clone https://github.com/ufrpe-mineracao-textos/projeto-de-mineracao-20192-rockboyz.git``
* Install all the dependencies
`` pip3 install -r requirements.txt ``
* Change to the backend directory
 ``cd backend/``

### Setting up Google Vision

This project requires a Google Account to parse the image to text [follow these steps](https://cloud.google.com/docs/authentication/api-keys?hl=en&visit_id=637111981987631327-3133425640&rd=1) to setup an authentication key, the key will look like this:

    {
    "type": "service_account",
    "project_id": "livox-2323131",
    "private_key_id": "4018172b5ed0f709b036e1606ca9701806a1efad",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBmC0\n3IY9FhsvFU87qRB=\n-----END PRIVATE KEY-----\n",
    "client_email": "vision@project",
    "client_id": "XXXXX",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/vision%40livox-1492702205991.iam.gserviceaccount.com"
    }

Save this file as `credentials.json` and insert in you backend folder.


### Getting the model

Last, download the Google Vision model inside the `backend/` folder:

``wget https://github.com/eyaler/word2vec-slim/raw/master/GoogleNews-vectors-negative300-SLIM.bin.gz``

### Running the server

After setting up the model and the Google auth key run the server with the following command:

``python3 manage.py runserver 0.0.0.0:8000``

Navigate to ``http://localhost:8000/`` and you are all set!

## Developing new strategies

The core of application lives inside ``backend/questions/views.py`` there are functions to parse the image to text.

The function being called to try to process the correct answer is called `best_probability`, the input is a `question` dict like this:

    question = {
	    "text": "While in reality Alpha Centauri is a triple star, _ to the naked eye to be a single star.",
	    "options": ["it appears","but it appears","appears","despite it"]
    }

The answer to this function must be the correct alternative ("A").