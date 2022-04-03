
# TEXT TO IMAGE ENCRYPTION

In this project I implemented the text-to-image encryption. The main idea is to assgin a unic RGB value for every char that can be used to 
exchange the user's information across the network.

Cool thing about this project that the whole backend is being written from a scratch without using any popular frameworks like
Flask or Django. This exeperience helps to understand better the underlying processes of any web-framework.

## TODO List

- [x] Router class
- [x] key exchange endpoint
- [x] seed exchange endpoint
- [ ] add error handling for endpoints
- [ ] map creation endpoint
- [x] add resource path to the settings.py
- [ ] upgrade to WS endpoint
- [ ] start frontend
- [ ] modify exception handling in request_handler.py
- [ ] char-map initialization
- [x] handle requests for JS, CSS, and other http
- [x] fix http request parser (limited amount of chars)
