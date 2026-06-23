from string import Template
from typing import Type
from pydantic import BaseModel
from documents.parser.types import ParserResult
from documents.constants import DocumentType
from agents.prompts.templates import PromptTemplate
from agents.prompts.types import PromptPackage, PromptContext, PromptMetadata
from agents.prompts.exceptions import VariableMissingException

class PromptBuilder:
    """
    Builder class for injecting variables into templates to create a PromptPackage.
    """
    
    @staticmethod
    def build(
        template: PromptTemplate, 
        parser_result: ParserResult, 
        document_type: DocumentType,
        extra_variables: dict = None
    ) -> PromptPackage:
        extra_variables = extra_variables or {}
        
        # Combine parser result text and extra variables
        context_vars = {
            "raw_text": parser_result.raw_text,
            "document_type": document_type.value,
            **extra_variables
        }
        
        # Validate required variables
        for var in template.variables:
            if var.is_required and var.name not in context_vars:
                if var.default_value is not None:
                    context_vars[var.name] = var.default_value
                else:
                    raise VariableMissingException(f"Missing required variable: {var.name}")

        try:
            # Inject variables
            sys_template = Template(template.system_template)
            system_prompt = sys_template.safe_substitute(**context_vars)
            
            usr_template = Template(template.user_template)
            user_prompt = usr_template.safe_substitute(**context_vars)
            
            # Append instructions and examples if present
            if template.instructions:
                system_prompt += f"\n\nInstructions:\n{template.instructions}"
                
            if template.examples:
                system_prompt += "\n\nExamples:\n" + "\n".join(template.examples)

            return PromptPackage(
                system_prompt=system_prompt.strip(),
                user_prompt=user_prompt.strip(),
                response_schema=template.output_schema,
                metadata=template.metadata
            )
        except Exception as e:
            raise VariableMissingException(f"Failed to build prompt: {str(e)}")
