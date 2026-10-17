import csv
import io
from datetime import timedelta

from django.db import transaction
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from online_store.permissions import IsSellerAccount
from . import models, serializer

LOW_STOCK_THRESHOLD = 5
IMPORT_MAX_BYTES = 1024 * 1024
IMPORT_MAX_ROWS = 500


class SellerOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsSellerAccount]


def csv_safe(value):
    """Stop spreadsheet formula injection: a cell starting with = + - @ would run as a formula in Excel."""
    text = '' if value is None else str(value)
    return "'" + text if text[:1] in ('=', '+', '-', '@', '\t', '\r') else text


def csv_response(filename, header, rows):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write('﻿')  # BOM so Excel reads Arabic text correctly
    writer = csv.writer(response)
    writer.writerow(header)
    for row in rows:
        writer.writerow([csv_safe(cell) for cell in row])
    return response


class SellerStatsView(SellerOnlyView):
    def get(self, request):
        seller = request.user.seller
        now = timezone.now()

        def revenue(days):
            total = models.OrderStatusEvent.objects.filter(
                order__seller=seller, status='delivered', created__gte=now - timedelta(days=days),
            ).aggregate(t=Sum('order__total_value'))['t']
            return total or 0

        by_status = dict(models.order.objects.filter(seller=seller)
                         .values_list('order_status').annotate(n=Count('id')))
        top = (models.order_item.objects.filter(order__seller=seller).exclude(order__order_status='cancelled')
               .values('product_id', 'product__name').annotate(units=Sum('quantity')).order_by('-units')[:5])
        low = (models.product.objects.filter(seller=seller, inventory__lte=LOW_STOCK_THRESHOLD)
               .order_by('inventory', 'id').values('id', 'name', 'inventory')[:10])
        return Response({
            'revenue_7': revenue(7),
            'revenue_30': revenue(30),
            'orders_by_status': by_status,
            'top_products': [{'id': t['product_id'], 'name': t['product__name'], 'units': t['units']} for t in top],
            'low_stock': list(low),
            'low_stock_threshold': LOW_STOCK_THRESHOLD,
        })


class ExportOrdersView(SellerOnlyView):
    def get(self, request):
        orders = (models.order.objects.filter(seller=request.user.seller)
                  .select_related('customer__user').annotate(items=Sum('order_item__quantity')).order_by('-id'))
        rows = ((o.id, o.creation_date.strftime('%Y-%m-%d %H:%M'), str(o.customer) if o.customer else '',
                 o.order_status, o.payment_status, o.location, o.total_value, o.items or 0) for o in orders)
        return csv_response('orders.csv',
                            ['order_id', 'date', 'customer', 'status', 'payment', 'location', 'total', 'items'], rows)


class ExportEarningsView(SellerOnlyView):
    def get(self, request):
        entries = models.LedgerEntry.objects.filter(seller=request.user.seller).order_by('-created', '-id')
        rows = ((e.created.strftime('%Y-%m-%d %H:%M'), e.kind, e.order_id or '', e.amount) for e in entries)
        return csv_response('earnings.csv', ['date', 'type', 'order_id', 'amount'], rows)


class ProductImportView(SellerOnlyView):
    """CSV columns: name, price, inventory (required); description, category (category slug) optional.
    All rows are checked first. If any row is bad nothing is created, so the file can be fixed and re-sent."""

    def post(self, request):
        upload = request.FILES.get('file')
        if upload is None:
            return Response({'detail': 'Attach a CSV file in the "file" field.'}, status=status.HTTP_400_BAD_REQUEST)
        if upload.size > IMPORT_MAX_BYTES:
            return Response({'detail': 'File is too large (max 1 MB).'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            text = upload.read().decode('utf-8-sig')
        except UnicodeDecodeError:
            return Response({'detail': 'File must be UTF-8 encoded.'}, status=status.HTTP_400_BAD_REQUEST)

        reader = csv.DictReader(io.StringIO(text))
        missing = {'name', 'price', 'inventory'} - set(reader.fieldnames or [])
        if missing:
            return Response({'detail': 'Missing column(s): ' + ', '.join(sorted(missing))}, status=status.HTTP_400_BAD_REQUEST)
        rows = list(reader)
        if not rows:
            return Response({'detail': 'The file has no rows.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(rows) > IMPORT_MAX_ROWS:
            return Response({'detail': f'Too many rows (max {IMPORT_MAX_ROWS}).'}, status=status.HTTP_400_BAD_REQUEST)

        categories = {c.slug: c.id for c in models.Category.objects.all()}
        serializers_, errors = [], []
        for line, row in enumerate(rows, start=2):  # line 1 is the header
            slug = (row.get('category') or '').strip()
            if slug and slug not in categories:
                errors.append({'line': line, 'errors': {'category': [f'Unknown category "{slug}".']}})
                continue
            item = serializer.ProductSerialzer(data={
                'name': (row.get('name') or '').strip(),
                'description': (row.get('description') or '').strip(),
                'price': (row.get('price') or '').strip(),
                'inventory': (row.get('inventory') or '').strip(),
                'category': categories.get(slug),
            }, context={'request': request})
            if item.is_valid():
                serializers_.append(item)
            else:
                errors.append({'line': line, 'errors': item.errors})

        if errors:
            return Response({'detail': 'No products were created. Fix these rows and upload again.', 'errors': errors[:50]},
                            status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            for item in serializers_:
                item.save()
        return Response({'created': len(serializers_)}, status=status.HTTP_201_CREATED)
