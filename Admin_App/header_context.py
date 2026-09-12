from Admin_App.models import HeaderSettings


def header_settings(request):

    settings = HeaderSettings.objects.filter(
        is_active=True
    ).first()

    return {
        "header_settings": settings
    }