from google import genai


class GeminiClient:
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize Gemini API client.

        Args:
            api_key (str): Google Gemini API key. If not provided, will use GEMINI_API_KEY env variable.
            model (str): Default Gemini model to use.
        """
        self.api_key = api_key
        self.model = model
        if not self.api_key:
            raise ValueError("api_key is required. Set GEMINI_API_KEY in `.env` and pass api_key argument.")
        if not self.model:
            raise ValueError("model is required. Set GEMINI_MODEL in `config.py` and pass model argument.")

        self.client = genai.Client(api_key=self.api_key)

    def generate_text(self, prompt: str) -> str:
        """
        Generate text response for a given prompt.

        Args:
            prompt (str): Input prompt text.
            kwargs: Additional model configuration options.

        Returns:
            str: Generated text response.
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=[{"parts": [{"text": prompt}]}]
        )
        return getattr(response, "text", "")
