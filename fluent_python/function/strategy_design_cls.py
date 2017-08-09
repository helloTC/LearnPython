#!/usr/bin/env python
# coding=utf-8

from abc import ABC, abstractmethod
from collections import namedtuple

Customer = nametupled('Customer', 'name fidelity')
class LineItem(object):
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
    
    def total(self):
        return self.price * self.quantity

class Order(object):
    # the context
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount
    
    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())

class Promotion(ABC):
    # The Strategy: an abstract Base class
    @abstractmethod
    def discount(self, order):
        pass

class FidelityPromo(Promotion):
    """
    5% discount for customers with 1000 or more fidelity points
    """
    def discount(self, order):
        return order.total()

class BulkItemPromo(Promotion):
    """
    10% discount for each LineItem with 20 or more units
    """
    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount+= item.total()*.1
        return discount

class LargeOrderPromo(Promotion):
    """
    7% discount for orders with 10 or more distinct items
    """
    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items)>=10:
            return order.total() * .07
        else:
            return 0




