# AirBnB Clone v3 - RESTful API

## Description
This is the third version of the AirBnB clone project, which is a simple copy of the AirBnB website. This project is a RESTful API that interacts with a MySQL database. The API allows users to create, update, delete, and view users, places, cities, states, and amenities. The API also allows users to view the status of the API and retrieve the number of each object in the database.

## API Endpoints
The API has the following endpoints:

### Status
- `GET /status`: Retrieves the status of the API.
- `GET /status`: Retrieves the number of each object in the database.
- `GET /status/<object>`: Retrieves the number of a specific object in the database.

### Users


### Places


### Cities
- `GET /states/<state_id>/cities`: Retrieves all cities in a specific state.
- `GET /cities/<city_id>`: Retrieves a specific city.
- `DELETE /cities/<city_id>`: Deletes a specific city.
- `POST /cities`: Creates a new city.
- `PUT /cities/<city_id>`: Updates a specific city.


### States
- `GET /states`: Retrieves all states.
- `GET /states/<state_id>`: Retrieves a specific state.
- `DELETE /states/<state_id>`: Deletes a specific state.
- `POST /states`: Creates a new state.
- `PUT /states/<state_id>`: Updates a specific state.


### Amenities


## Requirements


## Installation


## Usage


## Authors


