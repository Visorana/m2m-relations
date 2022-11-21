from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        scopes = []
        for form in self.forms:
            if form.cleaned_data['topic'] in scopes:
                raise ValidationError('Разделы не могут повторяться')
            scopes.append(form.cleaned_data['topic'])
        for form in self.forms:
            if form.cleaned_data['is_main']:
                count += 1
                if count > 1:
                    raise ValidationError('Основным может быть только один раздел')
        if count == 0:
            raise ValidationError('Должен быть хотя бы один основной раздел')
        return super().clean()


class RelationshipInline(admin.TabularInline):
    model = Scope
    formset = RelationshipInlineFormset
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at', 'image']
    inlines = [RelationshipInline]


@admin.register(Tag)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ['id', 'topic']
