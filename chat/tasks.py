import time
from celery import Celery
import json

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def delete_idle_lobbies():
    with open('chat/static/lobbies.json', 'r+') as file:
        lobbies = json.load(file)
        current_time = time.time()

        for lobby_code, last_activity_time in lobbies.copy().items():
            if current_time - last_activity_time > 3600:
                del lobbies[lobby_code]  

        file.seek(0)
        json.dump(lobbies, file)
        file.truncate()

