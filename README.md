# learning-authentication
Implementing the basic of multiple authorization strategies.  

NOTE: I was organizing the repository but stopped middle way because I was tired of adding many ways of doing the same thing.

# strategies
- [username password](./username_password/README.md)
    - Login by username and password
    - Access private content
- [email password](./email_password/README.md)
    - Login by email and password
    - Access private content
    - Recover account through recovery code

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
