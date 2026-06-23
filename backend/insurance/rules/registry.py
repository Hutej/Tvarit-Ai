from typing import Dict, Type, List, Optional
from insurance.rules.base import Rule
from insurance.rules.exceptions import RuleRegistrationException

class RuleRegistry:
    """
    Registry for managing validation rules.
    """
    _rules: Dict[str, Type[Rule]] = {}

    @classmethod
    def register(cls, rule_cls: Type[Rule]) -> None:
        try:
            # Instantiate to get the ID, we register by class but use instance for ID retrieval
            instance = rule_cls()
            rule_id = instance.rule_id
        except Exception as e:
            raise RuleRegistrationException(f"Failed to instantiate rule {rule_cls.__name__} for registration: {e}")

        if rule_id in cls._rules:
            raise RuleRegistrationException(f"Rule '{rule_id}' is already registered.")
        if not issubclass(rule_cls, Rule):
            raise RuleRegistrationException(f"Class '{rule_cls.__name__}' must inherit from Rule.")
        
        cls._rules[rule_id] = rule_cls

    @classmethod
    def get_all_rules(cls) -> List[Type[Rule]]:
        return list(cls._rules.values())
        
    @classmethod
    def clear(cls):
        cls._rules.clear()
