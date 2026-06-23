from typing import TypeVar, Generic, Type, Optional, List
from django.db.models import Model

T = TypeVar('T', bound=Model)

class BaseRepository(Generic[T]):
    """
    Base repository layer.
    All database operations should be abstracted through repositories.
    """
    model: Type[T]

    def __init__(self):
        if not hasattr(self, 'model'):
            raise ValueError("Repository must define 'model' attribute")

    def get_by_id(self, id: int) -> Optional[T]:
        try:
            return self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return None

    def get_all(self) -> List[T]:
        return list(self.model.objects.all())

    def create(self, **kwargs) -> T:
        return self.model.objects.create(**kwargs)

    def delete(self, id: int) -> bool:
        instance = self.get_by_id(id)
        if instance:
            instance.delete()
            return True
        return False
