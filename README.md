# 🌿 Local Producers Directory API

![Django](https://img.shields.io/badge/Django-6.0.2-092E20?style=for-the-badge&logo=django)
![Django REST](https://img.shields.io/badge/DRF-3.15.2-ff1709?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=json-web-tokens)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python)

## 📋 About The API

RESTful API built with Django to manage a directory of local producers from the Minho region, Portugal. Provides endpoints for querying and managing producers, their products, location, and contact information.

### 🎯 API Objectives

- Serve structured data of local producers
- Enable filtering by product type and location
- Manage image uploads (products and producers)
- Provide interactive API documentation

## 🏗️ Project Structure

```
back-end/
├── core/                  # Main configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL routes
│   └── asgi.py            # ASGI configuration
│
├── producer/              # Main app
│   ├── models.py          # Data models
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # API routes
│   └── admin.py           # Admin configuration
│
├── media/                 # Image uploads
│   ├── producers/         # Main producer images
│   └── gallery/           # Gallery images
│
├── requirements.txt       # Dependencies
└── manage.py              # Django management
```

## 🔌 API Endpoints

### Producers

| Method | Endpoint               | Description          |
| ------ | ---------------------- | -------------------- |
| GET    | `/api/producers/`      | List all producers   |
| GET    | `/api/producers/{id}/` | Get producer details |
| POST   | `/api/producers/`      | Create new producer  |
| PUT    | `/api/producers/{id}/` | Update producer      |
| PATCH  | `/api/producers/{id}/` | Partial update       |
| DELETE | `/api/producers/{id}/` | Delete producer      |

## 🚀 Technologies Used

- **Django 6.0** - High-level Python web framework
- **Django REST Framework 3.15** - Powerful API toolkit
- **PostgreSQL 16** - Production database
- **SQLite** - Development database
- **Swagger/OpenAPI** - Automatic API documentation
- **Pillow** - Image processing

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.13+
- PostgreSQL (optional, SQLite works for development)
- Git

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

Nuno Fernandes de Sa - n.fernandes.contact@gmail.com

Project Link: [https://github.com/NunoFernandesSa/produtores-locais-backend](https://github.com/NunoFernandesSa/produtores-locais-backend)

## 🙏 Acknowledgments

- Django and Django REST Framework communities
- All local producers from Minho region for inspiration
- Contributors and testers

---

**⭐ Star this repository if you find it useful!**
