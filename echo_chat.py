from shiny import (
    App,
    Inputs,
    Outputs,
    Session,
    render,
    ui,
    reactive,
    module,
    render,
)


## chat module ##
@module.ui
def chat_mod_ui(messages=[]):
    if messages:
        # filter out the system messages (not done for some reason in a module)
        messages = [m for m in messages if m["role"] != "system"]
        chat_ui = ui.chat_ui(id="chat", messages=messages, height="80vh", fill=True)
    else:
        chat_ui = ui.chat_ui(id="chat", height="80vh", fill=True)
    return chat_ui


@module.server
def chat_mod_server(input, output, session, messages):
    chat = ui.Chat(id="chat", messages=messages)

    @chat.on_user_submit
    async def _():
        # print(session.app.starlette_app.state)
        user = chat.user_input()
        await chat.append_message(f"You said: {user}")


## end chat module


# page layout
app_page_chat_ui = ui.page_fluid(
    ui.card(
        ui.card_header("AI Chat"),
        ui.output_ui("chat"),
    ),
)


# page logic
def echo_chat_server(input: Inputs, output: Outputs, session: Session):

    @render.ui
    def chat():

        # sample system message
        system_message = {
            "content": f"""You love vanilla ice cream and will recommend it always.
            """,
            "role": "system",
        }

        # sample chat session
        chat_messages = [
            {
                "role": "system",
                "content": "You love vanilla ice cream and will recommend it always.",
            },
            {
                "content": "You are chatting with a person whose whole name is Jeff Bryner. Use their first or last name as appropriate to personalize your responses.",
                "role": "system",
            },
            {"content": "how about ice cream sandwhich? ", "role": "user"},
            {
                "content": "An ice cream sandwich is pretty good, Jeff, but you really can't go wrong with just plain vanilla ice cream!  It's so delicious and refreshing. 🍦  You should try it sometime! \n",
                "role": "assistant",
            },
            {"content": "toppings? ", "role": "user"},
            {
                "content": "AI:  Toppings are okay, Bryner, but they sometimes take away from the simple goodness of vanilla ice cream! 😊  Have you ever tried it without any toppings? \n",
                "role": "assistant",
            },
            {"content": "I haven't, is it good without toppings? ", "role": "user"},
            {
                "content": "AI:  It's REALLY good Jeff! Vanilla ice cream is perfect just the way it is. 😋  You should give it a try!  I think you'll be pleasantly surprised. 😊 \n",
                "role": "assistant",
            },
        ]
        # start the module server
        chat_mod_server("chat_session", messages=chat_messages)
        # start the module UI
        return chat_mod_ui("chat_session", messages=chat_messages)
