# simple web site with flask

>! i used flask_login to authorization and it so easy to learn you can search for YouTube for flask-login tutorials





> its not for production but only for leorning purposes
> if you want to run it in you local machine you need to 
> follow the steps below


## Installing Dependencies
>[!] Python-3.9.5 (recommended)

### Virtual Environment

```bash

cd project_directory
pip install venv
python -m venv venv
source venv/Script/active

```

### PIP Dependecies
> Once you have your **venv** setup and running, install dependencies by navigating
> to the root directory and running:
```bash
pip install -r requirements.txt
```
>This will install all of the required packages included in the requirements.txt
>file.

### Exporting ENV VARIABES form setup.sh file
>`You mus change database ulr in setup.sh file`
```bash
source setup.sh
```

## Runing the Server
> From within the root directory, first ensure you're working with your created
venv. To run the server, execute the following:
```bash

flask run

```
> Setting the FLASK_ENV variable to development will detect file changes and
> restart the server automatically.
> Setting the FLASK_APP variable to agency directs Flask to use
