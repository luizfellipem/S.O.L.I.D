from abc import ABC, abstractmethod
from typing import List

# Single Responsibility Principle (SRP)
# Cada classe tem uma única responsabilidade.

class Order:
    def __init__(self, items: List[str], customer: str):
        self.items = items
        self.customer = customer

class OrderRepository:
    def save_order(self, order: Order):
        print(f"Salvando pedido para {order.customer} com itens: {order.items}")

# Open/Closed Principle (OCP)
# O sistema é aberto para extensão, mas fechado para modificação.
# Adicionamos novos métodos de pagamento sem alterar a classe `PaymentProcessor`.

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float):
        pass

class CreditCardPayment(PaymentProcessor):
    def process_payment(self, amount: float):
        print(f"Processando pagamento com cartão de crédito de {amount}.")

class PixPayment(PaymentProcessor):
    def process_payment(self, amount: float):
        print(f"Processando o pagamento do Pix de {amount}.")

# Liskov Substitution Principle (LSP)
# Subclasses devem ser substituíveis por suas superclasses.
# `Discount` é uma classe base abstrata, e as subclasses seguem o contrato definido.

class Discount(ABC):
    @abstractmethod
    def apply_discount(self, total: float) -> float:
        pass

class NoDiscount(Discount):
    def apply_discount(self, total: float) -> float:
        return total

class PercentageDiscount(Discount):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def apply_discount(self, total: float) -> float:
        return total * (1 - self.percentage)

# Interface Segregation Principle (ISP)
# Interfaces devem ser específicas ao cliente. A interface `PaymentProcessor` atende um propósito claro.

# Dependency Inversion Principle (DIP)
# Módulos de alto nível não dependem de módulos de baixo nível. Ambos dependem de abstrações.
# `OrderService` depende de abstrações (`PaymentProcessor` e `Discount`) ao invés de implementações concretas.

class OrderService:
    def __init__(self, payment_processor: PaymentProcessor, discount: Discount):
        self.payment_processor = payment_processor
        self.discount = discount

    def place_order(self, order: Order, total: float):
        discounted_total = self.discount.apply_discount(total)
        print(f"Final total após desconto: {discounted_total}")
        self.payment_processor.process_payment(discounted_total)
        OrderRepository().save_order(order)

# Exemplo de interação com o usuário
def get_user_input():
    print("Bem-vindo ao sistema de pedidos da loja online!")

    # Coletar dados do pedido
    customer = input("Informe o nome do cliente: ")
    items = input("Informe os itens separados por vírgula: ").split(",")
    total = float(input("Informe o valor total da compra: "))

    # Escolher tipo de pagamento
    print("Escolha o método de pagamento:")
    print("1. Cartão de Crédito")
    print("2. Pix")
    payment_option = int(input("Digite a opção de pagamento: "))
    
    if payment_option == 1:
        payment_processor = CreditCardPayment()
    elif payment_option == 2:
        payment_processor = PixPayment()
    else:
        print("Opção inválida! Usando Cartão de Crédito por padrão.")
        payment_processor = CreditCardPayment()

    # Escolher tipo de desconto
    print("Escolha o tipo de desconto:")
    print("1. Sem Desconto")
    print("2. Desconto de 10%")
    discount_option = int(input("Digite a opção de desconto: "))
    
    if discount_option == 1:
        discount = NoDiscount()
    elif discount_option == 2:
        discount = PercentageDiscount(0.1)
    else:
        print("Opção inválida! Usando Sem Desconto por padrão.")
        discount = NoDiscount()

    # Processar pedido
    order = Order(items, customer)
    order_service = OrderService(payment_processor, discount)
    order_service.place_order(order, total)

# Executa o programa de forma iterativa
if __name__ == "__main__":
    while True:
        get_user_input()
        continue_shopping = input("Deseja fazer outro pedido? (s/n): ").lower()
        if continue_shopping != 's':
            print("Obrigado por utilizar o sistema!")
            break



""" 
Justificativas para o S.O.L.I.D. com interatividade:

Single Responsibility Principle (SRP):
As classes Order, OrderRepository, e OrderService têm responsabilidades definidas. Order mantém os detalhes do pedido, OrderRepository salva os pedidos e OrderService processa os pedidos, isso melhorou a qualidade do código ao isolar responsabilidades, o que facilita alterações e testes.

Open/Closed Principle (OCP):
Foi adicionada a capacidade de escolher diferentes formas de pagamento e tipos de desconto sem modificar o comportamento das classes principais, isso tornou o código extensível, facilitando a adição de novos métodos de pagamento e tipos de desconto sem alterar as classes existentes.

Liskov Substitution Principle (LSP):
As subclasses CreditCardPayment, PixPayment, NoDiscount, e PercentageDiscount podem substituir as suas superclasses sem alterar o comportamento esperado, isso garantiu que o código seja facilmente mantido e estendido, e que as subclasses possam ser usadas de forma substituível.

Interface Segregation Principle (ISP):
A interface PaymentProcessor está focada apenas no processamento de pagamentos, o que faz sentido para todas as suas implementações (CreditCardPayment e PixPayment), mantendo as interfaces específicas e simples, isso evita que as classe sejam sobrecarregadas com métodos desnecessários.

Dependency Inversion Principle (DIP):
OrderService depende de abstrações como PaymentProcessor e Discount ao invés de implementações concretas. Isso permite que o sistema seja altamente configurável, dependendo do contexto, a inversão de dependências torna o código mais flexível, permitindo que as implementações sejam trocadas ou estendidas facilmente.

Melhorias com as mudanças:
Essas mudanças melhoraram a modularidade, flexibilidade e a facilidade de manutenção do código. Ao seguir os princípios S.O.L.I.D., o sistema se torna mais resiliente a mudanças e permite a inclusão de novas funcionalidades sem comprometer o código existente. 
"""

