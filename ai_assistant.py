from openai import OpenAI
import streamlit as st


class AIChatAssistant:
    def __init__(self, inventory, sales, flags):
        self.inventory = inventory
        self.sales = sales
        self.flags = flags
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    def build_context(self):
        return f"""
Inventory Data:
{self.inventory}

Sales Data:
{self.sales}

Low Stock Flags:
{self.flags}
"""

    def generate_response(self, user_question):
        context = self.build_context()

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful bakery inventory assistant. "
                        "Use the provided inventory, sales, and low stock data to answer questions. "
                        "Keep answers short, clear, and useful for bakery employees."
                    )
                },
                {
                    "role": "user",
                    "content": f"Data:\n{context}\n\nQuestion: {user_question}"
                }
            ]
  