from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
import time

class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Try fetching cached data
        products = cache.get("all_products")
        if not products:
            # Simulate expensive DB call
            time.sleep(15)  # <-- to simulate slowness
            products = [
                {"id": 1, "name": "Laptop"},
                {"id": 2, "name": "Phone"},
            ]
            cache.set("all_products", products, timeout=10)  
            print("data accessed from the the database")
        else:
            print("data accessed from the the cache memory")

        return Response({
            "user": request.user.username,
            "products": products,
        })
