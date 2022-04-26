
# TEXT TO IMAGE ENCRYPTION

## Overview

A project for people who like to know how things work!
This project represents a basic implementation of the Text-to-Image encryption algorithm. Core concept of this algorithm
is to create RGB values for every printable. The Diffie–Hellman key exchange algorithm was used to exchange public keys 
between the clinet and the server.

Cool thing about this project is that the whole backend is being written from a scratch without using any popular frameworks like
Flask or Django. This exeperience helps to understand better the underlying processes of any web-framework.

## Quick Start

To run the project on your PC you need:

- Download the GIT repository.
- Create the virtual environmnet in the main repository:

```#!/bin/bash
    \$ python -m venv myvenv
```

- Activate virtual environmnet

```#!/bin/bash
    \$ /myvenv/Scripts/activate
```

- Install al the packages from the requirement.txt

```#!/bin/bash
    \$ pip install -r /requirements.txt
```

- Now you need to run the server, by using the driver file in the main repository

```#!/bin/bash
    \$ python server_driver.py
```

- The last step is going to be to navigate to the: 'http://127.0.0.1:5050/index'

## Main Concepts

The key idea of this projects is to encode a text message into an image. In our case we encode text into .png image and 
send it through the network in base64 format.

Below you can find 3 main states of a message:

- Plain Text
![plaint_text](/readme_res/first_phase_text.png)

## TODO List

- [x] Router class
- [x] key exchange endpoint
- [x] seed exchange endpoint
- [ ] add error handling for endpoints
- [x] map creation endpoint
- [x] add resource path to the settings.py
- [ ] modify exception handling in request_handler.py
- [x] char-map initialization
- [x] handle requests for JS, CSS, and other http
- [x] fix http request parser (limited amount of chars)
- [ ] fix doubling connections from the 'refresh' button
- [x] upgrade to WS endpoint
