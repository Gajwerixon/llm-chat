import gradio as gr
from ollama import chat
from chat_manager import ChatManager


manager = ChatManager()
manager.initialize_current_chat()


with gr.Blocks() as demo:

    conversation = gr.State(manager.current_conversation)

    assistant_response  = gr.State("")


    with gr.Row():
        user_input = gr.Textbox(
            placeholder="Ask about anything",
            show_label=False,
            elem_id="user-input"
        )


    chat_bot = gr.Chatbot(value=manager.get_chat_history())


    with gr.Row():
        new_chat_btn = gr.Button(value="New chat")


    # Create radio menu with chats
    chat_selector = gr.Radio(
        choices=[
            f"Chat {chat_id}"
            for chat_id in manager.get_all_chats()
        ],
        label="Your chats:"
    )


    def user(user_input, conversation):
        """Get user input"""

        conversation.append({"role": "user", "content": user_input})

        return "", conversation


    def bot(conversation):
        """Get chat response"""

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

        manager.save_chat(conversation)

        return conversation


    def create_new_chat():

        conversation = manager.create_new_chat()

        return conversation, [], gr.Radio(
            choices=[
                f"Chat {chat_id}"
                for chat_id in manager.get_all_chats()
            ],
            label="Your chats:"
        )


    user_input.submit(
        user, 
        [user_input, conversation],
        [user_input, conversation],
        queue=False
    ).then(
        bot,
        conversation,
        [chat_bot, assistant_response]
    ).then(
        add_assistant_message,
        [conversation, assistant_response],
        conversation
    )

    new_chat_btn.click(
        create_new_chat,
        outputs=[conversation, chat_bot, chat_selector]
    )

demo.launch()