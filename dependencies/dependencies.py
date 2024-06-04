from typing import Annotated

from fastapi import Depends, FastAPI, Form
from typing import Union

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

# class dependencies
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/class_dependencies/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

# sub dependencies
def query_extractor(q: str | None = None):
    return q


def query_or_form_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Form()] = None,
):
    if not q:
        return last_query
    return q

def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_or_form_extractor)],
    last_query_2: Annotated[str | None, Form()] = None,
):
    if not q:
        return last_query_2
    return q

@app.get("/items/sub_dependencies/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}