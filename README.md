# Virtual Data Room Platform to Cloud Storage Integration

This web app has been created as a proof of concept for of a common integration use-case in the LegalTech world.
Virtual Data Rooms commonly facilitate M&A Transactions and VDR Platforms can allow Law Firms to run many transactions
at once, all managed from a single SaaS Platform. 

## Imagined use case

This app assumes that there is a remote VDR service which contains many sites (i.e Data Rooms!). It provides a basic dashboard
for searching and viewing metadata associated with these sites. Individual sites can be viewed in detail and from there, the remote system's
REST API can be leveraged to download the file & folder structures of these sites onto the server this app is running on, as well as an
object storage repository like AWS S3.

VDR Platforms generally charge by the amount of data stored, so an integration which can provide efficient transfer out of the system, 
is a valuable tool for system administrators. 

The individual data rooms can also be 'soft' (i.e recycle bin) deleted or even 'hard' (irretrievably) deleted, 

## Technologies Used

- [Django](https://www.djangoproject.com/)
- [Django AllAuth](https://django-allauth.readthedocs.io/en/latest/overview.html)
  - Allows us to use the remote VDR system to provide authentication. 
- [Pydantic](https://pydantic-docs.helpmanual.io/)
  - Gives a much cleaner interface for the data transfer object. Also provides validation on fields. 
- [Pytest](https://docs.pytest.org/)
  - Easy monkey-patching and mocking is perfect for testing an app reliant on network calls to a 3rd party service
- [Celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html)
  - We expect some 'jobs' to be long running. This allows us to define them as Tasks and push to a background worker.
- [Django-Solo](https://github.com/lazybird/django-solo)
  - Settings can be defined by users in an admin interface. This allows us to do so as a Singleton object. 
  - [Memcached](https://memcached.org/)
    - Caching the settings, for as fast as possible access. 
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
  - For interacting with the S3 functionality. 
- [Bottle](https://bottlepy.org/docs/dev/)
  - API Proxy between Django App and remote system
  - [PyPy](https://www.pypy.org/)
  - [Gunicorn](https://docs.gunicorn.org/en/stable/index.html)
    - PyPy and Gunicorn Async workers to improve throughput for the API Proxy. 


## Screenshots
![Data Room List](https://user-images.githubusercontent.com/40800258/153038124-897fd7e2-948d-4525-8ab3-adf2f56863c0.png)
![Data Room Detail](https://user-images.githubusercontent.com/40800258/153038126-feba6ee7-af5d-43bc-b3b8-c30b5b98d163.png)
![Task Buttons](https://user-images.githubusercontent.com/40800258/153038128-7ab8f1d8-07f3-4a19-81f0-0239b853583b.png)
![Polling the Celery Progress](https://user-images.githubusercontent.com/40800258/153038135-dea8c4e0-5208-4e6b-b990-d76bd11b1d7f.png)
![Reporting on the Background Jobs](https://user-images.githubusercontent.com/40800258/153038129-ceec0a45-e6a9-4601-945e-a4911f392a13.png)
![Report Details](https://user-images.githubusercontent.com/40800258/153038133-3bd00afd-2387-4dc1-9334-ec23afc0b649.png)
![Settings](https://user-images.githubusercontent.com/40800258/153038134-ad9e2e3f-4321-4282-b736-c8fdf0b4bc97.png)

## Warning about the endpoints
This repository is for demo purposes only! I would advise against trying to run it, as the requests to the remote system urls
are 'sort of' fake. I've deliberately obfuscated them, as I dont want to reveal the endpoints of the company I work for's API. 
When running in my local, I have an api proxy written in Bottle forwarding the requests to the 'real' service (not checked into
version control). Post about it [HERE](https://petersimpson.dev/blog/building-an-api-proxy-with-bottle/).
Having said that, if the purpose of each endpoint is clear to you and could easily 'map' onto a system you are familiar with,
feel free to write your own proxy service! 

## ToDo
 - Only really considers the 'happy path': improve error handling. 
 - Research more efficient algorithms for file-deletion (reverse level order traversal?). 
 - More Tests. More Integration in tests.
 - Get Memcached to play more nicely with Django-Solo. 
 - Bug where the 'Site Copy' returns success message too early. 
 - Improve the interface (add more filtering and ordering options). 

