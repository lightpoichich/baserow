# Development tools

## Backend

### PostgreSQL

By default Baserow uses PostgreSQL for persistent storage. In the near future MySQL and 
SQLite are also going to by supported, but this is not yet the case. Most things will
probably work with the other engines, but it will probably fail when converting a field
to another type. Haven't tested if the other engines work though.

https://www.postgresql.org/

### Django

https://www.djangoproject.com

### Django REST framework

https://www.django-rest-framework.org/

### pytest

To easily and automatically test all the python code we use pytest. Most of the backend
code is covered with tests and we like to keep it that way! The code is also tested
in the continuous integration pipline. It can also be tested manually in the development
environment. Make sure that you are in the `backend` container and execute the following
command.

```
$ make test
```

https://docs.pytest.org/en/latest/contents.html

### Flake8

Flake8 makes it easy to enforce our python code style. The code is checked in the 
continuous integration pipeline. It can also by checked manually in the development
environment. Make sure that you are in the `backend` container and execute the 
following command. If all code meets the standards you should not see any output.

```
$ make lint
```

https://flake8.pycqa.org/en/latest/

### ItsDangerous

In order to safely share sensitive data like password reset tokens we use the proven
ItsDangerous library.

https://itsdangerous.palletsprojects.com/en/1.1.x/

### DRF spectacular

Having up to date API documentation and having it in the OpenAPI specification format 
is a must. To avoid mistakes the contents are close to the code and are automated as 
much as possible. DRF Spectacular could offer all this!

https://pypi.org/project/drf-spectacular/

### MJML

In order to simplify the process of creating HTML emails we use MJML. This tool makes
it easy to create responsive emails that work with most email clients. This might seem
like a bit of over engineering to use this for only the password forgot email, but more
complicated emails are going to be added in the future and we wanted to have a solid 
base. To make this integrate very nicely with Django templates we use the liminispace
django package.

https://mjml.io/
https://github.com/liminspace/django-mjml

## Web frontend

### Vue.js

https://vuejs.org/

### Nuxt.js

https://nuxtjs.org/

### Stylelint

https://stylelint.io/

### ESLint

https://eslint.org/

### Prettier

https://prettier.io/

### Webpack

https://webpack.js.org/

### SCSS

https://sass-lang.com/

### JEST

https://jestjs.io/

### Font Awesome 5

https://fontawesome.com/
