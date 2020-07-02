# Baserow introduction

## Architecture

Baserow consists of two main components:

1. The **backend** is a Python Django application that exposes a REST API. This is the
   core of Baserow and it does not have a user interface. The [API spec](./api.md) can 
   be found here. The persistent state is by default stored in a PostgreSQL database.
   MySQL and  SQLite are not supported at the moment, but will probably be in the
   future.
1. The **web frontend** is an application that serves as a user interface for the
   backend and is made in [NuxtJS](https://nuxtjs.org/) and 
   [Vue.js](https://vuejs.org/). It communicates to the backend via the REST API.
   
@TODO:
* Tell something about the handlers.
* Tell something about the api as a plugin.

## Backend

The backend consists of the **core**, **api** and **database** apps. The package also
contains base settings that can be extended. The REST API is written as a decoupled 
component which is not necessary to run Baserow. It is highly recommended though. The
same goes for the database app, this is written als a plugin for Baserow. Without it
you would only have the core which only has functionality like authentication, groups 
and some application abstraction.

## Web frontend

The web-frontend consists of the **core** and **database** modules. The package also 
contains some base config that can be extended. It is basically a user friendly shell 
around the backend that can run in your browser. It is made using 
[NuxtJS](https://nuxtjs.org/).

## Concepts

### Groups

A group can contain multiple applications. It can be used to define a company and in the
future it is going to be possible to invite extra users to a group. Every user in the 
group has access to all the applications within that group. Unfortunately it is not yet
possible  to add extra users because the live collaboration feature has to be 
implemented first.

### Applications

An application is more of an abstraction that be added to a group. By default the 
database plugin is included which contains the database application. Via the 
"create new" button in the sidebar a new application instance can be created for the 
selected group. Once you click on it you will see a context menu with all the 
application types. Plugins can introduce new application types.

### Database plugin

More information about the concepts of the database application can be found on the
[database plugin introduction page](./database-plugin.md).

## Environment variables

@TODO
