"""
Expense Tracker CLI
Usage:
  python tracker.py add "Coffee" 4.50 Food
  python tracker.py list
  python tracker.py summary
"""

import argparse
from datetime import date

from storage import load_expenses, save_expenses


def cmd_add(description: str, amount: float, category: str) -> None:
    """Append a new expense entry and persist it."""
    if amount <= 0:
        print("Amount must be greater than zero.")
        return
    expenses = load_expenses()
    expenses.append({
        "date": str(date.today()),
        "description": description,
        "amount": round(amount, 2),
        "category": category,
    })
    save_expenses(expenses)
    print(f"Added: {description} — ${amount:.2f} [{category}]")


def cmd_list(category: str | None = None) -> None:
    """Print recorded expenses as a table, newest last. Optionally filter by category."""
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet. Use 'add' to get started.")
        return

    if category is not None:
        # Case-insensitive filter to match user expectation; storage casing is preserved in output
        expenses = [e for e in expenses if e["category"].lower() == category.lower()]
        if not expenses:
            print(f"No expenses found for category '{category}'.")
            return

    # Column widths chosen to fit typical values without truncating
    print(f"{'#':<4}  {'Date':<12}  {'Category':<16}  {'Amount':>8}  Description")
    print("─" * 65)
    for i, e in enumerate(expenses, 1):
        print(
            f"{i:<4}  {e['date']:<12}  {e['category']:<16}  "
            f"${e['amount']:>7.2f}  {e['description']}"
        )
    print("─" * 65)
    total = sum(e["amount"] for e in expenses)
    print(f"{'':>38}  ${total:>7.2f}  Total")


def cmd_summary() -> None:
    """Print total spending grouped by category, sorted alphabetically."""
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    # Accumulate totals per category
    totals: dict[str, float] = {}
    for e in expenses:
        totals[e["category"]] = round(totals.get(e["category"], 0) + e["amount"], 2)

    print(f"{'Category':<20}  {'Total':>10}")
    print("─" * 33)
    for category in sorted(totals):
        print(f"{category:<20}  ${totals[category]:>9.2f}")
    print("─" * 33)
    print(f"{'TOTAL':<20}  ${sum(totals.values()):>9.2f}")


def main() -> None:
    """Parse CLI arguments and dispatch to the appropriate command."""
    parser = argparse.ArgumentParser(
        description="Track your expenses from the command line.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python tracker.py add \"Lunch\" 12.50 Food\n"
            "  python tracker.py add \"Bus pass\" 40 Transport\n"
            "  python tracker.py list\n"
            "  python tracker.py list --category Food\n"
            "  python tracker.py summary"
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 'add' subcommand — takes positional args for a concise one-liner UX
    add_p = subparsers.add_parser("add", help="Add a new expense")
    add_p.add_argument("description", help='What you spent money on (quote if it has spaces)')
    add_p.add_argument("amount", type=float, help="Amount spent (e.g. 9.99)")
    add_p.add_argument("category", help="Category label (e.g. Food, Transport, Entertainment)")

    list_p = subparsers.add_parser("list", help="List all expenses")
    list_p.add_argument("--category", "-c", help="Filter by category (case-insensitive)")
    subparsers.add_parser("summary", help="Show totals grouped by category")

    args = parser.parse_args()

    if args.command == "add":
        cmd_add(args.description, args.amount, args.category)
    elif args.command == "list":
        cmd_list(args.category)
    elif args.command == "summary":
        cmd_summary()


if __name__ == "__main__":
    main()
