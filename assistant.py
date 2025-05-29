from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from pro_tem import prompt
from model import ProductResponse
from image_fetcher import fetch_product_image
from logger import log_query_response
from config import GROQ_API_KEY
import re


def ask_product_question(question: str) -> tuple[str, str, ProductResponse]:
    messages = [HumanMessage(content=prompt.format_messages(question=question)[0].content)]

    llm = ChatGroq(temperature=0, api_key=GROQ_API_KEY, model="llama3-8b-8192")
    response = llm(messages)
    text = response.content.strip()

    # Reject any non-formatted response
    if not all(key in text for key in ["Product Name:", "Product Details:", "Tentative Price:", "Release Date:", "**Advantages**", "**Disadvantages**"]):
        raise ValueError(f"Failed to parse LLM response: {text}")

    try:
        name = re.search(r"Product Name:\s*(.*)", text).group(1).strip()
        details = re.search(r"Product Details:\s*(.*)", text).group(1).strip()
        price = int(re.search(r"Tentative Price:\s*(\d+)", text).group(1).strip())
        release_date = re.search(r"Release Date:\s*(.*)", text).group(1).strip()

        advantages = re.findall(r"\*\*Advantages\*\*:\n((?:- .+\n?){3})", text)[0].strip().splitlines()
        disadvantages = re.findall(r"\*\*Disadvantages\*\*:\n((?:- .+\n?){3})", text)[0].strip().splitlines()

        product_response = ProductResponse(
            name=name,
            details=details,
            price=price,
            release_date=release_date,
            advantages=[adv.strip("- ").strip() for adv in advantages],
            disadvantages=[dis.strip("- ").strip() for dis in disadvantages],
        )

        log_query_response(question, product_response)
        image_url = fetch_product_image(name)

        return text, image_url, product_response

    except Exception as e:
        raise ValueError(f"Failed to parse LLM response: {text}")
