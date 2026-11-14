import csv
import os
import sys
from datetime import datetime


STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "GOOGL": 140.50,
    "MSFT": 420.00,
    "AMZN": 175.25,
    "NVDA": 880.00,
}


def get_valid_quantity(ticker: str) -> int:
    """Prompts and validates a positive integer quantity for a stock."""
    while True:
        try:
            raw_qty = input(f"Enter quantity of {ticker} shares: ").strip()
            qty = int(raw_qty)
            if qty <= 0:
                print("Quantity must be greater than zero.")
                continue
            return qty
        except ValueError:
            print("Invalid number. Please enter a whole integer (e.g., 5).")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            sys.exit(0)


def save_portfolio(portfolio: list, total_value: float) -> None:
    """Saves the portfolio summary to either a .txt or .csv file with error handling."""
    while True:
        try:
            choice = input("\nSave report? Enter 'txt', 'csv', or 'no': ").strip().lower()
            if choice == "no":
                print("Report not saved.")
                return

            if choice not in ("txt", "csv"):
                print("Please enter 'txt', 'csv', or 'no'.")
                continue

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"portfolio_summary_{timestamp}.{choice}"

            if choice == "txt":
                with open(filename, "w", encoding="utf-8") as file:
                    file.write("STOCK PORTFOLIO SUMMARY\n")
                    file.write("=" * 45 + "\n")
                    for item in portfolio:
                        file.write(
                            f"{item['ticker']:<8} | Qty: {item['quantity']:<5} | "
                            f"Price: ${item['price']:<8.2f} | Subtotal: ${item['subtotal']:.2f}\n"
                        )
                    file.write("=" * 45 + "\n")
                    file.write(f"TOTAL INVESTMENT VALUE: ${total_value:.2f}\n")

            elif choice == "csv":
                with open(filename, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Ticker", "Quantity", "Price Per Share ($)", "Subtotal ($)"])
                    for item in portfolio:
                        writer.writerow([item["ticker"], item["quantity"], item["price"], item["subtotal"]])
                    writer.writerow([])
                    writer.writerow(["TOTAL INVESTMENT", "", "", round(total_value, 2)])

            print(f"Successfully saved portfolio to '{os.path.abspath(filename)}'")
            return

        except PermissionError:
            print("Permission denied: Unable to write file. Close any open files or check folder permissions.")
            return
        except OSError as e:
            print(f"File system error while saving: {e}")
            return
        except (KeyboardInterrupt, EOFError):
            print("\nSave cancelled.")
            return


def run_stock_tracker() -> None:
    """Main function to collect user stocks and calculate total portfolio value."""
    print("=" * 50)
    print("STOCK PORTFOLIO TRACKER")
    print("=" * 50)
    print("Available Stocks & Current Prices:")
    for ticker, price in STOCK_PRICES.items():
        print(f"  • {ticker}: ${price:.2f}")
    print("\nType 'DONE' when finished adding stocks.")

    portfolio = []
    total_investment = 0.0

    while True:
        try:
            ticker = input("\nEnter stock ticker (or 'DONE'): ").strip().upper()

            if ticker == "DONE":
                break

            if not ticker:
                print("Ticker cannot be empty.")
                continue

            if ticker not in STOCK_PRICES:
                print(f"'{ticker}' not found in available stock list. Choose from: {', '.join(STOCK_PRICES.keys())}")
                continue

            quantity = get_valid_quantity(ticker)
            price = STOCK_PRICES[ticker]
            subtotal = round(price * quantity, 2)

            # Update existing entry if user adds the same stock twice
            existing = next((item for item in portfolio if item["ticker"] == ticker), None)
            if existing:
                existing["quantity"] += quantity
                existing["subtotal"] = round(existing["subtotal"] + subtotal, 2)
            else:
                portfolio.append({
                    "ticker": ticker,
                    "quantity": quantity,
                    "price": price,
                    "subtotal": subtotal
                })

            total_investment = round(total_investment + subtotal, 2)
            print(f"Added {quantity} shares of {ticker} (${subtotal:.2f}).")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting tracker...")
            sys.exit(0)

    if not portfolio:
        print("\nNo stocks were added to your portfolio. Exiting.")
        return

    print("\n" + "=" * 50)
    print("YOUR PORTFOLIO SUMMARY")
    print("=" * 50)
    for item in portfolio:
        print(
            f"{item['ticker']:<6} | Qty: {item['quantity']:<4} | "
            f"Price: ${item['price']:<7.2f} | Subtotal: ${item['subtotal']:.2f}"
        )
    print("-" * 50)
    print(f"TOTAL INVESTMENT VALUE: ${total_investment:.2f}")
    print("=" * 50)

    save_portfolio(portfolio, total_investment)


if __name__ == "__main__":
    run_stock_tracker()