"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data = load_prompts("prompts/bug_to_user_story_v2.yml")
        self.prompt = self.data["bug_to_user_story_v2"]

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in self.prompt
        assert self.prompt["system_prompt"].strip() != ""

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system = self.prompt["system_prompt"].lower()
        assert "product manager" in system or "você é" in system

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system = self.prompt["system_prompt"].lower()
        assert "markdown" in system or "user story" in system or "como um" in system

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system = self.prompt["system_prompt"]
        assert "Exemplo" in system or "exemplo" in system
        assert "Input" in system or "input" in system or "Output" in system or "output" in system

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system = self.prompt["system_prompt"]
        assert "[TODO]" not in system
        assert "TODO" not in system

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = self.prompt.get("techniques_applied", [])
        assert len(techniques) >= 2, f"Apenas {len(techniques)} técnicas listadas, mínimo é 2"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
