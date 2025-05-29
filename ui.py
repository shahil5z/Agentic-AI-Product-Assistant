import gradio as gr
from assistant import ask_product_question
from model import ProductResponse

def display_product(product: ProductResponse):
    return (
        f"### 🛒 **{product.name}**\n\n"
        f"**📄 Details**: {product.details}\n\n"
        f"**Price**: ${product.price}\n\n"
        f"**Release Date**: {product.release_date}\n\n"
        f"**Advantages**:\n" + "\n".join([f"- {adv}" for adv in product.advantages]) + "\n\n"
        f"**Disadvantages**:\n" + "\n".join([f"- {dis}" for dis in product.disadvantages])
    )


def handle_query(question: str):
    try:
        response_text, image_url, product = ask_product_question(question)
        formatted_text = display_product(product)
        return formatted_text, image_url
    except Exception as e:
        return f"❌ Error: {str(e)}", None


with gr.Blocks(css="""
#footer, footer, .svelte-13jv051 {
    display: none !important;
}
""") as demo:
    gr.Markdown("## 🤖 AI Product Assistant\nEnter a product name to get its details.")
    with gr.Row():
        input_box = gr.Textbox(label="Enter Product Name")
    with gr.Row():
        submit_button = gr.Button("Search Product")
    with gr.Row():
        output_text = gr.Markdown()
        output_image = gr.Image(type="filepath", label="Product Image")

    submit_button.click(fn=handle_query, inputs=[input_box], outputs=[output_text, output_image])

if __name__ == "__main__":
    demo.launch(show_api=False, show_error=False, inbrowser=True)
