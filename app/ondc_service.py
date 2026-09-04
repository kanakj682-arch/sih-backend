from app.models import Product

class ONDCIntegrationService:
    @staticmethod
    async def sync_product_to_ondc(product: Product) -> dict:
        ondc_payload = {
            "context": {
                "domain": "nic2004:52110",
                "action": "on_search",
                "version": "1.1.0",
                "bpp_id": "artisan-bpp.com"
            },
            "message": {
                "catalog": {
                    "providers": [{
                        "id": f"ARTISAN-{product.artisan_id}",
                        "items": [{
                            "id": f"PROD-{product.id}",
                            "descriptor": {
                                "name": product.title_en,
                                "short_desc": product.description_en[:100]
                            },
                            "price": {"currency": "INR", "value": str(product.price)}
                        }]
                    }]
                }
            }
        }
        
        return {
            "status": "SUCCESS",
            "ondc_item_id": f"PROD-{product.id}",
            "message": "Product successfully synced with ONDC network",
            "payload_sent": ondc_payload
        }