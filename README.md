# ustechsolution

Cricket App

## Getting Started

I have develop this project on python2.7 and django==1.1

### Prerequisites

clone this repo on your local

```
git clone https://github.com/string-maaz/ustechsolution.git
cd ustechsolution

```
create virtual enviroment and install requirements
```
virtualenv .pyenv
source .pyenv/bin/activate
pip install -r requirements.txt
```

### Installing

Run migrate to create db, and collectstatic file

```
python manage.py migrate
python manage.py collectstatic
```

And to initalize the database with some team

```
python manage.py initial_data
```



## Running the browser
```
hit - localhost:8000
```

### Note

I used bootstrap for frontend so import all the file of js in the project because its too much time taking to find out which js is will required or which not.
