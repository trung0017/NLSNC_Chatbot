from setuptools import setup, find_packages

setup(
    name="order_chatbot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.1.0",
        "langchain-community",
        "langchain-google-vertexai",
        "google-cloud-aiplatform",
        "mysql-connector-python",
        "python-dotenv",
        "fastapi",
        "uvicorn",
        "pydantic",
        "python-multipart",
        "requests",
        "aiohttp",
        "openai",
        "tiktoken",
    ],
) 