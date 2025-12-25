from groq import Groq
import os
import json

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def format_with_groq(extracted_text):
    """
    Use Groq LLM to format extracted text into structured JSON
    """
    try:
        prompt = f"""
You are an expert data extraction assistant. Analyze the following extracted text from a document and convert it into a well-structured JSON format.

Extract the following information if present:
- Document type (ID card, invoice, receipt, contract, etc.)
- Personal information (name, date of birth, address, ID numbers, etc.)
- Financial information (amounts, dates, transaction details, etc.)
- Any other relevant structured data

Provide the output as a clean JSON object. If information is not found, use null values.

Extracted Text:
{extracted_text}

Return only valid JSON, no additional text or explanation.
"""
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a data extraction expert that converts unstructured text into structured JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=2000,
        )
        
        response_text = chat_completion.choices[0].message.content.strip()
        
        # Try to parse as JSON
        try:
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            formatted_data = json.loads(response_text)
            return formatted_data
            
        except json.JSONDecodeError:
            # If parsing fails, return as structured dict
            return {
                "raw_extraction": response_text,
                "extracted_text": extracted_text,
                "status": "parsing_failed"
            }
    
    except Exception as e:
        return {
            "error": str(e),
            "extracted_text": extracted_text,
            "status": "groq_error"
        }