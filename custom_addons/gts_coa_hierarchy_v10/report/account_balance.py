import time
from odoo import api, models, _
from odoo.exceptions import UserError

class ReportTrialBalance(models.AbstractModel):
    _inherit = 'report.account.report_trialbalance'

    # get accounts of level selected in the wizard
    def _get_accounts(self, accounts, display_account):
        """ compute the balance, debit and credit for the provided accounts
            :Arguments:
                `accounts`: list of accounts record,
                `display_account`: it's used to display either all accounts or those accounts which balance is > 0
            :Returns a list of dictionary of Accounts with following key and value
                `name`: Account name,
                `code`: Account code,
                `credit`: total amount of credit,
                `debit`: total amount of debit,
                `balance`: total amount of balance,
        """
        
        # get level from context
        level = self._context.get('level',1)

        account_result = {}
        # Prepare sql query base on selected parameters from wizard
        tables, where_clause, where_params = self.env['account.move.line']._query_get()
        tables = tables.replace('"','')
        if not tables:
            tables = 'account_move_line'
        wheres = [""]
        if where_clause.strip():
            wheres.append(where_clause.strip())
        filters = " AND ".join(wheres)
        # compute the balance, debit and credit for the provided accounts
        request = ("SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" +\
                   " FROM " + tables + " WHERE account_id IN %s " + filters + " GROUP BY account_id")
        params = (tuple(accounts.ids),) + tuple(where_params)
        self.env.cr.execute(request, params)
        for row in self.env.cr.dictfetchall():
            account_result[row.pop('id')] = row

        account_res = []
        # filter the accounts for selected level
        if level:
            accounts = accounts.filtered(lambda a: a.level < int(level))
        for account in accounts:
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance'])
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            res['code'] = account.code
            res['name'] = account.name
            res['level'] = account.level
            res['type'] = account.type
            if account.id in account_result.keys():
                res['debit'] = account_result[account.id].get('debit')
                res['credit'] = account_result[account.id].get('credit')
                res['balance'] = account_result[account.id].get('balance')
            elif account.type == 'view':
                all_child_ids = list(set(account._get_children_and_consol_only_leaf_account().ids).intersection(account_result.keys()))
                if all_child_ids:
                    total_debit = total_credit = total_balance = 0.0
                    for each_child_id in all_child_ids:
                        total_debit += account_result[each_child_id].get('debit')
                        total_credit += account_result[each_child_id].get('credit')
                        total_balance += account_result[each_child_id].get('balance')
                    res['debit'] = total_debit
                    res['credit'] = total_credit
                    res['balance'] = total_balance

            if display_account == 'all':
                account_res.append(res)
            if display_account == 'not_zero' and not currency.is_zero(res['balance']):
                account_res.append(res)
            if display_account == 'movement' and (not currency.is_zero(res['debit']) or not currency.is_zero(res['credit'])):
                account_res.append(res)
        return account_res