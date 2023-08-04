from django.contrib.sitemaps import Sitemap
from shopapp.models import Product


class ShopSitemap(Sitemap):
    changefreq = 'never'
    priority = 1

    def items(self):
        return (
            Product.objects.filter(archived=False).order_by('pk')
        )

    def lastmod(self, item: Product):
        return item.created_at
