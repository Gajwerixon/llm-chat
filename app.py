import gradio as gr
from ollama import chat
from chat_manager import ChatManager


manager = ChatManager()
manager.initialize_current_chat()


with gr.Blocks() as demo:

    # Conversation history in Ollama message format
    conversation = gr.State(manager.current_conversation)

    # Current model response
    assistant_response  = gr.State("")


    with gr.Row():
        user_input = gr.Textbox(
            placeholder="Ask about anything",
            show_label=False,
            elem_id="user-input"
        )

    chat_bot = gr.Chatbot(value=manager.get_chat_history())


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


    def add_assistant_message(conversation, output_state):
        conversation.append({
            "role": "assistant",
            "content": output_state
        })

        # Save data
        manager.save_chat(conversation)

        return conversation


    def clear_chat(conversation, assistant_response ):
        conversation = manager.clear_current_chat()
        assistant_response  = ""

        return conversation, assistant_response , []
        
    user_input.submit(
        user, 
        [user_input, conversation],
        [user_input, conversation],
        queue=False
    ).then(
        bot,
        conversation,
        [chat_bot, assistant_response ]
    ).then(
        add_assistant_message,
        [conversation, assistant_response ],
        conversation
    )

    clear_btn.click(
        clear_chat,
        [conversation, assistant_response ],
        [conversation, assistant_response , chat_bot]
    )

demo.launch()