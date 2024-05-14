
from fastapi import WebSocket
from jinja2 import Environment, FileSystemLoader
import time
import logging
logging.basicConfig(filename='chat.log', filemode='w+', level=logging.INFO)
_logger = logging.getLogger('chat_app')
_logger.setLevel(logging.INFO)



from chat_generator import response_generator

env = Environment(loader=FileSystemLoader('templates'))
history_template = env.get_template("chat_history.html")
stream_template = env.get_template("chat_stream.html")

session_state = {}

# Initialize chat history
if "messages" not in session_state:
    session_state['messages'] = []



async def response_generator_helper(user_message:str):
    full_text = ""
    stream_generator = response_generator(user_message)
    for stream_text in stream_generator:
        if stream_text is None:
            continue
        full_text += stream_text
        
        stream_html = stream_template.render(current_stream = full_text)

        yield stream_html


async def handle_websocket_stream(websocket: WebSocket, user_message: str):

    
    async for stream_html in response_generator_helper(user_message):
        await websocket.send_text(stream_html)

    return stream_html
    


async def handle_websocket_chat(websocket: WebSocket):

    await websocket.accept()
    while True:
        
        
        user_message = await websocket.receive_json()
        #print(f"got data: {str(user_message)}")
        session_state["messages"].append({"role": "user", "content": user_message["chat_message"]})
        chat_history = history_template.render(prev_messages=session_state["messages"])
        #print(chat_history)
        await websocket.send_text(chat_history)

        start = time.time()
        stream_html = await handle_websocket_stream(websocket, user_message["chat_message"])
        end = time.time()
        _logger.info(f"Total Time: {end-start}")

        session_state["messages"].append({"role": "system", "content": stream_html})
        