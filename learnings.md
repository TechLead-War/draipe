contexts are of 3 types 
1. application context ("g"(global variable), current_app)
2. request context (request object, session object)
Both of these contexts are available in Sanic using the app.ctx and request.ctx properties, respectively.


session 
 - is also a dict
 - import from sanic like request.
 - then, in functions, session["hi"] = "hello"

request decorators
 - @app.before_request  -> executes before every request
 - @app.before_first_request  -> only for first request
 - @app.after_request   -> only after get request gets an exception
 - @app.teardown_request  ->  after each request, even if excption occurs

any folder with __init__ py, treats it as a package



how to verify if user is logged in.
1. session based. (request will have a unique id)
2. token based(JWT), check if this is valid token.


Signals in Tortoise ORM are a way to execute certain actions automatically when specific events occur in the database. These events can be anything from creating a new record to updating or deleting an existing one.

Some examples of signals in Tortoise ORM are:

1. Pre-save signal: This signal is triggered just before a record is saved to the database. It can be used to perform any necessary validation or modification of the data before it is saved.

2. Post-save signal: This signal is triggered after a record has been saved to the database. It can be used to perform any additional actions that need to be taken after the record has been saved, such as sending notifications or updating related records.

3. Pre-delete signal: This signal is triggered just before a record is deleted from the database. It can be used to perform any necessary checks or modifications before the record is deleted.

4. Post-delete signal: This signal is triggered after a record has been deleted from the database. It can be used to perform any additional actions that need to be taken after the record has been deleted, such as cleaning up related records or sending notifications.

5. Pre-update signal: This signal is triggered just before a record is updated in the database. It can be used to perform any necessary validation or modification of the data before it is updated.

6. Post-update signal: This signal is triggered after a record has been updated in the database. It can be used to perform any additional actions that need to be taken after the record has been updated, such as sending notifications or updating related records.