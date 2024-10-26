import base64
from fastapi import FastAPI, File, UploadFile, Form
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import os
import re
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware   
from datetime import datetime
import pytesseract
from fastapi import HTTPException
import json
import csv
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds_def.json'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

client = Groq(
    api_key='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',
)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

vertexai.init(project="presales-286307", location="us-central1")

@app.post("/generate")
async def generate_image(
    prompt: str = Form(...),      
    image: UploadFile = File(...)  
):
    # Read image data
    image_data = await image.read()
    image_part = Part.from_data(
        mime_type=image.content_type,
        data=image_data,  
    )
    
    # Prepare the generation configuration
    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }
    
    # Initialize model and generate content
    model = GenerativeModel("gemini-1.5-flash-002")
    responses = model.generate_content(
        [image_part, prompt],
        generation_config=generation_config,
        stream=True,
    )

    result = ""
    for response in responses:
        result += response.text
    
    # Use Llama model for structuring data
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": """Your role is a text-structuring model in JSON nothing else structure the below text into (NO comments and no additional text)
                {
                    "datetime": (always convert it to yyyy-mm-dd hh:mm:ss format),
                    "coords": [[lat1, lon1],[latn,lonn]],
                    "description": (descriptive summary of the whole message),
                    "speed": (unknown if not mentioned),
                    "directions": (unknown if not mentioned),
                    "depth": (unknown if not mentioned)
                }"""
                + f"""
                Context:
                {result}
                """,
            }
        ],
        model="llama3-70b-8192",
    )
    
    text = chat_completion.choices[0].message.content
    print(text)
    pattern = r"\{[^{}]*\}"
    matches = re.findall(pattern, text)

    structured_data = None
    for match in matches:
        print(match)
        structured_data = json.loads(match)
    
    # Return structured data and OCR result
    return {
        "structured": structured_data,
        "OCR": result
    }

@app.post("/update_report")
async def update_report(data: dict):
    try:
        # Ensure `structured_data` and `ocr_result` exist in `data`
        structured_data = data.get("structured_data", {})
        ocr_result = data.get("ocr_result", "")

        # Writing to CSV
        with open('report.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['datetime', 'coords', 'description', 'speed', 'directions', 'depth']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'datetime': structured_data.get('datetime', 'Unknown'),
                'coords': structured_data.get('coords', 'Unknown'),
                'description': structured_data.get('description', 'Unknown'),
                'speed': structured_data.get('speed', 'Unknown'),
                'directions': structured_data.get('directions', 'Unknown'),
                'depth': structured_data.get('depth', 'Unknown'),
            })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing to CSV: {e}")

    try:
        # Ensure the master directory exists
        master_dir = os.path.join(os.getcwd(), "master")
        os.makedirs(master_dir, exist_ok=True)

        # Create a file with the current date in its name
        date_str = datetime.now().strftime("%y-%m-%d")
        file_path = os.path.join(master_dir, f"{date_str}-report.txt")

        # Write OCR result to the text file
        with open(file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(ocr_result + "\n")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing OCR to text file: {e}")

    return {"message": "Report updated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
