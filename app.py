import gradio as gr
from ollama import chat
from chat_manager import ChatManager

# Create manager class and initialize the conversation
manager = ChatManager()
manager.initialize_current_chat()

# Create demo block
with gr.Blocks() as demo:

    # Conversation history in Ollama message format
    conversation = gr.State(manager.current_conversation)

    # Current model response
    assistant_response  = gr.State("")

    # Row with user input
    with gr.Row():
        user_input = gr.Textbox(
            placeholder="Ask about anything",
            show_label=False,
            elem_id="user-input"
        )

    # Chat bot display provided by Gradio API
    chat_bot = gr.Chatbot(value=manager.get_chat_history())

    # Create new chat (button)
    with gr.Row():
        new_chat_btn = gr.Button(value="New chat")


    def user(user_input, conversation):
        """Get user input from textbox"""

        # Append user input
        conversation.append({"role": "user", "content": user_input})

        # Clear user input and return updated conversation
        return "", conversation


    def bot(conversation):
        """Get chat response and stream it in chat bot display"""

        # Get the model response by using gemma3:4b model
        response = chat(
            model="gemma3:4b", 
            messages=conversation, 
            stream=True
        )

        # Stream the model response in chat bot display
        chat_output = ""

        for chunk in response:

            chat_output += chunk.message.content
            conversation_temp = conversation + [
                {"role": "assistant", "content": chat_output}
            ]

            # Yield conversation word by word and update model response by using chat_output
            yield conversation_temp, chat_output


    def add_assistant_message(conversation, output_state):
        """Add assistand message to conversation"""
        conversation.append({
            "role": "assistant",
            "content": output_state
        })

        # Save data
        manager.save_chat(conversation)

        # Return update conversation
        return conversation


    def create_new_chat():
        ...

        # Create new chat by using ChatManager

        
        # Set new chat as current chat


        # Clear chat_bot view


        # Update conversation to the chat go into new conversation


    # Conversation flow
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

    # Create new chat
    new_chat_btn.click(
        create_new_chat,
    )

demo.launch()