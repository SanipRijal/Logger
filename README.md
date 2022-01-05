======================
Eightlab Django Logger
======================


Eightlab Django Logger is a Django app to help simplify the logging activities.
It creates log files for access, error, exception and info. 

Dashboard
---------

The Eightlab Django Logger Dashboard helps in viewing detailed error statuses.

Email
-----

The Eightlab Django Logger can also be configured to send email to recipients when exceptions occur.


Quick start
-----------

1. Add "eight_logger" to your INSTALLED_APPS setting:

    INSTALLED_APPS = [
        ...
        'eight_logger',
        ...
    ]

2. Include the polls URLConf in your project urls.py like:
    
    path('eight_logger/', include('eight_logger.urls')),

3. Run `python manage.py migrate` to create eight_logger models.
