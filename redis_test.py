import redis

r = redis.StrictRedis(host='localhost', port=6379)
p = r.pubsub()
p.subscribe('game_action')

while True:
    message = p.get_message()
    if message:
        command = message['data']
        if isinstance(command, (bytes, bytearray)):
            command = str(command, "utf-8")
            print(command)
            if command == "Left":
                print("left")
            if command == "Right":
                print("right")
            if command == "S Down":
                print("down")
            if command == "Rot L":
                print("rotL")
            if command == "Rot R":
                print("rotR")
            if command == "H Down":
                print("full down")