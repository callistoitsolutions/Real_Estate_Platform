# Main_App/context_processors.py
from seo.models import SeoMetaTag

def global_seo(request):
    """
    Automatically fetches SEO data for static pages (Home, About, Contact)
    based on the URL name.
    """
    # Get the name of the current URL pattern (e.g., 'index', 'Contact_Us')
    url_name = request.resolver_match.url_name if request.resolver_match else ''
    
    try:
        # Look for a matching SEO record in your SeoMetaTag table
        seo_data = SeoMetaTag.objects.get(page_name=url_name)
        return {'global_seo': seo_data}
    except SeoMetaTag.DoesNotExist:
        # If no specific SEO record exists, return None to trigger fallbacks
        return {'global_seo': None}