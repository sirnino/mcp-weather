from tools import api, web, video
import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown("## This tool is MCP-only, so it does not have a UI.") 
    gr.api(fn=api.current_weather)
    gr.api(fn=web.scrape_body)
    gr.api(fn=video.youtube_transcript)
    gr.api(fn=web.get_title)

demo.launch(mcp_server=True)