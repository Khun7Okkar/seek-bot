import requests
import json
import re
from bs4 import BeautifulSoup
import config

class JobExtractor:
    def __init__(self):
        self.api_url = f"{config.LLM_API_BASE}/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.LLM_API_KEY}"
        }

    def clean_html(self, raw_html):
        """Strips out unnecessary tags to save tokens."""
        soup = BeautifulSoup(raw_html, 'html.parser')
        
        # Remove script, style, nav, footer, and other clutter
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'noscript', 'iframe', 'svg']):
            element.decompose()
            
        # Get text, but keep some structure usually helpful. 
        # However, passing cleaned HTML might be better for structure if token limit allows,
        # but pure text is safer for small local models.
        # User requested "strip out tags... send cleaned text".
        # Let's try to keep it as dense text or simplified HTML.
        
        # Simplest: get text with separators
        text = soup.get_text(separator='\n')
        
        # Compress whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return clean_text[:15000] # Truncate if too huge to prevent context overflow

    def extract_job_details(self, raw_html):
        """Sends cleaned text to LLM and returns structured JSON."""
        cleaned_text = self.clean_html(raw_html)
        
        system_prompt = (
            "You are a precise data extraction assistant. "
            "Extract job details from the provided text. "
            "Return ONLY a valid JSON object with the following keys: "
            "company_name, job_position, full_description, date_posted (DD/MM/YYYY). "
            "If a field is missing, use 'N/A'. "
            "Do not include markdown formatting (```json) or conversational text."
        )
        
        user_prompt = f"Extract job info from this text:\n\n{cleaned_text}"
        
        payload = {
            "model": config.LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.1, # Low temp for factual extraction
            "json_schema": { # Structured output if supported (OpenAI comp.)
                "type": "object",
                "properties": {
                   "company_name": {"type":  "string"},
                   "job_position": {"type": "string"},
                    "full_description": {"type": "string"},
                    "date_posted": {"type": "string"}
                 }
            }
        }
        
        try:
            print("  [Extractor] Sending content to LLM...")
            # Note: json_schema param might not be supported by all local LLMs in 0.2.x of OpenAI format,
            # but LM Studio often supports 'response_format' or just simple prompting.
            # We'll try standard keys first.
            
            # Adjust payload for broader compatibility if needed, e.g. "stream": False
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Cleanup if LLM returns markdown fences
                content = content.replace("```json", "").replace("```", "").strip()
                
                try:
                    data = json.loads(content)
                    return data
                except json.JSONDecodeError:
                    print(f"  [Extractor] Failed to parse JSON: {content[:100]}...")
                    return None
            else:
                print(f"  [Extractor] API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"  [Extractor] Error calling LLM: {e}")
            return None
