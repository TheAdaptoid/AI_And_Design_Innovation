from datetime import datetime

from nicegui import ui

from backend.types import Message
from backend.orchestrator import Agent

ASSISTANT_NAME: str = "Jaxon"

agent: Agent = Agent()
convo_thread: list[Message] = [
    Message(
        content=f"Hello, I am {ASSISTANT_NAME}. How can I help you today?",
        role="assistant",
        timestamp=datetime.now(),
    )
]


async def trigger_chat_turn(
    input_element: ui.input, chat_window: ui.scroll_area
) -> None:
    """
    Trigger a chat turn by creating a user message, getting the response, and
    displaying both messages in the chat window.

    Args:
        input_element (ui.input): The input element to get the user message from.
        chat_window (ui.scroll_area): The chat window to display the messages in.
    """
    # Create user message
    user_message: Message = Message(
        content=input_element.value, role="user", timestamp=datetime.now()
    )
    input_element.value = ""  # Clear input
    input_element.disable()  # Lock the input until the response is received

    # Add user message to thread
    convo_thread.append(user_message)

    # Display user message
    await display_message(user_message, chat_window)

    # Get agent response
    response: Message = await receive_response()

    # Add agent response to thread
    convo_thread.append(response)

    # Display agent response
    await display_message(response, chat_window)

    # Enable input
    input_element.enable()

    # Scroll to bottom
    chat_window.scroll_to(percent=1, duration=0.5)


async def receive_response() -> Message:
    """
    Receive a response from the agent.

    Returns:
        Message: The agent response.
    """
    return await agent.chat(convo_thread)


async def display_message(message: Message, chat_window: ui.scroll_area) -> None:
    """
    Display a message in the chat window.

    Args:
        message (Message): The message to display.
        chat_window (ui.scroll_area): The chat window to display the message in.
    """
    with chat_window:
        with ui.card().classes("w-full flex-col flex-nowrap items-start").classes(
            "bg-accent" if message.role == "assistant" else "bg-primary"
        ):
            ui.label(
                f"{message.role.capitalize() if message.role == 'user' else ASSISTANT_NAME} | {message.timestamp.strftime('%I:%M:%S %p')}"
            )
            ui.separator().classes("-my-4")
            ui.markdown(message.content).classes("text-left")


@ui.page("/")
async def index() -> None:
    """
    The main page of the application.
    """
    ui.colors(secondary="#ffffff", primary="#F1F4F6", accent="#3c8cc3")

    with ui.header().classes("bg-accent"):
        with ui.row().classes("w-full justify-between items-center"):
            ui.icon("school")
            ui.label("Jacksonville Public Library")
            ui.space()
            ui.icon("menu")
            ui.label("User's Name")

    # Chat window
    chat_window = ui.scroll_area().classes(
        "w-full h-[calc(100vh-13rem)] overflow-hidden flex-col justify-between items-center"
    )
    for message in convo_thread:
        await display_message(message, chat_window)

    with ui.footer().classes(
        "w-full h-1/8 flex-row flex-nowrap justify-between items-center bg-accent"
    ):
        # User input card
        with ui.card().classes(
            "w-full h-full flex-row flex-nowrap items-center bg-primary"
        ):
            # TODO: Add autocomplete for suggested topics
            input_element: ui.input = (
                ui.input(placeholder="Chat with Jaxon...")
                .classes("flex-1 bg-secondary rounded-lg inset-5 px-2")
                .props("borderless")
                .on(
                    "keydown.enter",
                    lambda: trigger_chat_turn(input_element, chat_window),
                )
            )
            ui.button(
                "Send", on_click=lambda: trigger_chat_turn(input_element, chat_window)
            ).classes("basis-1/6 bg-accent")
