import unittest

from beancount.parser import cmptest
from beancount import loader

from non_leaf_account_restrictions.no_transactions import no_transactions

class TestNoNonLeafTransactions(cmptest.TestCase):
	@loader.load_doc()
	def test_should_allow_opening_non_leaf_account(self, entries, _, options_map):
		"""
			plugin "non_leaf_account_restrictions.no_transactions"
			1990-01-01 open Assets:MyBank GBP
			1990-01-01 open Assets:MyBank:Rent GBP
		"""
		returned_entries, errors = no_transactions(entries, options_map)
		self.assertFalse(errors)

	@loader.load_doc()
	def test_should_allow_closing_non_leaf_account(self, entries, _, options_map):
		"""
			plugin "non_leaf_account_restrictions.no_transactions"
			1990-01-01 open Assets:MyBank GBP
			1990-01-01 open Assets:MyBank:Rent GBP
			1990-01-02 close Assets:MyBank
		"""
		returned_entries, errors = no_transactions(entries, options_map)
		self.assertFalse(errors)

	@loader.load_doc()
	def test_should_allow_transaction_on_leaf_account(self, entries, _, options_map):
		"""
			plugin "non_leaf_account_restrictions.no_transactions"
			1990-01-01 open Assets:MyBank GBP
			1990-01-01 open Assets:MyBank:Rent GBP
			1990-01-01 open Equity:OpeningBalances GBP
			1990-01-02 * "Opening balance"
				Assets:MyBank:Rent      10.00 GBP
				Equity:OpeningBalances -10.00 GBP
		"""
		returned_entries, errors = no_transactions(entries, options_map)
		self.assertFalse(errors)

	@loader.load_doc()
	def test_should_allow_balance_assertion_on_non_leaf_account(self, entries, _, options_map):
		"""
			plugin "non_leaf_account_restrictions.no_transactions"
			1990-01-01 open Assets:MyBank GBP
			1990-01-01 open Assets:MyBank:Rent GBP
			1990-01-01 open Equity:OpeningBalances GBP
			1990-01-02 * "Opening balance"
				Assets:MyBank:Rent             10.00 GBP
				Equity:OpeningBalances        -10.00 GBP
			1990-01-03 balance Assets:MyBank 10.00 GBP
		"""
		returned_entries, errors = no_transactions(entries, options_map)
		self.assertFalse(errors)

	@loader.load_doc(expect_errors=True)
	def test_should_not_allow_transaction_on_non_leaf_account(self, entries, _, options_map):
		"""
			plugin "non_leaf_account_restrictions.no_transactions"
			1990-01-01 open Assets:MyBank GBP
			1990-01-01 open Assets:MyBank:Rent GBP
			1990-01-01 open Assets:MyBank:Food GBP
			1990-01-01 open Equity:OpeningBalances GBP
			1990-01-02 * "Opening balance"
				Assets:MyBank           10.00 GBP
				Equity:OpeningBalances -10.00 GBP
		"""
		returned_entries, errors = no_transactions(entries, options_map)
		self.assertEqual(len(errors), 1)
		self.assertRegex(errors[0].message, 'Assets:MyBank')

	@loader.load_doc(expect_errors=True)
	def test_should_not_allow_transaction_on_nested_non_leaf_account(self, entries, _, options_map):
		"""
			plugin "non_leaf_account_restrictions.no_transactions"
			1990-01-01 open Assets:MyBank GBP
			1990-01-01 open Assets:MyBank:MyAccount:Rent GBP
			1990-01-01 open Assets:MyBank:MyAccount:Food GBP
			1990-01-01 open Equity:OpeningBalances GBP
			1990-01-02 * "Opening balance"
				Assets:MyBank:MyAccount  10.00 GBP
				Equity:OpeningBalances  -10.00 GBP
		"""
		returned_entries, errors = no_transactions(entries, options_map)
		self.assertEqual(len(errors), 1)
		self.assertRegex(errors[0].message, 'Assets:MyBank:MyAccount')

	@loader.load_doc()
	def test_should_allow_balance_assertions_on_non_leaf_account(self, entries, _, options_map):
		"""
			plugin "non_leaf_account_restrictions.no_transactions"
			1990-01-01 open Assets:MyBank GBP
			1990-01-01 open Assets:MyBank:Rent GBP
			1990-01-01 open Assets:MyBank:Food GBP
			1990-01-01 open Equity:OpeningBalances GBP
			1990-01-02 * "Opening balance"
				Assets:MyBank:Rent              10.00 GBP
				Equity:OpeningBalances         -10.00 GBP
			1990-01-03 balance Assets:MyBank  10.00 GBP
		"""
		returned_entries, errors = no_transactions(entries, options_map)
		self.assertFalse(errors)

	@loader.load_doc(expect_errors=True)
	def test_should_not_allow_transaction_on_previously_leaf_account(self, entries, _, options_map):
		"""
			plugin "non_leaf_account_restrictions.no_transactions"
			1990-01-01 open Assets:MyBank GBP
			1990-01-01 open Equity:OpeningBalances GBP
			1990-01-02 * "Opening balance"
				Assets:MyBank           10.00 GBP
				Equity:OpeningBalances -10.00 GBP
			1990-01-03 open Assets:MyBank:MyAccount GBP
		"""
		returned_entries, errors = no_transactions(entries, options_map)
		self.assertEqual(len(errors), 1)
		self.assertRegex(errors[0].message, 'Assets:MyBank')

	@loader.load_doc(expect_errors=True)
	def test_should_not_allow_padding_on_non_leaf_account(self, entries, _, options_map):
		"""
			plugin "non_leaf_account_restrictions.no_transactions"
			1990-01-01 open Assets:MyBank GBP
			1990-01-01 open Assets:MyBank:Rent GBP
			1990-01-01 open Equity:OpeningBalances GBP
			1990-01-01 pad Assets:MyBank Equity:OpeningBalances
			1990-01-01 balance Assets:MyBank 10.00 GBP
		"""
		returned_entries, errors = no_transactions(entries, options_map)
		self.assertEqual(len(errors), 1)
		self.assertRegex(errors[0].message, 'Assets:MyBank')

	@loader.load_doc()
	def test_should_allow_padding_on_leaf_accounts(self, entries, _, options_map):
		"""
			plugin "non_leaf_account_restrictions.no_transactions"
			1990-01-01 open Assets:MyBank GBP
			1990-01-01 open Assets:MyBank:Rent GBP
			1990-01-01 open Equity:OpeningBalances GBP
			1990-01-01 pad Assets:MyBank:Rent Equity:OpeningBalances
			1990-01-02 balance Assets:MyBank:Rent 10.00 GBP
		"""
		returned_entries, errors = no_transactions(entries, options_map)

	@loader.load_doc()
	def test_should_allow_notes_on_non_leaf_accounts(self, entries, _, options_map):
		"""
			plugin "non_leaf_account_restrictions.no_transactions"
			1990-01-01 open Assets:MyBank GBP
			1990-01-01 open Assets:MyBank:Rent GBP
			1990-01-02 note Assets:MyBank "This is just a placeholder account"
		"""
		returned_entries, errors = no_transactions(entries, options_map)

if __name__ == '__main__':
    unittest.main()
