import json
from typing import Optional
from app.config import settings

class AICatalogService:
    @staticmethod
    async def process_product_catalog(
        image_bytes: bytes, 
        raw_text_or_transcript: Optional[str] = None, 
        source_language: str = "hi"
    ) -> dict:
        if not settings.GEMINI_API_KEY:
            # Fallback mock response for testing
            return {
                "title_en": "Handcrafted Terracotta Clay Water Jug",
                "title_hi": "हस्तनिर्मित मिट्टी का मटका",
                "description_en": "Authentic eco-friendly terracotta water jug crafted by traditional village artisans. Natural cooling properties.",
                "description_hi": "पारंपरिक ग्रामीण कारीगरों द्वारा बनाया गया प्रामाणिक मिट्टी का मटका। प्राकृतिक ठंडक प्रदान करता है।",
                "suggested_category": "Home & Handicrafts",
                "detected_craft_type": "Terracotta Pottery",
                "extracted_features": {
                    "material": "Clay / Terracotta",
                    "color": "Earthy Brown"
                },
                "seo_tags": ["handicraft", "terracotta", "handmade", "pottery"]
            }

        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Analyze the product image and artisan input: "{raw_text_or_transcript or ''}".
            Artisan language: {source_language}.

            Return strictly valid JSON:
            {{
                "title_en": "SEO English Title",
                "title_hi": "SEO Hindi Title",
                "description_en": "English Description",
                "description_hi": "Hindi Description",
                "suggested_category": "Category Name",
                "detected_craft_type": "Craft Type",
                "extracted_features": {{"material": "", "color": ""}},
                "seo_tags": ["tag1", "tag2"]
            }}
            """
            image_part = {
                "mime_type": "image/jpeg", 
                "data": image_bytes}
            response = model.generate_content([prompt, image_part])
            
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            raise RuntimeError(f"AI Cataloging Failed: {str(e)}")