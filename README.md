# notify-frontend [ALPHA]

Part of [GOV.UK Notify](https://gds.blog.gov.uk/2015/10/05/status-tracking-making-it-easy-to-keep-users-informed/)

Frontend app for the [Notify API](https://github.com/alphagov/notify-api)

Python app, based on the [Flask framework](http://flask.pocoo.org/)

## Setup

Install [Virtualenv](https://virtualenv.pypa.io/en/latest/)
```
sudo easy_install virtualenv
```

In the app folder, create a virtual environment
```
virtualenv ./venv
```

Activate the virtual environment
```
source ./venv/bin/activate
```

### Set the required environment variables

You need to run these commands every time you restart your terminal window -- this includes new terminal tabs and panes. To avoid this, you can [add environment variables](http://lmgtfy.com/?q=add+environment+variables+mac)

To use your local API instance:
```
export DM_DATA_API_URL=http://localhost:5000
export DM_DATA_API_AUTH_TOKEN=<bearer_token>
```

To use the test instance on heroku:
```
export NOTIFY_API_URL=https://test-notify-api.herokuapp.com/
export NOTIFY_DATA_API_AUTH_TOKEN=<bearer_token>
```

### Upgrade dependencies

Install new Python dependencies with pip
```
pip install -r requirements_for_test.txt
```

Install frontend dependencies with npm and gulp
```
npm install
```

### Compile the front-end code

For development usage:
```
npm run frontend-build:development
```

For production:
```
npm run frontend-build:production
```

### Compiling the front-end whenever it changes
```
npm run frontend-build:watch
```

### Run the tests

```
./scripts/run_tests.sh
```

### Run the server

To run the Admin Frontend App for local development you can use the convenient run
script, which sets the required environment variables to defaults if they have
not already been set:

```
./scripts/run_app.sh
```

More generally, the command to start the server is:
```
python application.py runserver
```

The admin frontend runs on port 5004. Use the app at [http://127.0.0.1:5004/](http://127.0.0.1:5004/)

### Using FeatureFlags

To use feature flags, check out the documentation in (the README of)
[digitalmarketplace-utils](https://github.com/alphagov/digitalmarketplace-utils#using-featureflags).

## Frontend tasks

[NPM](https://www.npmjs.org/) is used for all frontend build tasks. The commands available are:

- `npm run frontend-build:development` (compile the frontend files for development)
- `npm run frontend-build:production` (compile the frontend files for production)
- `npm run frontend-build:watch` (watch all frontend files & rebuild when anything changes)
- `npm run frontend-install` (install all non-NPM dependancies)

Note: `npm run frontend-install` is run as a post-install task after you run `npm install`.

## Cheatsheet

```
source ./venv/bin/activate
```
```
export DM_DATA_API_URL=http://localhost:5000
export DM_DATA_API_AUTH_TOKEN=<bearer_token>
```
or
```
export NOTIFY_API_URL=https://test-notify-api.herokuapp.com/
export NOTIFY_DATA_API_AUTH_TOKEN=<bearer_token>
```
```
pip install -r requirements_for_test.txt
npm install
npm run frontend-build:watch
./scripts/run_app.sh


See API and API Client repos for more information```
