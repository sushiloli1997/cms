from re import S
from django.db import Error, models
from contracts.models import Contracts, Client
from .manager import SoftDeleteManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDelete(models.Model):
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def delete(self):
        raise Error()

    class Meta:
        abstract = True


class PaymentStatus(models.IntegerChoices):
    UNPAID = 0, "Unpaid"
    PARTLY_PAID = 1, "Partly Paid"
    OVERDUE = 2, "Overdue"
    PAID = 3, "Paid"


class Invoices(BaseModel, SoftDelete):
    status_choices = [
        (PaymentStatus.UNPAID, "Unpaid"),
        (PaymentStatus.PARTLY_PAID, "Partly Paid"),
        (PaymentStatus.OVERDUE, "Overdue"),
        (PaymentStatus.PAID, "Paid"),
    ]
    status = models.IntegerField(choices=status_choices, default=PaymentStatus.UNPAID)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contracts, null=True, blank=True,
                                 on_delete=models.CASCADE)  # if no contract is selected, it will be None
    number_of_invoice = models.CharField("Number of invoice", max_length=10, )
    date_of_issue = models.DateField()

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'


class InvoiceTracks(BaseModel, SoftDelete):
    invoice = models.ForeignKey(Invoices, on_delete=models.CASCADE, related_name='tracks')
    action = models.PositiveSmallIntegerField()  # 1 - added,  2 - modified, 3 - removed
    description = models.TextField()
    status = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField(blank=True, null=True)
    amount = models.FloatField(null=True, blank=True)
    rate = models.FloatField(null=True, blank=True)
