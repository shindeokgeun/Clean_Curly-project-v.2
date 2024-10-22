from django.shortcuts import render
from orders.models import OrderItem
from orders.forms import OrderCreateForm
from carts.cart import Cart

def order_create(request):
    cart = Cart(request)
    
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # 사용자 정보 설정
            order.save()  # 이제 저장
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            order.status = 'delivered' #주문이 완료되면 status를 delivered로 바꿈
            order.save() #변경된 상태를 저장함

            cart.clear()
            request.session['order_id'] = order.id
            return render(request, 'orders/order/created.html',{'cart':cart,'form':form})

    
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order/create.html', {'cart':cart, 'form':form})


