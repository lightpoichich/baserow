## Testing

In order to test your changes, you need to have the Heroku command line installed on
your local machine. Next, you can use the Heroku command line to create an app,
manually install the `addons` and `labs` listed in the app.json file at the root of
this repo. In the example below we assume you are at the root of the Baserow repo and
we are going install a heroku app named `baserow-test-app`, this can of course be named
differently.

```
$ heroku apps:create baserow-test-app
$ heroku stack:set -a baserow-test-app container

# We need to add all the addons listed in the app.json file.
$ heroku addons:create -a baserow-test-app heroku-postgresql:hobby-dev
$ heroku addons:create -a baserow-test-app heroku-redis:hobby-dev
$ heroku addons:create -a baserow-test-app mailgun:starter

# We need to add all the labs listed in the app.json file.
$ heroku labs:enable -a baserow-test-app runtime-dyno-metadata

# Finally we need to set all the environment variables listed in the app.json file.
$ heroku config:set -a baserow-test-app SECRET_KEY=REPLACE_WITH_SECRET_VALUE
$ heroku config:set -a baserow-test-app BASEROW_PUBLIC_URL=
$ heroku config:set -a baserow-test-app BASEROW_AMOUNT_OF_WORKERS=1
```

Now that we have replicated the setup of the app.json, we can deploy the application
by pushing to the heroku remote repository.

```
$ git remote add heroku https://git.heroku.com/baserow-test-app.git
$ git push heroku YOUR_CURRENT_BRANCH:master
```
