import os
from urllib.request import urlopen, Request
import base64
from pathlib import Path
from dotenv import load_dotenv

# Add references
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        endpoint = os.getenv("PROJECT_CONNECTION")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")


        # Initialize the project client
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
        client = OpenAI(
            base_url=endpoint,
            api_key=token_provider(),
            default_query={"api-version": "2024-05-01-preview"}
        )
        

        # Get a chat client
        



        # Initialize prompts
        system_message = "You are an AI assistant in a grocery store that sells fruit. You provide detailed answers to questions about produce."
        prompt = ""

        # Loop until the user types 'quit'
        while True:
            prompt = input("\nAsk a question about the image\n(or type 'quit' to exit)\n")
            if prompt.lower() == "quit":
                break
            elif len(prompt) == 0:
                    print("Please enter a question.\n")
            else:
                print("Getting a response ...\n")


                # Get a response to image input 
                """ # 
                image_url = "https://github.com/MicrosoftLearning/mslearn-ai-vision/raw/refs/heads/main/Labfiles/gen-ai-vision/orange.jpeg"
                image_format = "jpeg"
                request = Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
                image_data = base64.b64encode(urlopen(request).read()).decode("utf-8")
                data_url = f"data:image/{image_format};base64,{image_data}"

                response = client.chat.completions.create(
                    model=model_deployment,
                    messages=[
                        {"role": "system", "content": system_message},
                        { "role": "user", "content": [  
                            { "type": "text", "text": prompt},
                            { "type": "image_url", "image_url": {"url": data_url}}
                        ] } 
                    ]
                )
                print(response.choices[0].message.content)
                """
                # Get a response to image input
                script_dir = Path(__file__).parent  # Get the directory of the script
                image_path = script_dir / 'mystery-fruit.jpeg'
                mime_type = "image/jpeg"

                # Read and encode the image file
                with open(image_path, "rb") as image_file:
                    base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

                # Include the image file data in the prompt
                data_url = f"data:{mime_type};base64,{base64_encoded_data}"
                response = client.chat.completions.create(
                        model=model_deployment,
                        messages=[
                            {"role": "system", "content": system_message},
                            { "role": "user", "content": [  
                                { "type": "text", "text": prompt},
                                { "type": "image_url", "image_url": {"url": data_url}}
                            ] } 
                        ]
                )
                print(response.choices[0].message.content)
    except Exception as ex:
        print(ex)


if __name__ == '__main__': 
    main()