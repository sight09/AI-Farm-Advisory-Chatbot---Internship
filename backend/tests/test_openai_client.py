import unittest

from common.core.openai_client import embed_texts, single_embed, chat_completion

class TestOpenAIClient(unittest.IsolatedAsyncioTestCase):

    async def test_embed_texts(self):
        texts = ["Hello, world!", "Testing embeddings."]
        embeddings = await embed_texts(texts)
        self.assertEqual(len(embeddings), 2)
        self.assertEqual(len(embeddings[0]), len(embeddings[1]))  # Assuming same dimension

    async def test_single_embed(self):
        text = "Hello, world!"
        embedding = await single_embed(text)
        self.assertIsInstance(embedding, list)
        self.assertGreater(len(embedding), 0)

    async def test_chat_completion(self):
        system_prompt = "You are a helpful assistant."
        messages = [{"role": "user", "content": "What is the capital of France?"}]
        response = await chat_completion(system_prompt, messages)
        self.assertIsInstance(response, str)
        self.assertIn("Paris", response)  # Assuming the model responds correctly

