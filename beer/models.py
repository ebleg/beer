from django.db import models
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta


class BronxMember(models.Model):
    firstName = models.CharField(max_length=10)
    lastName = models.CharField(max_length=20)
    nickName = models.CharField(max_length=30, default=firstName)

    beer_outstanding = models.IntegerField(default=0)

    def _get_daily(self):
        getQty = lambda obj: obj.qty
        transactions = self.transaction_set
        tres = datetime.combine(date.today(), time(0, 0, 0, 0))
        return sum(map(getQty, transactions.filter(stamp__gte=tres).filter(out__exact=True)))

    def _get_weekly(self):
        getQty = lambda obj: obj.qty
        transactions = self.transaction_set
        # beginning of the week
        td = date.today()
        tres = datetime.combine(td- timedelta(td.weekday()), time(0, 0, 0, 0))
        return sum(map(getQty, transactions.filter(stamp__gte=tres)
                       .filter(out__exact=True)))

    def _get_monthly(self):
        getQty = lambda obj: obj.qty
        transactions = self.transaction_set
        # beginning of the week
        td = date.today()
        tres = datetime.combine(td - timedelta(td.day), time(0, 0, 0, 0))
        return sum(map(getQty, transactions.filter(stamp__gte=tres)
                       .filter(out__exact=True)))

    daily = property(_get_daily)
    weekly = property(_get_weekly)
    monthly = property(_get_monthly)


    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class Transaction(models.Model):
    stamp = models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey("BronxMember", on_delete=models.CASCADE)
    item = models.ForeignKey("StockItem", on_delete=models.CASCADE)
    qty = models.IntegerField()
    out = models.BooleanField()  # False = in

    def __str__(self):
        if self.out:
            return f"[{self.stamp}] {self.member} took {self.qty} {self.item} out of inventory"
        else:
            return f"[{self.stamp}] {self.member} added {self.qty} {self.item} to inventory"


class StockItem(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField()
    qty = models.IntegerField()

    def __str__(self):
        return self.name

