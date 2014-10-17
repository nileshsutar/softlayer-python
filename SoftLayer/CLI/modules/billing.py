
"""
usage: sl billing  [<command>] [<args>...] [options]

Display information about Billing of an Account

The available commands are:
  detail  Display detailed information about a billing
  list    Show a list of all billings of an account
"""
# :license: MIT, see LICENSE for more details.

import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI import formatting
from SoftLayer.CLI import exceptions
from SoftLayer.CLI import helpers


class BillingList(environment.CLIRunnable):
    """
usage: sl billing list [options]

Displays a list of Billing Information of an account

Options:
  --sortby=ARG  Column to sort by. options: id

Required:
  -l, --limit=LIMIT No. of results. Default results are 25    

Filters:
  --from-date	Shows invoices from the date it was created. Format will be 'MM/dd/yyyy HH:mm:ss'
  --to-date	Shows invoices till to-date. Format will be 'MM/dd/yyyy HH:mm:ss'
  --type	The type of an Invoice  example. New, Recurring etc...
  --id      Shows invoice of passed Id. 
"""
    action = 'list'
    required_params = ['--limit']

    def execute(self, args):
        mgr = SoftLayer.BillingManager(self.client)
        table = formatting.Table(['Invoice Id', 'Company Name', 'Date Created', 'Invoice Type', 'Invoice Amount', 'Amount Paid', 'Balance'])
        #table.sortby = args.get('--sortby') or 'id'
        self._validate_create_args(args)

        invoices=mgr.list_billing(typeCode=args.get('--type'),
                                  limit=args.get('--limit'),
                                  fromDate=args.get('--from-date'),
                                  toDate=args.get('--to-date'),
                                  )

        for invoice in invoices:
            table.add_row([
            invoice['id'],
            invoice['companyName'],
            invoice['createDate'],
            invoice['typeCode'],
            invoice['amount'],
            '',
            invoice['endingBalance']
            ])
        return table

    def _validate_create_args(self, args):
        """ Raises an ArgumentError if the given arguments are not valid """
        invalid_args = [k for k in self.required_params if args.get(k) is None]
        if invalid_args:
            raise exceptions.ArgumentError('Missing required options: %s' % ','.join(invalid_args))
