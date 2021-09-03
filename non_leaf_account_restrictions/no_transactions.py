import collections

from beancount.core import data
from beancount.core import getters
from beancount.core import realization

__plugins__ = ['no_transactions']

NonLeafTransactionError = collections.namedtuple(
	'NonLeafTransactionError',
	'source message entry'
)

def no_transactions(entries, _):
	errors = []
	for account in non_leaf_accounts_from(entries):
		if has_disallowed_directives(account):
			errors.append(non_leaf_transaction_error_for(account, entries))
	return entries, errors

def non_leaf_accounts_from(entries):
	real_root = realization.realize(entries, compute_balance=False)
	return list(
		filter(
			lambda account: len(account) > 0 and account.txn_postings,
			realization.iter_children(real_root)
		)
	)

def has_disallowed_directives(account):
	disallowed_directives = (data.TxnPosting, data.Pad)
	return len([
		posting for posting in account.txn_postings
		if isinstance(posting, disallowed_directives)
	]) > 0

def non_leaf_transaction_error_for(account, entries):
	open_entry = open_entry_of(account, entries)
	default_meta = data.new_metadata('<leafonly>', 0)
	return NonLeafTransactionError(
		open_entry.meta if open_entry else default_meta,
		"Non-leaf account '{}' has transactions on it".format(account.account),
		open_entry
	)

def open_entry_of(account, entries):
	open_close_map = getters.get_account_open_close(entries)
	open_entry = None
	try:
		open_entry = open_close_map[account.account][0]
	except KeyError:
		pass
	return open_entry
