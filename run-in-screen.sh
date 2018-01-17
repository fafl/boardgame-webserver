# Start in screen with name and keep it open after server terminates
screen -dm -S boardgame-webserver sh -c 'python server.py; read x'

# Show running screns
screen -ls
