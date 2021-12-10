# api-swagger-flask

### Prerequisites

    ~ Python 3.7 or above

###Install Swagger UI:

    ~ pip Install flask_swagger_ui

### How to test

    ~ Run pip install -r requirements.txt
    ~ Then on your project directory run flusk run


### Features 
    ~ It takes any or all parameters from query string like house name,sleeps,
    bedrooms,bathrooms,price,location and gives api data.
    ~ For authentication you have to login where password is "smartboy".
    ~ To generate a JWT token visit http://127.0.0.1:5000/ or 
    http://127.0.0.1:5000/login and give password.
    ~ Then visit http://127.0.0.1:5000/protected?token="JWT Token".It will 
    redirect to api.
    ~ Then api interface will take parameter and response data if available 
    sorted by Bedrooms.
