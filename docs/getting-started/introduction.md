# Baserow introduction

## Architecture

Baserow consists of two main components:

1. The **backend** is a Python Django application that exposes a REST API. This is the
   core of Baserow and it does not have a user interface. This [API spec](#) can be
   found here. The persistent state is by default stored in a PostgreSQL database.
   MySQL and  SQLite are not supported at the moment, but will probably be in the
   future.
1. The **web frontend** is an application that serves as a user interface for the
   backend and is made in [NuxtJS](https://nuxtjs.org/) and 
   [Vue.js](https://vuejs.org/). It communicates via the API with the backend.

## Backend

The backend consists of the **core**, **api** and **database** apps. The package also
contains base settings that can be extended. The REST API is written as a decoupled 
component which is not necessary to run Baserow. It is highly recommended though. The
same goes for the database app, this is written als a plugin for Baserow. Without it
you would only have the core which only has functionality like authentication, groups 
and some application abstraction.

## Web frontend
