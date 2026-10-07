import json
from pathlib import Path

import gradio as gr
from ollama import chat
from chat_manager import ChatManager


manager = ChatManager()
manager.initialize_current_chat()


with gr.Blocks() as demo:

    # Conversation history in Ollama message format
    conversation = gr.State(manager.current_conversation)

    # Current model response.
    chat_output_state = gr.State("")


    with gr.Row():
        user_input = gr.Textbox(
            placeholder="Ask about anything",
            show_label=False,
            elem_id="user-input"
        )

    chat_bot = gr.Chatbot(value=manager.chat_history)


    with gr.Row():
        clear_btn = gr.Button(value="Clear chat")


    with gr.Row():
        new_chat_btn = gr.Button(value="New chat")


    def user(user_input, conversation):
        conversation.append({"role": "user", "content": user_input})
        return "", conversation


    def bot(conversation):
        response = chat(
            model="gemma3:4b", 
            messages=conversation, 
            stream=True
        )

        chat_output = ""
        for chunk in response:
            chat_output += chunk.message.content
            conversation_temp = conversation + [
                {"role": "assistant", "content": chat_output}
            ]
            yield conversation_temp, chat_output


    def update_conversation(conversation, output_state):
        conversation.append({
            "role": "assistant",
            "content": output_state
        })

        # Save data
        manager.add_assistant_message(conversation)

        return conversation


    def clear_chat(conversation, chat_output_state):
        conversation = manager.clear_current_chat()
        chat_output_state = ""

        return conversation, chat_output_state, []
        
    user_input.submit(
        user, 
        [user_input, conversation],
        [user_input, conversation],
        queue=False
    ).then(
        bot,
        conversation,
        [chat_bot, chat_output_state]
    ).then(
        update_conversation,
        [conversation, chat_output_state],
        conversation
    )

    clear_btn.click(
        clear_chat,
        [conversation, chat_output_state],
        [conversation, chat_output_state, chat_bot]
    )

demo.launch()