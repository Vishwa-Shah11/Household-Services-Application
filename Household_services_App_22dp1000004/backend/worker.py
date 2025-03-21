from celery import Celery, Task
from flask import Flask


def celery_init_app(app: Flask, CeleryConfig):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    cel_app = Celery(app.name, task_cls=FlaskTask)
    cel_app.config_from_object(CeleryConfig)
    cel_app.set_default()
    app.extensions["celery"] = cel_app
    return cel_app