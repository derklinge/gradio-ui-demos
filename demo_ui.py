"""
A most simple user interface example that uses the Gradio framework.
"""
import gradio as gr

def build():
  ui_root = gr.Interface(fn=greet, inputs="text", outputs="text")
  return ui_root

def greet(name):
    return "Hello " + name + "!"
