from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
import threading
import time

loop_running = False

def loop_function(room):
    global loop_running
    i = 0
    while loop_running:
        i = i + 1
        # Esegui il codice del tuo loop qui
        # Ad esempio, invia dati al frontend tramite socket.emit()
        emit('status', {'msg': session.get('name') + ' loop ' + str(i)}, room=room)
        #socketio.emit('update', {'data': 'Nuovi dati dal backend'})
        time.sleep(1)

@socketio.on('start_loop', namespace='/chat')
def start_loop():
    global loop_running
    if not loop_running:
        loop_running = True
        room = session.get('room')
        join_room(room)
        # Avvia il loop in un thread separato
        threading.Thread(target=loop_function(room)).start()

@socketio.on('stop_loop', namespace='/chat')
def stop_loop():
    global loop_running
    loop_running = False

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

