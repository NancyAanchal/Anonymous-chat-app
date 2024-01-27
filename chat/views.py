from django.shortcuts import render
import random, string
import json


def index(request):
    return render(request, 'chat/index.html')


def lobby(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        lobby_code = request.POST.get('lobbycode')

        #checking if lobby code exists
        f=open("chat/static/lobbies.json")
        lobbies=json.load(f)
        f.close()

        if lobby_code not in lobbies:
            return render(request, 'chat/index.html', {'message':'Lobby does not exist. Please check your lobby code.'})

    return render(request, 'chat/lobby.html', {'user_name': name, 'lobbycode':lobby_code, 'room_name':lobbies[lobby_code]})


def create_lobby(request):
    if request.method == 'POST':
        lobby_name = request.POST.get('lobby_name')
        
        f=open("chat/static/lobbies.json")
        lobbies=json.load(f)
        f.close()

        while True:
            lobby_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            if lobby_code not in lobbies:
                break
        
        lobbies.update({lobby_code:lobby_name})
        with open("chat/static/lobbies.json","w") as file:
            json.dump(lobbies, file)
        
        return render(request, 'chat/create_lobby.html',{'lobby_code': lobby_code})
    
    return render(request, 'chat/create_lobby.html')