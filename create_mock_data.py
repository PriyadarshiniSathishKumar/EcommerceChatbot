from app import app, db
from models import Product
import random

def create_mock_products():
    """Create mock product data for the application"""
    
    # Electronics products
    electronics = [
        {
            'title': 'Wireless Bluetooth Headphones',
            'description': 'High-quality wireless headphones with noise cancellation and long battery life.',
            'price': 79.99,
            'category': 'Electronics',
            'rating': 4.5,
            'image_url': 'https://pixabay.com/get/gc88466a5fc34cd892c21b78c6c8dbd1d39bcc0b768c34af7f810065dd609cf029b2565a8eafde491be4aed715b53d5d2c21e142eab65beb9f257d817846889d8_1280.jpg'
        },
        {
            'title': 'Smart Watch Pro',
            'description': 'Advanced smartwatch with fitness tracking, heart rate monitor, and GPS.',
            'price': 299.99,
            'category': 'Electronics',
            'rating': 4.7,
            'image_url': 'https://pixabay.com/get/g7406b76fa835eda10fc42ecd4ebde1a39410fe8aa2566c62d788ffd05c55a61fc501035ebf0811702e7ec159333115980dccbd43a469b9ee8592e30fb99b2db5_1280.jpg'
        },
        {
            'title': 'USB-C Fast Charger',
            'description': 'Quick charge adapter with multiple ports for all your devices.',
            'price': 24.99,
            'category': 'Electronics',
            'rating': 4.3,
            'image_url': 'https://pixabay.com/get/g8d5e78c414e8fc5be379452811e1bda3d901eb51e2c6e60e63e366d8192a9f9e77413c12d41ccb447b2fb93555bfba8a1f332c9dff162b2c74fdf1a02cb3950b_1280.jpg'
        },
        {
            'title': 'Laptop Stand Adjustable',
            'description': 'Ergonomic laptop stand for better posture and cooling.',
            'price': 34.99,
            'category': 'Electronics',
            'rating': 4.4,
            'image_url': 'https://pixabay.com/get/g1fd5b45800c495e3dbbc0f94111f3858a97549dc194fca4cafc09737649b9f008da4c3a28022d0c75e4e329f84c548c1bdf81d5bc5724ce7095fc5a7e572c459_1280.jpg'
        },
        {
            'title': 'Wireless Gaming Mouse',
            'description': 'High-precision gaming mouse with customizable RGB lighting.',
            'price': 59.99,
            'category': 'Electronics',
            'rating': 4.6,
            'image_url': 'https://pixabay.com/get/gd1e95447f38753c5d2aab85d4634cb2105f7fcacd9556d79d7466e43836359280406d56e58647f375e6de51193bce6b8639b32b6dc92af61a5fff6b94bb43cba_1280.jpg'
        },
        {
            'title': '4K Webcam HD',
            'description': 'Ultra HD webcam perfect for streaming and video calls.',
            'price': 89.99,
            'category': 'Electronics',
            'rating': 4.5,
            'image_url': 'https://pixabay.com/get/gc639c96bb4caf3dbee17995c3ea797bf055fc47886211242c1142a0dff4dceee8d4f1975f134b25276022fe4dd332b28530256c3e473a4b072256ccc435ff6d3_1280.jpg'
        }
    ]
    
    # Books
    books = [
        {
            'title': 'The Art of Programming',
            'description': 'Comprehensive guide to modern programming techniques and best practices.',
            'price': 45.99,
            'category': 'Books',
            'rating': 4.8,
            'image_url': 'https://pixabay.com/get/g5ce90db0b464ec78317c363b4f6326810d9c0c0b59d487e6eae2475fafdd098a4fd185441f2071741b6fa004739e9bfd19d254279cbb99c020b620b088f5c0a8_1280.jpg'
        },
        {
            'title': 'Machine Learning Fundamentals',
            'description': 'Learn the basics of machine learning and artificial intelligence.',
            'price': 52.99,
            'category': 'Books',
            'rating': 4.7,
            'image_url': 'https://pixabay.com/get/gbbd5a8c148c72d31907ef84523fd386258f4c0e7b94eb150e2caa072a4cc3d71e59add0b0d361d20e68fd241ebc281ca266d8f6632326605f55764ecb40f2fcd_1280.jpg'
        },
        {
            'title': 'Web Development Complete',
            'description': 'Full-stack web development from frontend to backend.',
            'price': 39.99,
            'category': 'Books',
            'rating': 4.6,
            'image_url': 'https://pixabay.com/get/g5ce90db0b464ec78317c363b4f6326810d9c0c0b59d487e6eae2475fafdd098a4fd185441f2071741b6fa004739e9bfd19d254279cbb99c020b620b088f5c0a8_1280.jpg'
        },
        {
            'title': 'Data Science Handbook',
            'description': 'Essential guide to data analysis and visualization.',
            'price': 48.99,
            'category': 'Books',
            'rating': 4.5,
            'image_url': 'https://pixabay.com/get/gbbd5a8c148c72d31907ef84523fd386258f4c0e7b94eb150e2caa072a4cc3d71e59add0b0d361d20e68fd241ebc281ca266d8f6632326605f55764ecb40f2fcd_1280.jpg'
        }
    ]
    
    # Textiles
    textiles = [
        {
            'title': 'Premium Cotton T-Shirt',
            'description': 'Comfortable and breathable cotton t-shirt in various colors.',
            'price': 19.99,
            'category': 'Textiles',
            'rating': 4.4,
            'image_url': 'https://pixabay.com/get/g5cbc779c8905e4e5949520557a1c5661a1972e5c7b6dc0a02475df466b7087e9c9473526c09468722895ddf0bc6fb8b37b0e7767353df26f46db28179d1ac1ed_1280.jpg'
        },
        {
            'title': 'Denim Jacket Classic',
            'description': 'Timeless denim jacket perfect for any casual outfit.',
            'price': 65.99,
            'category': 'Textiles',
            'rating': 4.6,
            'image_url': 'https://pixabay.com/get/gc93bf46d6727b1560f23a1ac05b3617a0f7369fc45ae9a6ace35038a33304e35b7e487ba9c6d028d7933f605fc897cafdcfbde45adc204360924c434f7e1ade7_1280.jpg'
        },
        {
            'title': 'Winter Scarf Wool',
            'description': 'Warm and cozy wool scarf for cold weather.',
            'price': 29.99,
            'category': 'Textiles',
            'rating': 4.3,
            'image_url': 'https://pixabay.com/get/gc342b41776f2a0ac07536f985c550ce86db44ac8e47d2b2d53a6812282b62c92e1480784617257696f1e8685a7f823ebe39cd1a89c408f5ecdd166545550e316_1280.jpg'
        },
        {
            'title': 'Athletic Shorts',
            'description': 'Breathable athletic shorts for workouts and sports.',
            'price': 24.99,
            'category': 'Textiles',
            'rating': 4.5,
            'image_url': 'https://pixabay.com/get/g1c1fdb847807515918b2261f1be06c1d5f252f8b2c274aad9d01c1f2d2ac213e40c89b3ec443c7bc0346aa6b47e93e8911ed06490510546440d117a13eed1fa2_1280.jpg'
        }
    ]
    
    # Combine all products
    all_products = electronics + books + textiles
    
    # Generate additional products to reach 100+
    additional_products = []
    base_products = electronics + books + textiles
    
    for i in range(90):  # Add 90 more to reach 100+
        base = random.choice(base_products)
        variation = {
            'title': f"{base['title']} - Model {i+1}",
            'description': base['description'],
            'price': round(base['price'] * random.uniform(0.8, 1.3), 2),
            'category': base['category'],
            'rating': round(random.uniform(3.5, 5.0), 1),
            'image_url': base['image_url']
        }
        additional_products.append(variation)
    
    all_products.extend(additional_products)
    
    # Add products to database
    with app.app_context():
        # Clear existing products
        Product.query.delete()
        
        for product_data in all_products:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        print(f"Created {len(all_products)} mock products!")

if __name__ == '__main__':
    create_mock_products()
