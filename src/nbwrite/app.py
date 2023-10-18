import gradio as gr
from dotenv import load_dotenv

from nbwrite.writer import gen

if __name__ == "__main__":
    load_dotenv()
    placeholder_task = "Create a hello world notebook 'x.ipynb', use nbmake's NotebookRun class to test it from a Python application"

    demo = gr.Interface(
        fn=gen,
        inputs=[
            gr.Textbox(lines=2, placeholder=placeholder_task),
            "text",
            "text",
            "text",
            "text",
            "text",
        ],
        outputs="text",
    )

    demo.launch()
