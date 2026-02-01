"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """Faz pull do prompt v1 do LangSmith Hub e retorna como dict."""
    prompt_name = "leonanluppi/bug_to_user_story_v1"

    print(f"Puxando prompt: {prompt_name}")
    prompt = hub.pull(prompt_name)
    print(f"   ✓ Prompt carregado com sucesso")

    # Extrair mensagens do ChatPromptTemplate
    messages = prompt.messages
    system_prompt = ""
    user_prompt = ""

    for msg in messages:
        if msg.__class__.__name__ in ("SystemMessagePromptTemplate", "SystemMessage"):
            system_prompt = msg.prompt.template if hasattr(msg, "prompt") else str(msg.content)
        elif msg.__class__.__name__ in ("HumanMessagePromptTemplate", "HumanMessage"):
            user_prompt = msg.prompt.template if hasattr(msg, "prompt") else str(msg.content)

    prompt_data = {
        "bug_to_user_story_v1": {
            "description": "Prompt para converter relatos de bugs em User Stories",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": "v1",
            "tags": ["bug-analysis", "user-story", "product-management"],
        }
    }

    return prompt_data


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    try:
        prompt_data = pull_prompts_from_langsmith()

        output_path = "prompts/bug_to_user_story_v1.yml"
        if save_yaml(prompt_data, output_path):
            print(f"   ✓ Prompt salvo em {output_path}")
            return 0
        else:
            print("   ❌ Erro ao salvar prompt")
            return 1

    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
