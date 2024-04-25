# Routes Manager for FastAPI

Standardize and handle exceptions in [FastAPI](https://github.com/tiangolo/fastapi) more elegantly.

## Installation

```console
$ pip install fastapi-exceptionshandler
```


## Example

```python
from fastapi import FastAPI

from fastapi_exceptionshandler import APIExceptionMiddleware

app = FastAPI()

# Register the middleware
app.add_middleware(APIExceptionMiddleware, capture_unhandled=True)  # Capture all exceptions

# You can also capture Validation errors, that are not captured by default
from fastapi_exceptionshandler import APIExceptionHandler

from pydantic import ValidationError
app.add_exception_handler(ValidationError, APIExceptionHandler.unhandled)

from fastapi.exceptions import RequestValidationError
app.add_exception_handler(RequestValidationError, APIExceptionHandler.unhandled)

@app.get("/")
def read_root():
    return 1/0

```


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

In order to create a custom exception you need to extend `APIException` and `ErrorCodeBase` classes.

**Note:** if you want to capture *only* `APIException` then don't send the `capture_unhandled` param, or set it to `False`

```python
from fastapi import FastAPI

from fastapi_exceptionshandler import APIExceptionMiddleware, APIException, ErrorCodeBase

from starlette import status


app = FastAPI()

# Register the middleware
app.add_middleware(APIExceptionMiddleware)


class CustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    
    class ErrorCode(ErrorCodeBase):
        CustomExceptionCode = "Custom Exception Message", status.HTTP_401_UNAUTHORIZED
        CustomExceptionCodeWithDefaultStatusCode = "Custom Exception Message"
        
        
@app.get("/")
def read_root():
    raise CustomException(CustomException.ErrorCode.CustomExceptionCode)

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
