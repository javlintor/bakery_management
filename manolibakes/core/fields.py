from django.db import models


class TitleCaseCharField(models.CharField):
    def pre_save(self, model_instance: models.Model, add: bool) -> str | None:
        value = getattr(model_instance, self.attname)
        if value is not None:
            value = value.title()
            setattr(model_instance, self.attname, value)
        return value