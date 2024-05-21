# learning-authentication
Implementing the basic of multiple authorization strategies.  
Everything by terminal (no UI).  

# strategies
- username password
    - Login by username and password
- email password
    - Login by email and password
    - Recover account through recovery code
- oauth
- passkey

# tools
- [httpx](https://www.python-httpx.org/) to make http request
- [DuckDB](https://duckdb.org/) as local database
- [Starlette](https://www.starlette.io/) as RESTful API
- [aiosmtpd](https://aiosmtpd.aio-libs.org/en/latest/) as email server

# references
- https://www.youtube.com/watch?v=996OiexHze0
- https://www.youtube.com/watch?v=IThLjsDUG0g
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type