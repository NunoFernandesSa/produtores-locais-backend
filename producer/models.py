import uuid
from django.db import models
from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r"^\+?351?\d{9}$",
    message="Número de telefone deve estar no formato: '+351912345678' ou '912345678'",
)

email_regex = RegexValidator(
    regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    message="Email inválido",
)


class Producer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255, help_text="Nome do produtor", verbose_name="Nome"
    )
    type = models.JSONField(
        verbose_name="Tipo(s)",
        help_text='Selecione os tipos de produção (ex: "Legumes", "Fruta")',
        default=list,
        blank=True,
    )
    description = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição do produtor e seus produtos",
        blank=True,
    )
    phone = models.CharField(
        max_length=20,
        validators=[phone_regex],
        verbose_name="Telefone",
        blank=True,
        null=True,
    )
    mobile_phone = models.CharField(
        max_length=20,
        validators=[phone_regex],
        verbose_name="Telemóvel",
        blank=True,
        null=True,
    )
    email = models.EmailField(
        max_length=255,
        validators=[email_regex],
        verbose_name="Email",
        blank=True,
        null=True,
    )
    website = models.URLField(
        verbose_name="Site internet",
        max_length=255,
        blank=True,
        null=True,
    )
    street = models.CharField(
        max_length=200,
        verbose_name="Rua",
        blank=True,
        null=True,
    )
    number = models.CharField(
        max_length=20,
        verbose_name="Número",
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Cidade",
        default="",
        blank=True,
    )
    state = models.CharField(
        max_length=50,
        verbose_name="Distrito",
        default="",
        blank=True,
    )
    zip_code = models.CharField(
        max_length=10,
        verbose_name="Código Postal",
        blank=True,
        null=True,
        help_text="Formato: 1234-123",
    )
    facebook = models.URLField(
        verbose_name="Facebook",
        max_length=255,
        blank=True,
        null=True,
    )
    instagram = models.URLField(
        verbose_name="Instagram",
        max_length=255,
        blank=True,
        null=True,
    )
    twitter = models.URLField(
        verbose_name="Twitter",
        max_length=255,
        blank=True,
        null=True,
    )
    youtube = models.URLField(
        verbose_name="YouTube",
        max_length=255,
        blank=True,
        null=True,
    )
    tiktok = models.URLField(
        verbose_name="TikTok",
        max_length=255,
        blank=True,
        null=True,
    )
    main_image = models.ImageField(
        upload_to="producers/", verbose_name="Imagem principal", blank=True, null=True
    )
    products = models.JSONField(
        verbose_name="Produtos",
        help_text='Array de produtos: ["Queijo de Cabra", "Requeijão"]',
        default=list,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Produtor"
        verbose_name_plural = "Produtores"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["type"]),
            models.Index(fields=["city"]),
        ]

    def __str__(self):
        return self.name


class ProducerImage(models.Model):
    """Separated model for gallery images"""

    image = models.ImageField(upload_to="producers/gallery/", verbose_name="Imagem")
    caption = models.CharField(
        max_length=200,
        verbose_name="Legenda",
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    producer = models.ForeignKey(
        Producer,
        on_delete=models.CASCADE,
        related_name="gallery_images",
        verbose_name="Produtor",
    )

    class Meta:
        ordering = ["order", "uploaded_at"]
        verbose_name = "Imagem da galeria"
        verbose_name_plural = "Imagens da galeria"
        indexes = [
            models.Index(fields=["producer", "order"]),
        ]

    def __str__(self):
        return f"Imagem de {self.producer.name}"
