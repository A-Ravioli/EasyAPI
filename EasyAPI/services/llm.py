# This llm code came from databonsai and @alvin-r on github which was shown to me by a friend.

from tenacity import retry, wait_exponential, stop_after_attempt
from EasyAPI.utils.logs import logger
from abc import ABC, abstractmethod
from functools import wraps
from typing import Optional
from openai import OpenAI
from groq import Groq
import anthropic
import os


class LLMProvider(ABC):
    @abstractmethod
    def __init__(
        self,
        model: str = "",
        temperature: float = 0,
    ):
        """
        Initializes the LLMProvider with an API key and retry parameters.

        Parameters:

        model (str): The default model to use for text generation.
        temperature (float): The temperature parameter for text generation.
        """
        pass

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, max_tokens: int) -> str:
        """
        Generates a text completion using the provider's API, with a given system and user prompt.
        This method should be decorated with retry logic to handle temporary failures.

        Parameters:
        system_prompt (str): The system prompt to provide context or instructions for the generation.
        user_prompt (str): The user's prompt, based on which the text completion is generated.
        max_tokens (int): The maximum number of tokens to generate in the response.

        Returns:
        str: The generated text completion.
        """
        pass


class OpenAIProvider(LLMProvider):
    """
    A provider class to interact with OpenAI's API.
    Supports exponential backoff retries, since we'll often deal with large datasets.
    """

    def __init__(
        self,
        api_key: str = None,
        multiplier: int = 1,
        min_wait: int = 1,
        max_wait: int = 30,
        max_tries: int = 5,
        model: str = "gpt-4-turbo",
        temperature: float = 0,
    ):
        """
        Initializes the OpenAIProvider with an API key and retry parameters.

        Parameters:
        api_key (str): OpenAI API key.
        multiplier (int): The multiplier for the exponential backoff in retries.
        min_wait (int): The minimum wait time between retries.
        max_wait (int): The maximum wait time between retries.
        max_tries (int): The maximum number of attempts before giving up.
        model (str): The default model to use for text generation.
        temperature (float): The temperature parameter for text generation.
        """
        super().__init__()

        # Provider related configs
        if api_key:
            self.api_key = api_key
        else:
            if not self.api_key:
                raise ValueError("OpenAI API key not provided.")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        try:
            self.client.models.retrieve(model)
        except Exception as e:
            logger.warning(e.response.status_code)
            raise ValueError(f"Invalid OpenAI model: {model}") from e
        self.temperature = temperature
        self.input_tokens = 0
        self.output_tokens = 0

        # Retry related configs
        self.multiplier = multiplier
        self.min_wait = min_wait
        self.max_wait = max_wait
        self.max_tries = max_tries

    def retry_with_exponential_backoff(method):
        """
        Decorator to apply retry logic with exponential backoff to an instance method.
        It captures the 'self' context to access instance attributes for retry configuration.
        """

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            retry_decorator = retry(
                wait=wait_exponential(
                    multiplier=self.multiplier, min=self.min_wait, max=self.max_wait
                ),
                stop=stop_after_attempt(self.max_tries),
            )
            return retry_decorator(method)(self, *args, **kwargs)

        return wrapper

    @retry_with_exponential_backoff
    def generate(
        self, system_prompt: str, user_prompt: str, max_tokens=1000, json=False
    ) -> str:
        """
        Generates a text completion using OpenAI's API, with a given system and user prompt.
        This method is decorated with retry logic to handle temporary failures.

        Parameters:
        system_prompt (str): The system prompt to provide context or instructions for the generation.
        user_prompt (str): The user's prompt, based on which the text completion is generated.
        max_tokens (int): The maximum number of tokens to generate in the response.
        json (bool): Whether to use OpenAI's JSON response format.

        Returns:
        str: The generated text completion.
        """
        if not system_prompt:
            raise ValueError("System prompt is required.")
        if not user_prompt:
            raise ValueError("User prompt is required.")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{user_prompt}"},
                ],
                temperature=self.temperature,
                max_tokens=max_tokens,
                frequency_penalty=0,
                presence_penalty=0,
                response_format={"type": "json_object"} if json else {"type": "text"},
            )
            self.input_tokens += response.usage.prompt_tokens
            self.output_tokens += response.usage.completion_tokens
            return response.choices[0].message.content
        except Exception as e:
            logger.warning(f"Error occurred during generation: {str(e)}")
            raise


