#!/usr/bin/env python3
"""
Script để cào dữ liệu laptop từ thegioididong.com
Sử dụng Playwright để crawl dữ liệu và lưu vào database
"""

import asyncio
import json
import re
from playwright.async_api import async_playwright
from typing import List, Dict
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class TGDDScraper:
    def __init__(self):
        self.base_url = "https://www.thegioididong.com/laptop"
        self.products = []
        self.db_config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "chatbot_db")
        }
    
    def parse_price(self, price_text: str) -> int:
        """Parse giá từ text (ví dụ: '13.490.000₫' -> 13490000)"""
        if not price_text:
            return 0
        # Loại bỏ tất cả ký tự không phải số
        price_num = re.sub(r'[^\d]', '', price_text)
        return int(price_num) if price_num else 0
    
    def extract_category_from_name(self, name: str) -> int:
        """Xác định category_id dựa trên tên sản phẩm"""
        name_lower = name.lower()
        
        # Gaming laptops
        if any(keyword in name_lower for keyword in ['gaming', 'nitro', 'legion', 'tuf', 'rog', 'victus', 'omen']):
            return 5  # Laptop Gaming
        
        # Graphic/Design laptops
        if any(keyword in name_lower for keyword in ['proart', 'creator', 'aero', 'macbook pro']):
            return 7  # Laptop Đồ Họa
        
        # Thin and light laptops
        if any(keyword in name_lower for keyword in ['air', 'zenbook', 'gram', 'xps', 'matebook', 'swift']):
            return 8  # Laptop Mỏng Nhẹ
        
        # Office laptops (default)
        return 6  # Laptop Văn Phòng
    
    async def scrape_product_list(self, page, url: str) -> List[Dict]:
        """Cào danh sách sản phẩm từ trang danh sách"""
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(3000)  # Đợi trang load
        
        # Scroll xuống để load thêm sản phẩm
        await page.evaluate("""
            window.scrollTo(0, document.body.scrollHeight);
        """)
        await page.wait_for_timeout(2000)
        
        # Extract sản phẩm từ trang
        products = await page.evaluate("""
            () => {
                const products = [];
                const items = document.querySelectorAll('li[class*="item"], div[class*="item"], article[class*="item"]');
                
                items.forEach(item => {
                    try {
                        // Tìm tên
                        const nameSelectors = ['h3 a', 'a[class*="name"]', '.name', '[class*="product-name"]', 'h3'];
                        let name = '';
                        for (const selector of nameSelectors) {
                            const el = item.querySelector(selector);
                            if (el) {
                                name = el.textContent?.trim() || el.title?.trim() || '';
                                if (name) break;
                            }
                        }
                        
                        // Tìm giá
                        const priceSelectors = ['.price', '[class*="price"]', '[class*="cost"]', '.price-current'];
                        let priceText = '';
                        for (const selector of priceSelectors) {
                            const el = item.querySelector(selector);
                            if (el) {
                                priceText = el.textContent?.trim() || '';
                                if (priceText && priceText.includes('₫')) break;
                            }
                        }
                        
                        // Tìm link
                        const linkEl = item.querySelector('a[href*="/laptop/"]');
                        const link = linkEl ? linkEl.href : '';
                        
                        // Tìm hình ảnh
                        const imgEl = item.querySelector('img');
                        const image = imgEl ? (imgEl.src || imgEl.getAttribute('data-src') || '') : '';
                        
                        if (name && priceText && priceText.includes('₫') && link && !name.includes('Giá')) {
                            const priceNum = priceText.replace(/[^\d]/g, '');
                            products.push({
                                name: name.replace(/\\n/g, ' ').trim(),
                                price: priceText.trim(),
                                priceNumber: parseInt(priceNum) || 0,
                                link: link,
                                image: image
                            });
                        }
                    } catch (e) {
                        console.error('Error:', e);
                    }
                });
                
                // Loại bỏ trùng lặp
                const uniqueProducts = [];
                const seenLinks = new Set();
                products.forEach(p => {
                    if (!seenLinks.has(p.link)) {
                        seenLinks.add(p.link);
                        uniqueProducts.push(p);
                    }
                });
                
                return uniqueProducts;
            }
        """)
        
        return products
    
    async def scrape_product_detail(self, page, product_url: str) -> Dict:
        """Cào thông tin chi tiết của một sản phẩm"""
        try:
            await page.goto(product_url, wait_until="networkidle")
            await page.wait_for_timeout(2000)
            
            product_detail = await page.evaluate("""
                () => {
                    const product = {};
                    
                    // Tên sản phẩm
                    const nameEl = document.querySelector('h1, [class*="product-name"], [class*="name"]');
                    product.name = nameEl ? nameEl.textContent.trim() : '';
                    
                    // Giá
                    const priceEl = document.querySelector('.box-price-present, [class*="price-current"], .price');
                    product.price = priceEl ? priceEl.textContent.trim() : '';
                    
                    // Mô tả
                    const descEl = document.querySelector('[class*="description"], [class*="desc"], .content');
                    product.description = descEl ? descEl.textContent.trim().substring(0, 1000) : '';
                    
                    // Thông số kỹ thuật
                    const specEls = document.querySelectorAll('[class*="parameter"] li, [class*="spec"] li, .technical-specs li');
                    const specs = [];
                    specEls.forEach(el => {
                        const text = el.textContent.trim();
                        if (text && text.length > 5) specs.push(text);
                    });
                    product.specifications = specs.slice(0, 15).join(', ');
                    
                    // Hình ảnh
                    const imgEl = document.querySelector('.box-img-main img, [class*="product-image"] img');
                    product.image = imgEl ? (imgEl.src || imgEl.getAttribute('data-src') || '') : '';
                    
                    return product;
                }
            """)
            
            return product_detail
        except Exception as e:
            print(f"Error scraping {product_url}: {str(e)}")
            return {}
    
    async def scrape_multiple_pages(self, max_pages: int = 5) -> List[Dict]:
        """Cào nhiều trang sản phẩm"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = await context.new_page()
            
            all_products = []
            
            # Cào từng trang
            for page_num in range(1, max_pages + 1):
                if page_num == 1:
                    url = self.base_url
                else:
                    url = f"{self.base_url}?p={page_num}"
                
                print(f"Scraping page {page_num}: {url}")
                products = await self.scrape_product_list(page, url)
                all_products.extend(products)
                print(f"Found {len(products)} products on page {page_num}")
                
                # Đợi một chút trước khi cào trang tiếp theo
                await asyncio.sleep(2)
            
            # Lấy thông tin chi tiết cho mỗi sản phẩm
            detailed_products = []
            for i, product in enumerate(all_products[:50]):  # Giới hạn 50 sản phẩm
                print(f"Scraping detail {i+1}/{min(50, len(all_products))}: {product['name']}")
                detail = await self.scrape_product_detail(page, product['link'])
                
                # Merge thông tin
                merged_product = {
                    **product,
                    **detail
                }
                
                # Sử dụng tên và giá từ detail nếu có
                if detail.get('name'):
                    merged_product['name'] = detail['name']
                if detail.get('price'):
                    merged_product['price'] = detail['price']
                    merged_product['priceNumber'] = self.parse_price(detail['price'])
                if detail.get('image'):
                    merged_product['image'] = detail['image']
                
                detailed_products.append(merged_product)
                
                # Đợi một chút giữa các request
                await asyncio.sleep(1)
            
            await browser.close()
            return detailed_products
    
    def save_to_sql(self, products: List[Dict], filename: str = "tgdd_products.sql"):
        """Lưu sản phẩm vào file SQL"""
        sql_statements = []
        
        for product in products:
            if not product.get('name') or not product.get('priceNumber'):
                continue
            
            name = product['name'].replace("'", "\\'")
            price = product.get('priceNumber', 0)
            description = (product.get('description', '') or product.get('specifications', '')).replace("'", "\\'")
            image_url = product.get('image', '')
            category_id = self.extract_category_from_name(name)
            
            # Giới hạn độ dài description
            if len(description) > 500:
                description = description[:500]
            
            sql = f"""
