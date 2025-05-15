import requests
import json
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional, Union
import time

# Load environment variables from .env file
load_dotenv('env_file')

class PerplexityAPI:
    def __init__(self):
        self.api_key = os.getenv('PERPLEXITY_API_KEY')
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY not found in environment variables")
        
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Updated models based on official Perplexity documentation
        self.models = {
            "1": {
                "name": "sonar",
                "description": "Lightweight search model (128k context) - Best for quick factual queries and summaries",
                "type": "search",
                "has_web_search": True,
                "context_length": 128000
            },
            "2": {
                "name": "sonar-pro",
                "description": "Advanced search model (200k context) - Best for complex queries and follow-ups",
                "type": "search",
                "has_web_search": True,
                "context_length": 200000,
                "max_output_tokens": 8000
            },
            "3": {
                "name": "sonar-reasoning",
                "description": "Fast reasoning model (128k context) - Best for quick problem-solving with search",
                "type": "reasoning",
                "has_web_search": True,
                "context_length": 128000,
                "features": ["Chain of Thought (CoT)"]
            },
            "4": {
                "name": "sonar-reasoning-pro",
                "description": "Premier reasoning model (128k context) - Powered by DeepSeek R1 with CoT",
                "type": "reasoning",
                "has_web_search": True,
                "context_length": 128000,
                "features": ["Chain of Thought (CoT)"]
            },
            "5": {
                "name": "sonar-deep-research",
                "description": "Expert research model (128k context) - Best for comprehensive reports and analysis",
                "type": "research",
                "has_web_search": True,
                "context_length": 128000,
                "note": "May take 30+ minutes for complex tasks"
            },
            "6": {
                "name": "r1-1776",
                "description": "Offline chat model (128k context) - No web search, best for creative content",
                "type": "offline",
                "has_web_search": False,
                "context_length": 128000,
                "note": "Post-trained for uncensored, unbiased, and factual information"
            }
        }

    def verify_web_search(self, model: str) -> bool:
        """
        Verify if a model has web search capability by making a test request.
        """
        test_prompt = "What is the current time in New York? (This requires web search)"
        try:
            result = self.call_api(
                prompt=test_prompt,
                model=model,
                system_prompt="You are a helpful assistant. If you can't access web search, say 'I cannot access web search'.",
                temperature=0.7,
                max_tokens=100
            )
            
            if result and 'choices' in result:
                response = result['choices'][0]['message']['content'].lower()
                return "cannot access web search" not in response
            return False
        except Exception as e:
            print(f"Error during web search verification: {str(e)}")
            return False

    def call_api(
        self,
        prompt: str,
        model: str = "sonar",
        system_prompt: str = "Be precise and concise.",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        messages: Optional[List[Dict[str, str]]] = None,
        verify_web: bool = False
    ) -> Union[Dict, None]:
        """
        Call the Perplexity API with specified parameters.
        
        Args:
            prompt: The user's prompt
            model: The model to use
            system_prompt: System prompt for the model
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum length of response
            stream: Whether to stream the response
            messages: Optional list of previous messages for conversation
            verify_web: Whether to verify web search capability
        
        Returns:
            API response as dictionary or None if error
        """
        # Validate model name
        valid_models = [m["name"] for m in self.models.values()]
        if model not in valid_models:
            print(f"Error: Invalid model '{model}'. Available models are: {', '.join(valid_models)}")
            return None

        if verify_web:
            if not self.verify_web_search(model):
                print(f"Warning: Model {model} may not have web search capability")
                if input("Continue anyway? (y/n): ").lower() != 'y':
                    return None

        if messages is None:
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        # Ensure messages are properly formatted
        for msg in messages:
            if not isinstance(msg, dict) or 'role' not in msg or 'content' not in msg:
                raise ValueError("Invalid message format. Each message must have 'role' and 'content' fields.")
            if msg['role'] not in ['system', 'user', 'assistant']:
                raise ValueError("Invalid role. Must be one of: system, user, assistant")

        data = {
            "model": model,
            "messages": messages,
            "temperature": max(0.0, min(1.0, temperature))  # Ensure temperature is between 0 and 1
        }

        if max_tokens is not None:
            data["max_tokens"] = max(1, max_tokens)  # Ensure max_tokens is positive
        
        if stream:
            data["stream"] = True
            self.headers["Accept"] = "text/event-stream"
        else:
            self.headers["Accept"] = "application/json"

        try:
            # Print request details for debugging
            print(f"\nMaking request to {self.base_url}")
            print(f"Model: {model}")
            print(f"Headers: {json.dumps({k: v for k, v in self.headers.items() if k != 'Authorization'}, indent=2)}")
            print(f"Data: {json.dumps(data, indent=2)}")
            
            response = requests.post(self.base_url, headers=self.headers, json=data)
            
            # Print response details for debugging
            print(f"\nResponse Status: {response.status_code}")
            if response.status_code != 200:
                print(f"Response Body: {response.text}")
                if response.status_code == 400:
                    error_data = response.json()
                    if 'error' in error_data:
                        print(f"\nError Type: {error_data['error'].get('type', 'unknown')}")
                        print(f"Error Message: {error_data['error'].get('message', 'No message provided')}")
                        if 'docs' in error_data['error']:
                            print(f"Documentation: {error_data['error']['docs']}")
            
            response.raise_for_status()
            
            if stream:
                return self._handle_stream(response)
            
            result = response.json()
            if 'choices' not in result or not result['choices']:
                print("Warning: No choices in response")
                print(f"Full response: {json.dumps(result, indent=2)}")
                return None
                
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    if 'error' in error_data:
                        print(f"\nError Type: {error_data['error'].get('type', 'unknown')}")
                        print(f"Error Message: {error_data['error'].get('message', 'No message provided')}")
                        if 'docs' in error_data['error']:
                            print(f"Documentation: {error_data['error']['docs']}")
                except:
                    print(f"Error details: {e.response.text}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None

    def _handle_stream(self, response) -> None:
        """Handle streaming response"""
        try:
            for line in response.iter_lines():
                if line:
                    try:
                        # Remove 'data: ' prefix if present
                        line_text = line.decode('utf-8')
                        if line_text.startswith('data: '):
                            line_text = line_text[6:]
                        
                        if line_text.strip() == '[DONE]':
                            print("\nStream completed")
                            break
                            
                        json_response = json.loads(line_text)
                        if json_response.get('choices'):
                            content = json_response['choices'][0].get('delta', {}).get('content', '')
                            if content:
                                print(content, end='', flush=True)
                    except json.JSONDecodeError as e:
                        print(f"\nError decoding stream chunk: {str(e)}")
                        continue
                    except Exception as e:
                        print(f"\nError processing stream: {str(e)}")
                        continue
        except Exception as e:
            print(f"\nError in stream handling: {str(e)}")

    def get_model_info(self) -> Dict[str, Dict]:
        """Return information about available models"""
        return self.models

    def print_model_menu(self) -> None:
        """Print available models in a menu format"""
        print("\nAvailable Models:")
        print("=" * 80)
        
        # Search Models
        print("\nSearch Models (with web search):")
        print("-" * 40)
        for key, model in self.models.items():
            if model["type"] == "search":
                print(f"{key}. {model['name']}")
                print(f"   {model['description']}")
                if 'max_output_tokens' in model:
                    print(f"   Max output tokens: {model['max_output_tokens']}")
                print()
        
        # Reasoning Models
        print("\nReasoning Models (with web search):")
        print("-" * 40)
        for key, model in self.models.items():
            if model["type"] == "reasoning":
                print(f"{key}. {model['name']}")
                print(f"   {model['description']}")
                if 'features' in model:
                    print(f"   Features: {', '.join(model['features'])}")
                print()
        
        # Research Models
        print("\nResearch Models (with web search):")
        print("-" * 40)
        for key, model in self.models.items():
            if model["type"] == "research":
                print(f"{key}. {model['name']}")
                print(f"   {model['description']}")
                if 'note' in model:
                    print(f"   Note: {model['note']}")
                print()
        
        # Offline Models
        print("\nOffline Models (no web search):")
        print("-" * 40)
        for key, model in self.models.items():
            if model["type"] == "offline":
                print(f"{key}. {model['name']}")
                print(f"   {model['description']}")
                if 'note' in model:
                    print(f"   Note: {model['note']}")
                print()
        
        print("=" * 80)
        print("\nModel Selection Guide:")
        print("- sonar: Best for quick factual queries and summaries")
        print("- sonar-pro: Best for complex queries and follow-ups")
        print("- sonar-reasoning: Best for quick problem-solving with search")
        print("- sonar-reasoning-pro: Best for complex reasoning tasks")
        print("- sonar-deep-research: Best for comprehensive research and reports")
        print("- r1-1776: Best for creative content without web search")
        print("\nFor detailed model information, visit: https://docs.perplexity.ai/models/model-cards")

def main():
    try:
        api = PerplexityAPI()
        
        while True:
            print("\nPerplexity API Test Menu")
            print("1. Test a model")
            print("2. Show available models")
            print("3. Verify web search capability")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                api.print_model_menu()
                model_choice = input("\nSelect a model (1-6): ")
                
                if model_choice not in api.models:
                    print("Invalid model choice!")
                    continue
                
                model = api.models[model_choice]["name"]
                prompt = input("\nEnter your prompt: ")
                
                # Advanced options
                use_advanced = input("\nUse advanced options? (y/n): ").lower() == 'y'
                
                if use_advanced:
                    system_prompt = input("Enter system prompt (press Enter for default): ") or "Be precise and concise."
                    temperature = float(input("Enter temperature (0.0-1.0, press Enter for 0.7): ") or "0.7")
                    max_tokens = input("Enter max tokens (press Enter for default): ")
                    max_tokens = int(max_tokens) if max_tokens else None
                    stream = input("Enable streaming? (y/n): ").lower() == 'y'
                    verify_web = input("Verify web search capability? (y/n): ").lower() == 'y'
                else:
                    system_prompt = "Be precise and concise."
                    temperature = 0.7
                    max_tokens = None
                    stream = False
                    verify_web = False

                print("\nSending request...")
                result = api.call_api(
                    prompt=prompt,
                    model=model,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=stream,
                    verify_web=verify_web
                )
                
                if result and not stream:
                    print("\nAPI Response:", json.dumps(result, indent=2))
                
            elif choice == "2":
                api.print_model_menu()
            
            elif choice == "3":
                api.print_model_menu()
                model_choice = input("\nSelect a model to verify web search (1-6): ")
                
                if model_choice not in api.models:
                    print("Invalid model choice!")
                    continue
                
                model = api.models[model_choice]["name"]
                print(f"\nVerifying web search capability for {model}...")
                
                if api.verify_web_search(model):
                    print(f"✓ {model} has web search capability")
                else:
                    print(f"✗ {model} does not have web search capability")
            
            elif choice == "4":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice! Please try again.")
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print("Full error traceback:")
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 