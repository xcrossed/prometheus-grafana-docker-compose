from celery import Celery
from celery.result import AsyncResult
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis import Redis

app = FastAPI()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')


class Task(BaseModel):
    task_id: str


class Result(BaseModel):
    result: str


@app.post('/tasks')
def create_task():
    task_id = celery_app.send_task('tasks.add', args=[1, 2])
    return {'task_id': task_id.id}


@app.get('/tasks/{task_id}')
def get_task(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.successful():
        return Result(result=result.result)
    elif result.failed():
        raise HTTPException(status_code=500, detail='Task failed')
    else:
        raise HTTPException(status_code=404, detail='Task not found')


if __name__ == '__main__':
    redis = Redis(host='localhost', port=6379, db=0)
    app.state.redis = redis
    app.state.celery_app = celery_app
    uvicorn.run(app, host='0.0.0.0', port=8000)
