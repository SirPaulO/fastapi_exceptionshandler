# Routes Manager for FastAPI

Standardize and handle exceptions in [FastAPI](https://github.com/tiangolo/fastapi) more elegantly.

## Installation

```console
$ pip install fastapi-exceptionshandler
```


## Example

You can automatically handle **all** exceptions using [fastapi-routesmanager](https://github.com/SirPaulO/fastapi_routesmanager).
Simply register the `APIExceptionManager` to the `RouteManagersRegistry`. _Don't forget to use the `ManagedAPIRouter`_

**Note:** by default Validation errors are not captured. To do so, use `APIExceptionManager(capture_validation=True)` instead.

```python
from fastapi import FastAPI

from fastapi_routesmanager import RouteManagersRegistry, ManagedAPIRouter

from fastapi_exceptionshandler import APIExceptionManager

RouteManagersRegistry.register_route_manager(APIExceptionManager)  # Register manager

app = FastAPI()

router = ManagedAPIRouter()

@router.get("/")  # Use router instead of app
def read_root():
    return 1/0


app.include_router(router)  # Include the router to the app

```

<details>
<summary>Or you can handle exceptions manually...</summary>

```python
from fastapi import FastAPI

from fastapi_exceptionshandler import APIExceptionHandler

app = FastAPI()

@app.get("/")
def read_root():
    try:
        return 1/0
    except Exception as exc:
        return await APIExceptionHandler.unhandled(exc)

```
</details>


Create a custom exception class and error code, then 

### Run it

```console
$ uvicorn main:app --reload
```

### Check it

Browse to http://127.0.0.1:8000 you should see this json:

```console
{"errorCode": "InternalError", "message": "Internal Server Error"}
```

## Creating custom exceptions

In order to create a custom exception you need to extend `APIException` and create an `Enum` class.

**Note:** if you want to capture *only* `APIException` then use `APIExceptionManager(capture_unhandled=False)`

```python
from enum import Enum

from fastapi import FastAPI

from fastapi_routesmanager import RouteManagersRegistry, ManagedAPIRouter

from fastapi_exceptionshandler import APIExceptionManager, APIException

RouteManagersRegistry.register_route_manager(APIExceptionManager)  # Register manager

app = FastAPI()

router = ManagedAPIRouter()


class CustomException(APIException):
    status_code = 401
    
    class ErrorCode(Enum):
        CustomExceptionCode = "Custom Exception Message"


@router.get("/")  # Use router instead of app
def read_root():
    raise CustomException(CustomException.ErrorCode.CustomExceptionCode)


app.include_router(router)  # Include the router to the app

```

Then you should get a `401` response with this body

```console
{"errorCode": "CustomExceptionCode", "message": "Custom Exception Message"}
```

<details>
<summary>Or you can handle exceptions manually...</summary>

```python
@app.get("/")
def read_root():
    try:
        raise CustomException(CustomException.ErrorCode.CustomExceptionCode)
    except APIException as exc:
        return await APIExceptionHandler.handled(exc)
    except Exception as exc:  # Handle all exceptions
        return await APIExceptionHandler.unhandled(exc)

```
</details>


**Note:** The `ErrorCode` class doesn't need to be inside `CustomException` and can be shared with another exceptions as well.
