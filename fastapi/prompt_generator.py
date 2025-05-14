import json
import random
from pathlib import Path

def load_prompts():
    prompts_path = Path(__file__).parent / 'prompts.json'
    print(f"Loading prompts from: {prompts_path}")
    try:
        with open(prompts_path, 'r') as file:
            data = json.load(file)
            print(f"Loaded prompts data: {data}")
            return data
    except Exception as e:
        print(f"Error loading prompts: {str(e)}")
        return None

def generate_prompt(animal: str, object: str) -> str:
    """
    Generate a detailed prompt based on the selected animal and object.
    
    Args:
        animal (str): The selected animal (e.g., 'Monkey')
        object (str): The selected object (e.g., 'PlayStation')
    
    Returns:
        str: A complete prompt for image generation
    """
    print(f"Generating prompt for animal: {animal}, object: {object}")
    prompts = load_prompts()
    
    if not prompts:
        raise ValueError("Failed to load prompts data")
    
    try:
        # Check if animal exists
        if animal not in prompts['animals']:
            raise ValueError(f"Animal '{animal}' not found in prompts")
            
        # Get the animal's prompts
        animal_data = prompts['animals'][animal]
        print(f"Found animal data: {animal_data}")
        
        # Check if object exists for this animal
        if object not in animal_data['objects']:
            raise ValueError(f"Object '{object}' not found for animal '{animal}'")
            
        # Get the object's prompts
        object_data = animal_data['objects'][object]
        print(f"Found object data: {object_data}")
        
        animal_prompt = random.choice(animal_data['animal_prompts'])
        print(f"Selected animal prompt: {animal_prompt}")
        object_prompt = random.choice(object_data['object_prompts'])
        print(f"Selected object prompt: {object_prompt}")
        background_prompt = random.choice(object_data['background_prompts'])
        print(f"Selected background prompt: {background_prompt}")
        
        # Construct the final prompt
        prompt = (
            f"Create a surreal, high-quality 3D image of {animal_prompt} "
            f"{object_prompt} {background_prompt}. "
            "The visual style is absurd, shiny, clean, and cartoonish inspired by "
            "BombordiroCrocodilo and Bombini Goosini memes. Use vibrant colors, "
            "glossy surfaces, and a minimal background."
        )
        
        print(f"Generated final prompt: {prompt}")
        return prompt
    
    except KeyError as e:
        print(f"Error generating prompt: {str(e)}")
        raise ValueError(f"Invalid animal or object combination: {animal} + {object}") from e
    except Exception as e:
        print(f"Unexpected error generating prompt: {str(e)}")
        raise ValueError(f"Failed to generate prompt: {str(e)}") from e

if __name__ == "__main__":
    # Example usage
    try:
        prompt = generate_prompt("Monkey", "PlayStation")
        print(prompt)
    except ValueError as e:
        print(f"Error: {e}") 