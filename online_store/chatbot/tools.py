# tools.py
from core.models import product

def search_products(limit: int = 10) -> list[dict]:

    prd = product.objects.all()
    return [
        {"id": o.id, "name": o.name, "price": str(o.price)}
        for o in prd
    ]

def get_recommendations(max_price: float = None, name: str = None):
    """
        Return up to five products filtered by optional name and/or maximum price.

        Args:
            max_price: Maximum acceptable price, optional and can be None.
            name: Partial product name to search for, optional and can be None.
    """
    if name:
        prd = product.objects.filter(name__icontains=name)
    if max_price:
        prd = product.objects.filter(price__lte=max_price)

    return [{"id": i.id, "name": i.name, "price": float(i.price)} for i in prd[:5]]