class AnthropicProvider(LLMProvider):
    """
    A provider class to interact with Anthropic's Claude API.
    Supports exponential backoff retries, since we'll often deal with large datasets.
    """

    def __init__(
        self,
        api_key: str = None,
        multiplier: int = 1,
        min_wait: int = 1,
        max_wait: int = 30,
        max_tries: int = 5,
        model: str = "claude-3-haiku-20240307",
        temperature: float = 0,
    ):
        """
        Initializes the ClaudeProvider with an API key and retry parameters.

        Parameters:
        api_key (str): Anthropic API key.
        multiplier (int): The multiplier for the exponential backoff in retries.
        min_wait (int): The minimum wait time between retries.
        max_wait (int): The maximum wait time between retries.
        max_tries (int): The maximum number of attempts before giving up.
        model (str): The default model to use for text generation.
        temperature (float): The temperature parameter for text generation.
        """
        super().__init__()

        # Provider related configs
        if api_key:
            self.api_key = api_key
        else:
            if not self.api_key:
                raise ValueError("Anthropic API key not provided.")
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.temperature = temperature
        self.input_tokens = 0
        self.output_tokens = 0

        # Retry related configs
        self.multiplier = multiplier
        self.min_wait = min_wait
        self.max_wait = max_wait
        self.max_tries = max_tries

    def retry_with_exponential_backoff(method):
        """
        Decorator to apply retry logic with exponential backoff to an instance method.
        It captures the 'self' context to access instance attributes for retry configuration.
        """

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            retry_decorator = retry(
                wait=wait_exponential(
                    multiplier=self.multiplier, min=self.min_wait, max=self.max_wait
                ),
                stop=stop_after_attempt(self.max_tries),
            )
            return retry_decorator(method)(self, *args, **kwargs)

        return wrapper

    @retry_with_exponential_backoff
    def generate(
        self, system_prompt: str, user_prompt: str, max_tokens=1000, json: bool = False
    ) -> str:
        """
        Generates a text completion using Anthropic's Claude API, with a given system and user prompt.
        This method is decorated with retry logic to handle temporary failures.

        Parameters:
        system_prompt (str): The system prompt to provide context or instructions for the generation.
        user_prompt (str): The user's prompt, based on which the text completion is generated.
        max_tokens (int): The maximum number of tokens to generate in the response.

        Returns:
        str: The generated text completion.
        """
        try:
            if not system_prompt:
                raise ValueError("System prompt is required.")
            if not user_prompt:
                raise ValueError("User prompt is required.")
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=self.temperature,
                system=f"{system_prompt}",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_prompt,
                            }
                        ],
                    }
                ],
            )
            self.input_tokens += response.usage.input_tokens
            self.output_tokens += response.usage.output_tokens
            return response.content[0].text
        except Exception as e:
            logger.warning(f"Error occurred during generation: {str(e)}")
            raise


class GroqProvider(LLMProvider):
    """
    A provider class to interact with Groq's API.
    Supports exponential backoff retries, since we'll often deal with large datasets.
    """

    def __init__(
        self,
        api_key: str = None,
        multiplier: int = 1,
        min_wait: int = 1,
        max_wait: int = 30,
        max_tries: int = 5,
        model: str = "groq-3",
        temperature: float = 0,
    ):
        """
        Initializes the GroqProvider with an API key and retry parameters.

        Parameters:
        api_key (str): Groq API key.
        multiplier (int): The multiplier for the exponential backoff in retries.
        min_wait (int): The minimum wait time between retries.
        max_wait (int): The maximum wait time between retries.
        max_tries (int): The maximum number of attempts before giving up.
        model (str): The default model to use for text generation.
        temperature (float): The temperature parameter for text generation.
        """
        super().__init__()

        # Provider related configs
        if api_key:
            self.api_key = api_key
        else:
            if not self.api_key:
                raise ValueError("Groq API key not provided.")
        self.model = model
        self.client = Groq(api_key=self.api_key)
        self.temperature = temperature
        self.input_tokens = 0
        self.output_tokens = 0

        # Retry related configs
        self.multiplier = multiplier
        self.min_wait = min_wait
        self.max_wait = max_wait
        self.max_tries = max_tries

    def retry_with_exponential_backoff(method):
        """
        Decorator to apply retry logic with exponential backoff to an instance method.
        It captures the 'self' context to access instance attributes for retry configuration.
        """

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            retry_decorator = retry(
                wait=wait_exponential(
                    multiplier=self.multiplier, min=self.min_wait, max=self.max_wait
                ),
                stop=stop_after_attempt(self.max_tries),
            )
            return retry_decorator(method)(self, *args, **kwargs)

        return wrapper

    @retry_with_exponential_backoff
    def generate(self, system_prompt: str, user_prompt: str, max_tokens: int) -> str:
        """
        Generates a text completion using Groq's API, with a given system and user prompt.
        This method is decorated with retry logic to handle temporary failures.

        Parameters:
        system_prompt (str): The system prompt to provide context or instructions for the generation.
        user_prompt (str): The user's prompt, based on which the text completion is generated.
        max_tokens (int): The maximum number of tokens to generate in the response.

        Returns:
        str: The generated text completion.
        """
        try:
            if not system_prompt:
                raise ValueError("System prompt is required.")
            if not user_prompt:
                raise ValueError("User prompt is required.")
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=self.temperature,
                system=f"{system_prompt}",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_prompt,
                            }
                        ],
                    }
                ],
            )
            self.input_tokens += response.usage.input_tokens
            self.output_tokens += response.usage.output_tokens
            return response.content[0].text
        except Exception as e:
            logger.warning(f"Error occurred during generation: {str(e)}")
            raise
