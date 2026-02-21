from django.contrib import admin
from django import forms
from .models import Producer, ProducerImage


TYPE_CHOICES = [
    ("legumes", "Legumes"),
    ("fruta", "Fruta"),
    ("vinho", "Vinho"),
    ("queijo", "Queijo"),
    ("mel", "Mel"),
    ("artesanato", "Artesanato"),
    ("pao", "Pão"),
    ("azeite", "Azeite"),
    ("conservas", "Conservas"),
    ("carnes", "Carnes"),
]

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

    type = forms.MultipleChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Tipo(s)",
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
        if self.instance and self.instance.type:
            # Convert json to list of values
            if isinstance(self.instance.type, list):
                self.initial["type"] = [t.lower() for t in self.instance.type]
            elif isinstance(self.instance.type, str):
                self.initial["type"] = [self.instance.type.lower()]

    def clean_type(self):
        """Converts the list of checkboxes back to JSON"""
        data = self.cleaned_data.get("type", [])
        return list(data) if data else []


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    form = ProducerAdminForm
    inlines = [ProducerImageInline]

    list_display = ["name", "get_types", "city", "phone", "email", "is_active"]

    # Side filters
    list_filter = ["is_active", "city", "state", "created_at"]

    # Search fields
    search_fields = ["name", "description", "email", "phone", "city"]

    # Form sections
    fieldsets = [
        ("Informação Básica", {"fields": ["name", "type", "description", "is_active"]}),
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

    # Methods for list_display
    def get_types(self, obj):
        """Formats type field for display"""
        if isinstance(obj.type, list):
            return ", ".join(obj.type[:3]) + ("..." if len(obj.type) > 3 else "")
        return obj.type

    get_types.short_description = "Tipos"
    get_types.admin_order_field = "type"

    def phone(self, obj):
        """Shows main or mobile phone"""
        return obj.phone or obj.mobile_phone

    phone.short_description = "Telefone"

    def email(self, obj):
        """Returns email"""
        return obj.email

    email.short_description = "Email"

    def city(self, obj):
        """Returns city"""
        return obj.city

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
