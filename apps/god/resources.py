from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from apps.god.models import Domains, God


class DomainResources(resources.ModelResource):
    """ Import/export csf files in admin panel """

    class Meta:
        model = Domains

    def skip_row(self, instance, original, row, import_validation_errors=None):
        if Domains.objects.filter(name=instance.name).exists():
            return True
        return False


class GodResource(resources.ModelResource):
    """ Import/export csf files in admin panel """

    domain = fields.Field(
        column_name="domain",
        attribute="domain",
        widget=ManyToManyWidget(model=Domains, field="name")
    )

    class Meta:
        model = God

    def skip_row(self, instance, original, row, import_validation_errors=None):
        if God.objects.filter(question=instance.question).exists():
            return True
        return False
