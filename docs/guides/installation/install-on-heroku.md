# Installation on Heroku

> The Heroku template and one click to deploy button are currently in beta.

Heroku is a platform as a service that enables developer to build, run and operate
applications entirely in the cloud. We have created a template that allows you to
easily install Baserow on the free plan of Heroku. You can also scale up by tweaking
some settings

## The template

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/bram2w/baserow/tree/master)
*Beta*

The button above can be used to install Baserow on Heroku with one click. Click on it
and follow the steps on heroku.com to proceed. After the installation, you can reach
Baserow on the URL provided by Heroku. Everything installed via the template runs on
the free plan of Heroku by default.

## Could not connect to the API server error

If you are getting a "Could not connect to the API server." error when logging in or
creating an account, then you most likely need to update the `BASEROW_PUBLIC_URL`
config var. You can do so by going to the settings page in your Heroku app dashboard,
click on "Reveal Config Vars", find the `BASEROW_PUBLIC_URL` and change the value to 
`https://YOUR_APP_NAME.herokuapp.com`. Don't forget to replace `YOUR_APP_NAME` with the
name of your app.

## Persistent S3 file storage

By default, the uploaded files are stored inside the dyno for demo purposes. This means
that everytime your dyno restarts, you will lose all your uploaded files. Your files
can optionally be stored inside an S3 bucket. To do so, you need to add a couple of
config vars to the settings. Go to the Settings page and click on "Reveal Config Vars".
Here you need to add the following vars:

* AWS_ACCESS_KEY_ID: The access key for your AWS account.
* AWS_SECRET_ACCESS_KEY: The secret key for your AWS account.
* AWS_STORAGE_BUCKET_NAME: Your Amazon Web Services storage bucket name.
* AWS_S3_REGION_NAME *Optional*: Name of the AWS S3 region to use (eg. eu-west-1)
* AWS_S3_ENDPOINT_URL *Optional*: Custom S3 URL to use when connecting to S3, including
  scheme.
* AWS_S3_CUSTOM_DOMAIN *Optional*: Your custom domain where the files can be downloaded
  from.

### Non AWS S3 providers

It is also possible to use non AWS, S3 providers like for example Digital Ocean. Below
you will find example settings if you want to connect to Digital Ocean Spaces.

* AWS_ACCESS_KEY_ID: The spaces API key.
* AWS_SECRET_ACCESS_KEY: The spaces API secret key.
* AWS_STORAGE_BUCKET_NAME: The name of your space.
* AWS_S3_REGION_NAME: Name of the Digital Ocean spaces region (eg. ams3)
* AWS_S3_ENDPOINT_URL: (eg. https://ams3.digitaloceanspaces.com)
* AWS_S3_CUSTOM_DOMAIN: (eg. name-of-your-space.ams3.digitaloceanspaces.com)

## Scaling

Even though the template runs on the free plan of Heroku by default, it can easily be
scaled up to fit your needs. We recommend scaling up if you are going to use Baserow
with more than one user simultaneously. You can scale up by changing the dyno type
and increase the amount of dyno's.

### Workers per dyno

To spare resources, every dyno has only one worker by default. If you are upgrading to
a standard 2x dyno, you can increase the amount of workers to 2. This can be done  via
the Config Vars in the Settings. On the settings page, click on "Reveal Config Vars",
find the "BASEROW_AMOUNT_OF_WORKERS" var and set the value to 2.

You can roughly estimate the amount of workers based on the available RAM of your
dyno type. Every worker needs around 512MB ram, so a standard x1 dyno should have one
worker, a standard x2 can have 2 workers and a performance M can have 4.

### Postgres

By default, we are using the `heroku-postgresql:hobby-dev` addon because that supports
10k rows for free. If you need more rows, you need to upgrade that addon.

### Redis

By default, we are using the `heroku-redis:hobby` addon because that addon supports
20 connections for free. If you are scaling up, you need more connections which means
you need to upgrade that addon. In order to roughly estimate how many connections you
would need, you can do DYNO COUNT * BASEROW_AMOUNT_OF_WORKERS * 15.

## Custom Domain

If you added a custom domain, then you need to change a Config Var on the settings
page. Go to the Settings page and click on "Reveal Config Vars". Here you need to set
the `BASEROW_PUBLIC_URL` value and add your own URL. If your domain is 
`baserow-test.com` ,then the value should be `https://baserow-test.com`. If you don't 
have a custom domain then this value can be empty.

## Environment variables

* SECRET_KEY: A unique string that is used to generate secrets.
* BASEROW_PUBLIC_URL: The public URL of your Heroku Baserow app. If empty, the default
  Heroku app URL is used, but if it differs it must be changed.
  (eg. https://baserow-test.com).
* BASEROW_AMOUNT_OF_WORKERS: The amount of workers per dyno.
* AWS_ACCESS_KEY_ID: The spaces API key.
* AWS_SECRET_ACCESS_KEY: The spaces API secret key.
* AWS_STORAGE_BUCKET_NAME: The name of your space.
* AWS_S3_REGION_NAME: Name of the Digital Ocean spaces region (eg. ams3)
* AWS_S3_ENDPOINT_URL: Custom S3 URL to use when connecting to S3, including scheme.
* AWS_S3_CUSTOM_DOMAIN: Your custom domain where the files can be downloaded from.

## Update

When a new version of Baserow has been released, you probably want to update.
Unfortunately, it is not possible to update from a public repository via the web
interface, so you need to do that via the command line. If don't have the
heroku-cli installed, you can follow the instructions here 
https://devcenter.heroku.com/articles/heroku-cli. After the cli is installed, you
probably need to run `heroku login` to authenticate with your account.

Make sure that you navigate to an empty directory and then run the commands below.
Don't forgot to replace `YOUR_APP_NAME` with the name of your Heroku app.

```
$ git clone --branch master https://gitlab.com/bramw/baserow.git
$ cd baserow
$ git remote add heroku https://git.heroku.com/YOUR_APP_NAME.git
$ git push -f heroku master
```

The latest version is deployed after the command finishes. You can optionally cleanup
the created directory by executing the following commands.

```
$ cd ../
$ rm -rf baserow
```
