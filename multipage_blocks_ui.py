"""
A stateful multi-page UI example using gradio.Blocks()
"""
import gradio as gr
import numpy

def build():
  page_headlines_markdown = {
    1: """# Source Image
          *Browse for an image to upload, or use your device\'s camera if available.*
       """,
    2: """# Bogus Example Page
          *Just a plain textbox here for demo purposes.*
       """,
  }

  with gr.Blocks() as ui_root:

    # Application States
    state_current_page = gr.State(value=1)
    state_source_image = gr.State(value=None)

    # Layout
    with gr.Row():
      # Header
      with gr.Column(scale=1):
        with gr.Row():
          with gr.Column():
            page_headline = gr.Markdown(
              value=page_headlines_markdown[state_current_page.value]
            )
        with gr.Row():
          with gr.Column(min_width=160):
            button_back = gr.Button(
              "Back",
              interactive=False,
              variant="secondary",
              visible=False
            )
          with gr.Column(min_width=160):
            button_confirm = gr.Button(
              "Next",
              interactive=False,
              variant="primary"
            )
      # Page Container
      with gr.Column(scale=3) as page_container_1:
        with gr.Row():
          with gr.Column():
            source_image_browse = gr.Image(
              source="upload",
              shape=(320, 240),
              label="Browse"
            )
          with gr.Column():
            source_image_camera = gr.Image(
              source="webcam",
              shape=(320, 240),
              label="Camera"
            )
        with gr.Row():
          with gr.Column():
            button_reset = gr.Button(
              "Reset",
              interactive=False,
              variant="secondary",
              visible=False
            )
      # Page Container
      with gr.Column(scale=3, visible=False) as page_container_2:
        with gr.Row():
            gr.Text("YEEHAAAWWWRRR!!")

    def on_change_image(image, state):
      can_proceed = isinstance(image, numpy.ndarray) or image != None
      if can_proceed:
        state = image
      return \
        state, \
        None, \
        gr.update(interactive=can_proceed), \
        gr.update(interactive=can_proceed, visible=can_proceed)

    source_image_browse.change( \
      fn=on_change_image,
      inputs=[
        source_image_browse,
        state_source_image
      ],
      outputs=[
        state_source_image,
        source_image_camera,
        button_confirm,
        button_reset
      ]
    )

    source_image_camera.change( \
      fn=on_change_image,
      inputs=[
        source_image_camera,
        state_source_image
      ],
      outputs=[
        state_source_image,
        source_image_browse,
        button_confirm,
        button_reset
      ]
    )

    def on_click_button_back(state_page):
      if state_page > 1:
        state_page -= 1
        return \
          state_page, \
          page_headlines_markdown[state_page], \
          gr.update(visible=True), \
          gr.update(visible=False), \
          gr.update(interactive=True), \
          gr.update(interactive=True, visible=True), \
          gr.update(interactive=state_page > 1, visible=state_page > 1)

    button_back.click( \
      fn=on_click_button_back,
      inputs=state_current_page,
      outputs=[
        state_current_page,
        page_headline,
        page_container_1,
        page_container_2,
        button_confirm,
        button_reset,
        button_back,
      ]
    )

    def on_click_button_confirm(state_page):
      if state_page < 2:
        state_page += 1
        return \
          state_page, \
          page_headlines_markdown[state_page], \
          gr.update(visible=False), \
          gr.update(visible=True), \
          gr.update(interactive=False), \
          gr.update(interactive=False, visible=False), \
          gr.update(interactive=True, visible=True)
      else:
        raise NotImplementedError()

    button_confirm.click( \
      fn=on_click_button_confirm,
      inputs=state_current_page,
      outputs=[
        state_current_page,
        page_headline,
        page_container_1,
        page_container_2,
        button_confirm,
        button_reset,
        button_back
      ]
    )

    def on_click_button_reset(state_page):
      if state_page == 1:
        return \
          state_page, \
          None, \
          None, \
          gr.update(interactive=False), \
          gr.update(interactive=False, visible=False)
      else:
        raise NotImplementedError()

    button_reset.click( \
      fn=on_click_button_reset,
      inputs=state_current_page,
      outputs=[
        state_current_page,
        source_image_browse,
        source_image_camera,
        button_confirm,
        button_reset
      ]
    )

  return ui_root
