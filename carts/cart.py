from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request): #장바구니 항목 리스트 초기화
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] ={}
        self.cart = cart
            
    def add(self, product, quantity=1, override_quantity=False): #장바구니에 추가
        product_id = str(product.id) #prdouct가 가지고 있는 id 형태가 int형태인데 이걸 str로 바꿔서 가지고 옴
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price': str(product.price)}
        
        if override_quantity: #override_quantity가 True일때 덮어씌운다
            self.cart[product_id]['quantity']=quantity
        else: #override_quantity가 False일때 추가해준다
            self.cart[product_id]['quantity']+=quantity
        self.save()

    def save(self): #저장
        self.session.modified = True

    def remove(self, product): #삭제
        product_id = str(product.id)
        if product_id in self.cart: #product_id가 저장되어 있는 cart속에 있다면
            del self.cart[product_id]
            self.save()

    def __len__(self): #장바구니에 담긴 제품의 총 수량
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price']=Decimal(item['price'])
            item['total_price']=item['price']*item['quantity']
            yield item

    def get_total_price(self): #총 비용 계산
        return sum(Decimal(item['total_price']) for item in self.cart.values())

    def clear(self): #장바구니 비우기
        del self.session[settings.CART_SESSION_ID]
        self.save()



