# learning-authentication
Implementing the basic of multiple authorization strategies.  
Each strategy will include at least a client & server.  
Everything by terminal (no UI).  

Strategies:
- username password
    - Login by username and password
- email password
    - Login by email and password
    - Recover account through recovery code
- oauth
- passkey

We will use:
- [httpx](https://www.python-httpx.org/) to make http request
- [DuckDB](https://duckdb.org/) as database to store data
- [Starlette](https://www.starlette.io/) as RESTful API
- [aiosmtpd](https://aiosmtpd.aio-libs.org/en/latest/) as email server
