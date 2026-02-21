from django.contrib import admin
from django import forms
from .models import Category, Producer, ProducerImage


admin.site.site_header = "Produtores Locais"
admin.site.site_title = "Produtores Locais"
admin.site.index_title = "Bem-vindo ao Painel de Controlo"


class ProducerImageInline(admin.TabularInline):
    """Inline for gallery images"""

    model = ProducerImage
    extra = 3
    fields = ["image", "caption", "order"]
    ordering = ["order"]


class ProducerAdminForm(forms.ModelForm):
    """Form for Producer model with custom widgets"""

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Categoria(s)",
    )

    class Meta:
        model = Producer
        fields = "__all__"
        widgets = {
            "products": forms.Textarea(
                attrs={"rows": 3, "placeholder": '["Queijo de Cabra", "Requeijão"]'}
            ),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial["categories"] = self.instance.categories.all()

    def save(self, commit=True):
        """Save the form and update categories"""
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
        
        # Update categories based on the form data
        if self.cleaned_data.get("categories"):
            instance.categories.set(self.cleaned_data["categories"])
        else:
            instance.categories.clear()
        
        return instance


class CategoryInline(admin.TabularInline):
    """Inline to add categories directly on producer"""
    model = Producer.categories.through
    extra = 1
    verbose_name = "Categoria"
    verbose_name_plural = "Categorias"


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    form = ProducerAdminForm
    inlines = [ProducerImageInline]
    
    raw_id_fields = ['categories']

    list_display = ["name", "get_categories", "city", "phone", "email", "is_active"]

    # Side filters
    list_filter = ["categories", "is_active", "city", "state", "created_at"]

    # Search fields
    search_fields = ["name", "description", "email", "phone", "city"]

    # Form sections
    fieldsets = [
        ("Informação Básica", {
            "fields": ["name", "categories", "description", "is_active"]  # 👈 Mudou de type para categories
        }),
        (
            "Contactos",
            {
                "fields": [("phone", "mobile_phone"), "email", "website"],
                "classes": ["wide"],
            },
        ),
        (
            "Morada",
            {
                "fields": [("street", "number"), ("city", "state"), "zip_code"],
                "classes": ["wide"],
            },
        ),
        ("Localização no Mapa", {
            "fields": ["latitude", "longitude"],
            "classes": ["wide"],
            "description": "Coordenadas para aparecer no mapa (opcional)"
        }),
        (
            "Redes Sociais",
            {
                "fields": [("facebook", "instagram"), ("twitter", "youtube"), "tiktok"],
                "classes": ["collapse"],
            },
        ),
        ("Imagem Principal", {"fields": ["main_image"], "classes": ["wide"]}),
        (
            "Produtos",
            {
                "fields": ["products"],
                "classes": ["wide"],
                "description": "Lista de produtos oferecidos (formato JSON)",
            },
        ),
        (
            "Metadados",
            {"fields": ["created_at", "updated_at"], "classes": ["collapse"]},
        ),
    ]

    # Read-only fields
    readonly_fields = ["created_at", "updated_at"]

    # Pagination
    list_per_page = 25

    # Default ordering
    ordering = ["name"]

    # Custom actions
    actions = ["activate_producers", "deactivate_producers"]

    # 👇 Método corrigido para mostrar categorias
    def get_categories(self, obj):
        """Returns categories as string"""
        return ", ".join([cat.name for cat in obj.categories.all()]) or "-"
    get_categories.short_description = "Categorias"
    get_categories.admin_order_field = "categories"

    def phone(self, obj):
        """Shows main or mobile phone"""
        return obj.phone or obj.mobile_phone or "-"
    phone.short_description = "Telefone"

    def email(self, obj):
        """Returns email"""
        return obj.email or "-"
    email.short_description = "Email"

    def city(self, obj):
        """Returns city"""
        return obj.city or "-"
    city.short_description = "Cidade"
    city.admin_order_field = "city"

    # Custom actions
    def activate_producers(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} produtores ativados.")
    activate_producers.short_description = "Ativar produtores selecionados"

    def deactivate_producers(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} produtores desativados.")
    deactivate_producers.short_description = "Desativar produtores selecionados"


@admin.register(ProducerImage)
class ProducerImageAdmin(admin.ModelAdmin):
    list_display = ["producer", "image", "caption", "order"]
    list_filter = ["producer"]
    search_fields = ["producer__name", "caption"]
    ordering = ["producer", "order"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ["name"]
    ordering = ["name"]