INSERT INTO products (category_id, name, description, price, stock, image_url, status) VALUES
({category_id}, '{name}', '{description}', {price}, 10, '{image_url}', 'active');
"""
            sql_statements.append(sql)
        
        # Ghi vào file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("-- Products scraped from thegioididong.com\n")
            f.write("-- Generated automatically by scraper_tgdd.py\n\n")
            f.write("\n".join(sql_statements))
        
        print(f"Saved {len(sql_statements)} products to {filename}")
    
    def save_to_json(self, products: List[Dict], filename: str = "tgdd_products.json"):
        """Lưu sản phẩm vào file JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(products)} products to {filename}")
    
    async def run(self, max_pages: int = 3):
        """Chạy scraper"""
        print(f"Starting scraper for {max_pages} pages...")
        products = await self.scrape_multiple_pages(max_pages)
        print(f"Total products scraped: {len(products)}")
        
        # Lưu vào file
        self.save_to_json(products, "tgdd_products.json")
        self.save_to_sql(products, "tgdd_products.sql")
        
        return products

async def main():
    scraper = TGDDScraper()
    products = await scraper.run(max_pages=3)  # Cào 3 trang đầu
    print(f"\nScraping completed! Found {len(products)} products.")

if __name__ == "__main__":
    asyncio.run(main())

