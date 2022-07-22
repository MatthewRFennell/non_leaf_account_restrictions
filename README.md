# Non-Leaf Account Restrictions

A Beancount plugin that detects `transaction` or `pad` instructions on non-leaf
accounts.

## Motivation

The `leafonly` plugin included with Beancount is used to prevent you from
accidentally posting transactions to non-leaf accounts. However, sometimes it is
useful to open non-leaf accounts, while still posting no transactions to them.

This plugin is a less strict version of `leafonly` that just prevents
`transaction` and `pad` directives while letting you open and perform balance
assertions on your non-leaf account.

## Envelope Budgeting

Opening nested accounts can be useful to represent budgets within a particular
account. This is useful for approaches like envelope budgeting. For instance,
let's say you bank with `BofA`, but represent your budgets in sub-accounts of
`BofA` like so:

```
1990-01-01 open Assets:BofA      USD
1990-01-01 open Assets:BofA:Rent USD
1990-01-01 open Assets:BofA:Food USD
```

When summed together, the sub-accounts have the same amount of money as in your
bank account.

However, in order to create a balance assertions on `Assets:BofA`, you have to
open that account too. This is undesireable, as you may accidentally create
postings to this account. This plugin will let you open `Assets:BofA` and use
the account for balance assertions when you reconcile against your `BofA` bank
statement:

```
plugin "non_leaf_account_restrictions.no_transactions"
1990-01-01 open Assets:BofA USD              ; allowed
1990-01-01 open Assets:BofA:Rent USD
1990-01-01 open Assets:BofA:Food USD
1990-01-01 open Income:Hooli USD

1990-01-26 * "Payday!"
  Assets:BofA:Rent             650.00 USD
  Assets:BofA:Food             150.00 USD
  Income:Hooli                -800.00 USD    ; allowed

1990-02-01 balance Assets:BofA 800.00 USD    ; allowed, works as expected
```

While not letting you post `transaction`s or `pad` directives to this account:

```
1990-03-26 * "Another payday!"
  Assets:BofA       800.00 USD
  Income:Hooli     -800.00 USD               ; not allowed: raises an error

1999-04-26 pad Assets:BofA Income:Hooli      ; not allowed: raises an error
```

## Installing + Usage

```
pip3 install git+https://github.com/MatthewRFennell/non_leaf_account_restrictions.git
```

And then, in your `beancount` file:

```
plugin "non_leaf_account_restrictions.no_transactions"
```

## Contributing

Any kind of contribution is more than welcome! If you have a question or feature
request, please feel free to raise an issue. If you'd like to create a PR, feel
free to create it, or create an issue if you'd like to discuss the design first.
