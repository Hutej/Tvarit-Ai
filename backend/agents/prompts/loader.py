import os
from typing import Dict
from pathlib import Path
from agents.prompts.templates import PromptTemplate
from agents.prompts.types import PromptVariable
from agents.prompts.exceptions import TemplateNotFoundException

class PromptLoader:
    """
    Loads prompt templates from the filesystem.
    """
    def __init__(self, base_dir: str = None):
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path(__file__).parent

    def load_template(self, category: str, template_name: str) -> PromptTemplate:
        """
        Load a specific template by reading system.txt and user.txt from
        agents/prompts/{category}/
        """
        target_dir = self.base_dir / category
        if not target_dir.exists():
            raise TemplateNotFoundException(f"Category directory not found: {category}")
            
        system_file = target_dir / "system.txt"
        user_file = target_dir / "user.txt"
        
        if not system_file.exists() or not user_file.exists():
            raise TemplateNotFoundException(f"Missing system.txt or user.txt in {target_dir}")
            
        with open(system_file, 'r', encoding='utf-8') as f:
            system_template = f.read()
            
        with open(user_file, 'r', encoding='utf-8') as f:
            user_template = f.read()
            
        variables = [
            PromptVariable(name="raw_text", is_required=True),
            PromptVariable(name="document_type", is_required=False, default_value="UNKNOWN")
        ]
            
        return PromptTemplate(
            name=f"{category}_{template_name}",
            system_template=system_template,
            user_template=user_template,
            variables=variables,
            temperature=0.0
        )
        
    def list_categories(self) -> list[str]:
        if not self.base_dir.exists():
            return []
        return [d.name for d in self.base_dir.iterdir() if d.is_dir() and not d.name.startswith('_')]
