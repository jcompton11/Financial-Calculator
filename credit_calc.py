# dm = mth differentiated payment
# principal = the credit principal
# ni = nominal interest rate, usually 1/12th of the annual interest rate.
# If interest is 12%, then i = 0.01.
# np = number of payments or months.
# curr_p = current period.
# an = payment or annuity.

import argparse
import sys
from math import log, ceil, floor


# Define functions
def get_nominal_interest(interest):
    return interest / 1200


# This function is meant to be used in a loop. 'm' increments up to the limit 'n'.
def cal_diff_pay(p, i, n, m):
    return ceil(p/n + i * (p - p * ((m - 1) / n)))


def cal_annuity(p, i, n):
    return ceil(p * ((i * (1 + i) ** n) / ((1 + i) ** n - 1)))


# 'a' parameter is the annuity or payment made per month. The final value should be the principal
def cal_principal(a, i, n):
    return int(a / ((i * (1 + i) ** n) / ((1 + i) ** n - 1)))


# In a differentiated payment calculation, the overpayment is the sum of all payments minus the principal.
def cal_overpayment(p, n, a):
    return n * a - p


def cal_months_to_pay(p, i, a):
    return ceil(log(a / (a - i * p), 1 + i))


def param_error_exit():
    print("Incorrect parameters.")
    sys.exit()


# This section adds arguments using the argparse module.
# payments is a list of monthly payments used to derive a sum of all payments
# in order to calculate the over-payment.
payments = []

parser = argparse.ArgumentParser()

parser.add_argument("--type", choices=['diff', 'annuity'], help="needs to be either 'diff' or 'annuity'")
parser.add_argument("--principal", type=int, help="an 'int' which is the original value of the loan")
parser.add_argument("--periods", type=int, help="an 'int' which represents the number of months to pay")
parser.add_argument("--interest", type=float, help="a 'float' representation of interest in %")
parser.add_argument("--payment", type=int, help="an 'int' which represents payment in terms of months")

args = parser.parse_args()

if len(sys.argv[1:]) < 4:
    param_error_exit()
else:
    for v in vars(args).values():
        if isinstance(v, int) or isinstance(v, float):
            if v < 0:
                param_error_exit()

    principal = args.principal
    ni = get_nominal_interest(args.interest)
    np = args.periods
    an = args.payment

if args.type == "diff":
    for curr_p in range(1, np + 1):
        dm = cal_diff_pay(principal, ni, np, curr_p)
        payments.append(dm)
        print(f"Month {curr_p}: paid out {dm}")

    print(f"\nOverpayment = {sum(payments) - principal}")
elif args.type == "annuity":
    if np is not None and ni is not None and an is not None:
        principal = cal_principal(an, ni, np)
        op = cal_overpayment(principal, np, an)
        print(f"Your credit principal = {principal}!\nOverpayment = {op}")
    elif principal is not None and ni is not None and an is not None:
        np = cal_months_to_pay(principal, ni, an)
        y = floor(np / 12)
        op = cal_overpayment(principal, np, an)

        if np < 12:
            print(f'You need {np} month{"s" if np > 1 else ""} to repay this credit!')
        else:
            months = np % 12
            if months > 0:
                print(f'You need {y} year{"s" if y > 1 else ""} '
                      f'and {months} month{"s" if np > 1 else ""} to repay this credit!')
            else:
                print(f'You need {y} year{"s" if y > 1 else ""} to repay this credit!')
        print(f'Overpayment = {op}')
    elif principal is not None and np is not None and ni is not None:
        an = cal_annuity(principal, ni, np)
        op = cal_overpayment(principal, np, an)

        print(f'Your annuity payment = {an}!\nOverpayment = {op}')
