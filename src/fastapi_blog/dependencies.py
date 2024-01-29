from fastapi_blog.config import load_app_config


def get_config(dotenv_path: str):
    return load_app_config(dotenv_path)
