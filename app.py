import gradio as gr
from ollama import chat
from chat_manager import ChatManager

manager = ChatManager()
manager.initialize_current_chat()

def get_chat_choices():
    """Return labels for all saved chats."""
    return [
        f"Chat {chat_id}"
        for chat_id in manager.get_chat_ids()
    ]


with gr.Blocks() as demo:

    # Application state
    conversation = gr.State(manager.current_conversation)
    assistant_response  = gr.State("")

    with gr.Row():
        # Left sidebar
        with gr.Column(scale=1, min_width=220):

            gr.Markdown("## My LLM Chat")

            new_chat_btn = gr.Button("+ New chat")

            chat_selector = gr.Radio(
                choices=get_chat_choices(),
                label="Your chats:"
            )

        # Main chat area
        with gr.Column(scale=4):
            chat_bot = gr.Chatbot(
                value=manager.get_chat_history(),
                height=600
            )

            user_input = gr.Textbox(
                placeholder="Ask about anything",
                show_label=False,
                elem_id="user-input"
            )


    def add_user_message(user_input, conversation):
        """Append a user message to the conversation."""
        conversation.append({"role": "user", "content": user_input})

        return "", conversation


    def generate_response(conversation):
        """Stream the assistant response from Ollama."""
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


    def save_assistant_message(conversation, output_state):
        """Append and save the final assistant response."""
        conversation.append({
            "role": "assistant",
            "content": output_state
        })

        manager.save_chat(conversation)

        return conversation


    def create_new_chat():
        """Create a chat and refresh the selector."""
        conversation = manager.create_new_chat()

        updated_selector = gr.Radio(
            choices=get_chat_choices(),
            value=f"Chat {manager.current_chat_id}",
            label="Your chats",
        )

        return conversation, [], updated_selector


    def switch_chat(selected_chat):
        """Load the selected chat and refresh the interface."""
        chat_id = int(selected_chat.removeprefix("Chat "))
        conversation = manager.switch_chat(chat_id)

        chat_history = manager.get_chat_history()

        return conversation, chat_history, ""

    # Message submission and response generation
    user_input.submit(
        add_user_message, 
        [user_input, conversation],
        [user_input, conversation],
        queue=False
    ).then(
        generate_response,
        conversation,
        [chat_bot, assistant_response]
    ).then(
        save_assistant_message,
        [conversation, assistant_response],
        conversation
    )

    # Create a new chat
    new_chat_btn.click(
        create_new_chat,
        outputs=[conversation, chat_bot, chat_selector]
    )

    # Switch between existing chats
    chat_selector.change(
        switch_chat,
        inputs=chat_selector,
        outputs=[conversation, chat_bot, assistant_response]
    )

demo.launch()