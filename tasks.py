"""
0. To run file type `python tasks.py in_1000000.json`.
   Example structure of `in_xxxxx.json`:
   ```
   {
    "items": [
        {
            "package": "FLEXIBLE",
            "created": "2020-03-10T00:00:00",
            "summary": [
                {
                    "period": "2019-12",
                    "documents": {
                        "incomes": 63,
                        "expenses": 13
                    }
                },
                {
                    "period": "2020-02",
                    "documents": {
                        "incomes": 45,
                        "expenses": 81
                    }
                }
            ]
        },
        {
            "package": "ENTERPRISE",
            "created": "2020-03-19T00:00:00",
            "summary": [
                {
                    "period": "2020-01",
                    "documents": {
                        "incomes": 15,
                        "expenses": 52
                    }
                },
                {
                    "period": "2020-02",
                    "documents": {
                        "incomes": 76,
                        "expenses": 47
                    }
                }
            ]
        }
    ]
   }
   ```
1. Please make below tasks described in docstring of functions in 7 days.
2. Changes out of functions body are not allowed.
3. Additional imports are not allowed.
4. Send us your solution (only tasks.py) through link in email.
   In annotations write how much time you spent for each function.
5. The data in the file is normalized.
6. Skip additional functionalities not described directly (like sorting).
7. First we will run automatic tests checking (using: 1 mln and 100 mln items):
   a) proper results and edge cases
   b) CPU usage
   c) memory usage
8. If your solution will NOT pass automatic tests (we allow some errors)
   application will be automatically rejected without additional feedback.
   You can apply again after 90 days.
9. Our develepers will review code (structure, clarity, logic).
"""
import datetime
import collections
import itertools


def task_1(data_in):
    """
    Return number of items per created[year-month].
    Add missing [year-month] with 0 if no items in data.
    ex. {
        '2020-03': 29,
        '2020-04': 0,
        '2020-05': 24
    }
    """
    # Estimated time of task completion: 30min

    start_date = None
    end_date = None
    count_dict = collections.defaultdict(int)

    for item in data_in["items"]:
        current_date = datetime.datetime.strptime(item["created"], "%Y-%m-%dT%H:%M:%S")
        count_dict[current_date.strftime("%Y-%m")] += 1

        if start_date is None or current_date < start_date:
            start_date = current_date
        if end_date is None or current_date > end_date:
            end_date = current_date

    current_date = datetime.datetime(
        year=start_date.year, month=start_date.month, day=1
    )
    while current_date <= end_date:
        year_month = current_date.strftime("%Y-%m")
        if year_month not in count_dict:
            count_dict[year_month] = 0
        current_date += datetime.timedelta(days=32)
        current_date = datetime.datetime(
            year=current_date.year, month=current_date.month, day=1
        )

    return count_dict


def task_2(data_in):
    """
    Return number of documents per period (incomes, expenses, total).
    Return only periods provided in data.
    ex. {
        '2020-04': {
            'incomes': 2480,
            'expenses': 2695,
            'total': 5175
        },
        '2020-05': {
            'incomes': 2673,
            'expenses': 2280,
            'total': 4953
        }
    }
    """
    # # Estimated time of task completion: 5min

    counts = collections.defaultdict(lambda: {"incomes": 0, "expenses": 0, "total": 0})

    for item in data_in["items"]:
        for summary in item["summary"]:
            period = summary["period"]
            incomes = summary["documents"]["incomes"]
            expenses = summary["documents"]["expenses"]
            total = incomes + expenses

            counts[period]["incomes"] += incomes
            counts[period]["expenses"] += expenses
            counts[period]["total"] += total

    return counts


def task_3(data_in):
    """
    Return arithmetic average(integer) number of documents per day
    in last three months counted from last period in data (all packages)
    for package in ['ENTERPRISE', 'FLEXIBLE']
    as one int
    ex. 64
    """
    # Estimated time of task completion: 20min

    last_period = max(
        summary["period"] for item in data_in["items"] for summary in item["summary"]
    )
    last_period_date = datetime.datetime.strptime(last_period, "%Y-%m")
    three_months_ago = last_period_date - datetime.timedelta(days=90)

    total_documents = 0
    total_days = 0

    for item in data_in["items"]:
        if item["package"] in ("ENTERPRISE", "FLEXIBLE"):
            for summary in item["summary"]:
                period_date = datetime.datetime.strptime(summary["period"], "%Y-%m")
                if three_months_ago <= period_date <= last_period_date:
                    incomes = summary.get("documents", {}).get("incomes", 0)
                    expenses = summary.get("documents", {}).get("expenses", 0)
                    total_documents += incomes + expenses
                    total_days += 1

    if total_days > 0:
        average_documents_per_day = total_documents // total_days
    else:
        average_documents_per_day = 0
    return average_documents_per_day


if __name__ == "__main__":
    import json
    import sys

    try:
        with open(sys.argv[1]) as fp:
            data_in = json.load(fp)
    except IndexError:
        print(
            f"""USAGE:
    {sys.executable} {sys.argv[0]} <filename>

Example:
    {sys.executable} {sys.argv[0]} in_1000000.json
"""
        )
    else:
        for func in [task_1, task_2, task_3]:
            print(f"\n>>> {func.__name__.upper()}")
            print(json.dumps(func(data_in), ensure_ascii=False, indent=2))
