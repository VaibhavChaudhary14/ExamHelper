import os
from openai import OpenAI
import streamlit as st

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_ai_response(message, context=""):
    """Get response from OpenAI API"""
    try:
        system_prompt = """You are a helpful AI assistant for GATE and CAT exam preparation. 
        You provide accurate, concise answers and study tips. You also offer motivation 
        and guidance for personal development and maintaining good habits.
        When discussing sensitive topics like addiction, maintain a professional,
        supportive tone and encourage seeking professional help when appropriate."""
        
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        if context:
            messages.append({"role": "user", "content": f"Context: {context}"})
            
        messages.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error: Unable to get response from AI. Please try again later. ({str(e)})"
