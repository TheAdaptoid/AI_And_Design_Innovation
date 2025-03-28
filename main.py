from nicegui import ui
from frontend.index import index

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="Jaxon",
        reload=True,
    )
