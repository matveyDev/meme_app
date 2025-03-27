import os
from fastapi import APIRouter, HTTPException
from openai import AsyncOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

router = APIRouter()

class ImagePrompt(BaseModel):
    prompt: str

class ChatGPTAPI:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    async def generate_image(self, prompt: str) -> str:
        """
        Generate an image based on the text prompt using DALL-E
        
        Args:
            prompt (str): Text description of the image to generate
            
        Returns:
            str: URL of the generated image
        """
        try:
            # Генерируем изображение напрямую с DALL-E 3
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                style="vivid",
                n=1,
            )
            
            return response.data[0].url
            
        except Exception as e:
            print(f"Error generating image: {e}")
            raise HTTPException(status_code=500, detail=str(e))
            
    async def get_chat_response(self, message: str) -> str:
        """
        Get a response from ChatGPT
        
        Args:
            message (str): User's message
            
        Returns:
            str: ChatGPT's response
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting chat response: {str(e)}")

# Create a singleton instance
chatgpt_api = ChatGPTAPI()

@router.post("/generate_image/")
async def generate_image(prompt_data: ImagePrompt):
    """
    Generate an image using DALL-E based on the provided prompt
    """
    print(f"Received prompt: {prompt_data.prompt}")
    image_url = await chatgpt_api.generate_image(prompt_data.prompt)
    return {"image_url": image_url}

@router.post("/chat")
async def chat(message: str):
    """
    Get a response from ChatGPT for the provided message
    """
    return await chatgpt_api.get_chat_response(message)
