"""
    SoftLayer Billing
    ~~~~~~~~~~~~~~~~~
    Billing Managers/helpers
"""

import SoftLayer
from SoftLayer import utils


class BillingManager(utils.IdentifierMixin, object):
    """
    Manages Billings
    """

    def __init__(self, client):
        self.client = client
        #self.billingInfo = self.client['Billing_Invoice_Item']
        self.billingInfo = self.client['Billing_Invoice']

    def list_billing(self, typeCode=None, **kwargs):
        """
        List all billing information of an account.
        """
        object_mask = 'mask[id, createDate, typeCode, amount,\
                      endingBalance, companyName]'

        object_filter = {'invoices': dict()}
        type_filter = dict()
        if typeCode:
            type_filter = {
                    'typeCode': {
                    'operation': typeCode.upper()
                    },
            }
        if type_filter:
            object_filter['invoices'].update(type_filter)
        
        date_filter = {
                        'createDate': {
                                'operation': 'betweenDate',
                                'options': []
                            },
        }
        start_date = kwargs.pop('fromDate', None)
        if start_date:
            option = {'name': 'startDate', 'value': [start_date]}
            date_filter['createDate']['options'].append(option)
        
        end_date = kwargs.pop('toDate', None)
        if end_date:
            option = {'name': 'endDate', 'value': [end_date]}
            date_filter['createDate']['options'].append(option)
        
        if date_filter['createDate']['options']:
            object_filter['invoices'].update(date_filter)
        try:
            invoices_iter = self.client['Account'].getInvoices(\
                                            mask=object_mask, \
                                            filter=object_filter,\
                                            **kwargs)
            return invoices_iter
        except Exception as e:
            raise e

    def get_billing(self, billing_id, **kwargs):
        """
        Get the details of billing
        """
        try:
            billing_info = self.billingInfo.getObject(\
                                            id=billing_id)
            return billing_info
        except Exception as e:
            raise e
