from django.db import models
from django.db.models import Max

# Create your models here.
class Widget(models.Model):
    index = models.IntegerField(null=True, unique=True)
    value = models.CharField(max_length=200, default='')
    deleted = models.BooleanField(default=False)
    create_version = models.IntegerField(default=0)
    modify_version = models.IntegerField(default=0)
    
    @classmethod
    def version(cls):
        return Widget.objects.all() \
            .aggregate(Max('modify_version'))['modify_version__max'] or 0

    @classmethod
    def max_index(cls):
        return Widget.objects.all().aggregate(Max('index'))['index__max'] or 0
    
    @classmethod
    def changes_since_version(cls, version):
        widgets = Widget.objects.filter(modify_version__gt=version)
        changes = []
        for widget in widgets:
            changes.append({
                'index': widget.index,
                'value': widget.value,
                'deleted': widget.deleted,
            })
        return changes 
        
    @classmethod
    def widget_and_index(cls, index, version):
        try:
            widget = Widget.objects.get(index=index)
            if widget.create_version <= version:
                return widget, index
            else:
                return None, Widget.max_index() + 1
        except Widget.DoesNotExist:
            return None, index
    
    @classmethod
    def apply_changes(cls, client_version, changes):
        version = Widget.version() + 1
        moves = []
        for change in changes:
            index = change['index']
            value = change['value']
            deleted = change['deleted']
            widget, new_idx = Widget.widget_and_index(index, client_version)
            if new_idx != index:
                moves.append({ 'from': index, 'to': new_idx })
                index = new_idx
            if not widget:
                widget = Widget()
                widget.index = index
                widget.create_version = version
            if client_version < widget.modify_version:
                widget = None
            if widget:
                widget.value = value
                widget.deleted = deleted
                widget.modify_version = version
                widget.save()
        return moves
    
    @classmethod
    def sync_with_client(cls, client_patch):
        client_version = client_patch['clientVersion']
        client_changes = client_patch['clientChanges']
        return {
            'serverVersion': Widget.version(),
            'serverChanges': Widget.changes_since_version(client_version),
            'moves': Widget.apply_changes(client_version, client_changes),
        }
