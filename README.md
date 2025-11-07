# Finance Tracker Pro

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/UI-Tkinter-red.svg)](#)

**A modern, local-first personal finance dashboard built with Python and Tkinter.**

This application helps you manage your accounts, track all your transactions, and visualize your wealth allocation according to a customizable financial rule (e.g., 25/15/50/10).



---

## 📖 Table of Contents

* [What Makes This Project Special?](#-what-makes-this-project-special)
* [About the Project](#-about-the-project)
  * [Features](#-features)
  * [Built With](#-built-with)
* [Getting Started](#-getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#-usage)
* [Contributing](#-contributing)
* [License](#-license)
* [Contact](#-contact)

---

## 🌟 What Makes This Project Special?

Many finance apps are cloud-based, complicated, or require subscriptions. This project is different:

* **🔒 100% Private and Local-First:** Your financial data **never** leaves your computer. It's stored in a `finance_data.json` file in the same folder as the app. There are no web servers, no cloud accounts, and no subscriptions.
* **💡 Built-In Financial Strategy:** This isn't just a simple ledger. The entire app is built around the **25/15/50/10 Strategic Allocation Rule**, a powerful concept for wealth management:
    * **🚀 25% - Growth:** Money that works for you (e.g., Crypto, Stocks).
    * **🛡️ 15% - Stability:** Your emergency fund, easily accessible.
    * **🏠 50% - Essentials:** Money for your necessary living costs.
    * **🎉 10% - Rewards:** Money to enjoy life guilt-free.
* **✅ Fully Customizable:** Don't like the 25/15/50/10 split? You can change it to **any** percentages you want in the settings (as long as it totals 100%).
* **✈️ Lightweight & Portable:** It's a single Python script that uses standard libraries. You don't need complex dependencies or heavy installations. You can run it on any machine with Python.

---

## 📜 About the Project

Finance Tracker Pro is a desktop application designed for individuals who want a simple, clean, and effective way to manage their finances based on a clear strategy.

The core of the app is built around the "strategic allocation rule" that helps you see how your current wealth is divided between Growth, Stability, Essentials, and Rewards, and compare it against your financial goals.

### ✨ Features

* **Modern UI:** A beautiful, dark-themed interface built with Tkinter and `ttk` styles.
* **Dynamic Dashboard:** Get a complete financial overview with summary cards, a 30-day portfolio trend chart, and a detailed breakdown of all your accounts.
* **Strategic Allocation Rule:** Apply and customize the 25/15/50/10 rule to see if your finances are aligned with your goals.
* **Transaction Tracking:** Easily add, view, and **delete (with a right-click)** income or expense transactions. The app automatically updates your account balances.
* **Account Management:** Create, rename, and delete accounts across categories like "Cash & Bank," "Crypto & Investments," and "Upcoming."
* **Currency Conversion:** Includes a setting to define the USD-to-LKR exchange rate for accurate crypto/investment tracking.
* **Local-First:** All data is saved locally to `finance_data.json`. No servers, no accounts, no fees.

### 🛠️ Built With

* [Python](https://www.python.org/)
* [Tkinter](https://docs.python.org/3/library/tkinter.html) (including `ttk`)
* Standard libraries: `json`, `os`, `datetime`

---

## 🚀 Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

You must have **Python 3** installed on your system. This application uses standard libraries that come with Python, so no external packages (like from `pip`) are required.

### Installation

1.  **Clone the repository**
    ```sh
    git clone [https://github.com/tharinduxd0/Finance-Tracker-Pro.git](https://github.com/tharinduxd0/Finance-Tracker-Pro.git)
    ```
2.  **Navigate to the project directory**
    ```sh
    cd Finance-Tracker-Pro
    ```
3.  **Run the application**
    *(Assuming you named the file `finance_tracker.py`)*
    ```sh
    python finance_tracker.py
    ```

That's it! The application will launch, and it will automatically create a `finance_data.json` file in the same directory to store your information.

> **Note**
> You should add `finance_data.json` to your `.gitignore` file to avoid committing your personal financial data to GitHub.

---

## 💡 Usage

The application is split into four main tabs for easy navigation:

* **📊 Dashboard:** This is your home screen. It shows your total net worth, summary cards for each asset category, and a 30-day trend chart of your portfolio. Below, you can see all your individual accounts and edit their balances directly.
* **✅ 25/15/50/10 Rule:** This tab applies your strategic allocation rule. It calculates the *target* amount you should have in Growth, Stability, Essentials, and Rewards based on your total wealth, and compares it to your *current* allocation.
* **💰 Transactions:** View a complete history of all your transactions. You can add new income or expense items using the "+ Add Transaction" button. To delete a transaction, simply **right-click** it in the list and select "Delete."
* **⚙️ Settings:**
    * **Rule Percentages:** Customize the 25/15/50/10 rule to any percentage you want.
    * **Exchange Rate:** Update the USD to LKR exchange rate.
    * **Account Management:** Safely rename or delete existing accounts.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📬 Contact

[tharinduxd] - [@tharinduxd](https://twitter.com/tharinduxd)

Project Link: [https://github.com/tharinduxd0/Finance-Tracker-Pro](https://github.com/tharinduxd0/Finance-Tracker-Pro)
