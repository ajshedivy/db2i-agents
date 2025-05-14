import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the Python path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agno.models.ollama import Ollama
from agno.models.openai import OpenAIChat
try:
    from agno.models.anthropic import Anthropic
except ImportError:
    pass
from agno.models.ibm import WatsonX

from src.db2i_shared_utils.cli import get_model


class TestGetModel(unittest.TestCase):
    
    @patch('src.db2i_shared_utils.cli.dotenv_values')
    def test_default_model(self, mock_dotenv):
        # Test default model when model_id is None
        mock_dotenv.return_value = {}
        model = get_model(None)
        self.assertIsInstance(model, Ollama)
        self.assertEqual(model.id, "qwen2.5:latest")
    
    @patch('src.db2i_shared_utils.cli.dotenv_values')
    def test_invalid_format(self, mock_dotenv):
        # Test handling of invalid format (no colon)
        mock_dotenv.return_value = {}
        model = get_model("invalidformat")
        self.assertIsInstance(model, Ollama)
        self.assertEqual(model.id, "qwen2.5:latest")
    
    @patch('src.db2i_shared_utils.cli.dotenv_values')
    def test_ollama_model(self, mock_dotenv):
        # Test Ollama model
        mock_dotenv.return_value = {}
        model = get_model("ollama:llama2")
        self.assertIsInstance(model, Ollama)
        self.assertEqual(model.id, "llama2")
    
    @patch('src.db2i_shared_utils.cli.dotenv_values')
    def test_openai_model(self, mock_dotenv):
        # Test OpenAI model
        mock_dotenv.return_value = {"OPENAI_API_KEY": "test-key"}
        model = get_model("openai:gpt-4o")
        self.assertIsInstance(model, OpenAIChat)
        self.assertEqual(model.id, "gpt-4o")
        self.assertEqual(model.api_key, "test-key")
    
    @patch('src.db2i_shared_utils.cli.dotenv_values')
    def test_openai_missing_key(self, mock_dotenv):
        # Test OpenAI model with missing API key
        mock_dotenv.return_value = {}
        with self.assertRaises(ValueError) as context:
            get_model("openai:gpt-4o")
        self.assertIn("OPENAI_API_KEY", str(context.exception))
    
    # @patch('src.db2i_shared_utils.cli.dotenv_values')
    # def test_anthropic_model(self, mock_dotenv):
    #     # Test Anthropic model
    #     mock_dotenv.return_value = {"ANTHROPIC_API_KEY": "test-key"}
    #     model = get_model("anthropic:claude-3-sonnet")
    #     self.assertIsInstance(model, Anthropic)
    #     self.assertEqual(model.id, "claude-3-sonnet")
    #     self.assertEqual(model.api_key, "test-key")
    
    @patch('src.db2i_shared_utils.cli.dotenv_values')
    def test_watsonx_model(self, mock_dotenv):
        # Test WatsonX model
        mock_dotenv.return_value = {
            "IBM_WATSONX_API_KEY": "test-key",
            "IBM_WATSONX_PROJECT_ID": "test-project",
            "IBM_WATSONX_BASE_URL": "https://test-url.com"
        }
        model = get_model("watsonx:granite-13b")
        self.assertIsInstance(model, WatsonX)
        self.assertEqual(model.id, "granite-13b")
        self.assertEqual(model.api_key, "test-key")
        self.assertEqual(model.project_id, "test-project")
        self.assertEqual(model.url, "https://test-url.com")
    
    @patch('src.db2i_shared_utils.cli.dotenv_values')
    def test_unsupported_provider(self, mock_dotenv):
        # Test unsupported provider
        mock_dotenv.return_value = {}
        model = get_model("unsupported:model")
        self.assertIsInstance(model, Ollama)
        self.assertEqual(model.id, "qwen2.5:latest")


if __name__ == '__main__':
    unittest.main()