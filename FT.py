import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import json
import os

class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker Pro")
        self.root.geometry("1400x800")
        self.root.configure(bg='#0f172a')

        self.data_file = 'finance_data.json'
        self.usd_to_lkr = 290.0
        self.data = self.load_data()

        # Modern styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#0f172a', borderwidth=0)
        style.configure('TNotebook.Tab', background='#1e293b', foreground='#cbd5e1', 
                          padding=[20, 12], font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#3b82f6')], 
                    foreground=[('selected', 'white')])

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=0, pady=0)

        # Create tabs
        self.home_frame = tk.Frame(self.notebook, bg='#0f172a')
        self.rule_frame = tk.Frame(self.notebook, bg='#0f172a')
        self.tracker_frame = tk.Frame(self.notebook, bg='#0f172a')
        self.settings_frame = tk.Frame(self.notebook, bg='#0f172a')

        self.notebook.add(self.home_frame, text='📊 Dashboard')
        self.notebook.add(self.rule_frame, text='✅ 25/15/50/10 Rule')
        self.notebook.add(self.tracker_frame, text='💰 Transactions')
        self.notebook.add(self.settings_frame, text='⚙️ Settings')

        # Build tabs
        self.build_home_tab()
        self.build_rule_tab()
        self.build_tracker_tab()
        self.build_settings_tab() # This tab is now scrollable

        self.refresh_home()
        self.refresh_rule_tab()

    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.usd_to_lkr = data.get('exchange_rate', 290.0)
                return data
        else:
            return {
                'exchange_rate': 290.0,
                'rule_percentages': {
                    'growth': 25,
                    'stability': 15,
                    'essentials': 50,
                    'rewards': 10
                },
                'categories': {
                    'Cash & Bank': {
                        'Com Bank Main Acc': 0.00,
                        'MM Acc': 0.00,
                        'Boc Bank Main Acc': 0.00,
                        'Sampath Acc': 0.00,
                        'On Hand': 0.00
                    },
                    'Crypto & Investments': {
                        'Crypto $': 0.00,
                        'CAL': 0.00,
                        'CSE': 0.00,
                        'Ez Cash': 0.00,
                        'Paynoree Skrill': 0.00
                    },
                    'Upcoming': {}
                },
                'transactions': []
            }

    def save_data(self):
        """Save data to JSON file"""
        self.data['exchange_rate'] = self.usd_to_lkr
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    # --- NEW FUNCTION TO HANDLE ALL SCROLLING ---
    def _bind_mousewheel(self, widget, canvas):
        """Binds cross-platform mouse wheel events to the canvas."""
        
        def on_scroll(event):
            """Internal scroll handler."""
            # Linux scroll up/down
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
            # Windows/macOS scroll
            elif event.delta != 0:
                # event.delta is typically 120 on Windows, 1 on macOS
                if abs(event.delta) >= 120:
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                else:
                    canvas.yview_scroll(int(-1 * event.delta), "units")

        # Bind all relevant events
        widget.bind("<MouseWheel>", on_scroll)  # Windows/macOS
        widget.bind("<Button-4>", on_scroll)    # Linux scroll up
        widget.bind("<Button-5>", on_scroll)    # Linux scroll down
    # --- END OF NEW FUNCTION ---

    def build_home_tab(self):
        """Build the Home dashboard with chart"""
        # Create main container with scrollbar
        main_container = tk.Frame(self.home_frame, bg='#0f172a')
        main_container.pack(fill='both', expand=True)

        # Canvas and scrollbar
        self.home_canvas = tk.Canvas(main_container, bg='#0f172a', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=self.home_canvas.yview)

        self.home_content = tk.Frame(self.home_canvas, bg='#0f172a')

        # Configure scrolling
        self.home_content.bind("<Configure>", lambda e: self.home_canvas.configure(scrollregion=self.home_canvas.bbox("all")))

        canvas_frame = self.home_canvas.create_window((0, 0), window=self.home_content, anchor="nw")

        # Make canvas expand to fill width
        def configure_canvas(event):
            self.home_canvas.itemconfig(canvas_frame, width=event.width)

        self.home_canvas.bind('<Configure>', configure_canvas)
        self.home_canvas.configure(yscrollcommand=scrollbar.set)

        # --- MOUSE WHEEL SCROLLING (FIXED) ---
        # Bind the canvas AND the inner frame for scrolling
        self._bind_mousewheel(self.home_canvas, self.home_canvas)
        self._bind_mousewheel(self.home_content, self.home_canvas)
        # --- END OF FIX ---

        self.home_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_home(self):
        """Refresh home dashboard display"""
        for widget in self.home_content.winfo_children():
            widget.destroy()

        # Modern Header
        header = tk.Frame(self.home_content, bg='#1e293b', height=100)
        header.pack(fill='x', padx=20, pady=(20, 10))

        header_inner = tk.Frame(header, bg='#1e293b')
        header_inner.pack(fill='both', expand=True, padx=30, pady=20)

        tk.Label(header_inner, text="💼 Financial Dashboard", font=('Segoe UI', 28, 'bold'),
                 bg='#1e293b', fg='#ffffff').pack(anchor='w')

        date_info = f"{datetime.now().strftime('%A, %B %d, %Y')} • {datetime.now().strftime('%I:%M %p')}"
        tk.Label(header_inner, text=date_info, font=('Segoe UI', 11),
                 bg='#1e293b', fg='#94a3b8').pack(anchor='w', pady=(5, 0))

        rate_text = f"Exchange Rate: 1 USD = {self.usd_to_lkr} LKR"
        tk.Label(header_inner, text=rate_text, font=('Segoe UI', 10),
                 bg='#1e293b', fg='#64748b').pack(anchor='w', pady=(2, 0))

        # Calculate totals
        totals = self.calculate_totals()

        # Summary Cards
        cards_frame = tk.Frame(self.home_content, bg='#0f172a')
        cards_frame.pack(fill='x', padx=20, pady=10)

        self.create_modern_card(cards_frame, "💰 Real Total", 
                                f"LKR {totals['real_total']:,.2f}", 
                                '#10b981', 0)
        self.create_modern_card(cards_frame, "📈 Total with Upcoming", 
                                f"LKR {totals['total']:,.2f}", 
                                '#3b82f6', 1)
        self.create_modern_card(cards_frame, "🏦 Cash & Bank", 
                                f"LKR {totals['cash_bank']:,.2f}", 
                                '#8b5cf6', 2)
        self.create_modern_card(cards_frame, "₿ Crypto & Investments", 
                                f"LKR {totals['crypto']:,.2f}", 
                                '#f59e0b', 3)

        # Portfolio Chart
        self.create_portfolio_chart()

        # Categories
        for category, accounts in self.data['categories'].items():
            self.create_modern_category(category, accounts, totals)

    def create_modern_card(self, parent, title, value, color, column):
        """Create modern gradient card"""
        card = tk.Frame(parent, bg=color, relief='flat', bd=0)
        card.grid(row=0, column=column, padx=8, pady=5, sticky='nsew')
        parent.grid_columnconfigure(column, weight=1)

        # Add subtle shadow effect with frame
        shadow = tk.Frame(card, bg='#1e293b', relief='flat')
        shadow.pack(fill='both', expand=True, padx=2, pady=2)

        inner = tk.Frame(shadow, bg=color, relief='flat')
        inner.pack(fill='both', expand=True, padx=0, pady=0)

        tk.Label(inner, text=title, font=('Segoe UI', 11, 'bold'),
                 bg=color, fg='white', anchor='w').pack(fill='x', padx=20, pady=(20, 5))
        tk.Label(inner, text=value, font=('Segoe UI', 22, 'bold'),
                 bg=color, fg='white', anchor='w').pack(fill='x', padx=20, pady=(0, 20))

    def create_portfolio_chart(self):
        """Create portfolio trend chart"""
        chart_container = tk.Frame(self.home_content, bg='#1e293b', relief='flat')
        chart_container.pack(fill='x', padx=20, pady=10)

        header = tk.Frame(chart_container, bg='#1e293b')
        header.pack(fill='x', padx=25, pady=(20, 10))

        tk.Label(header, text="📊 Portfolio Trend (Last 30 Days)", 
                 font=('Segoe UI', 16, 'bold'),
                 bg='#1e293b', fg='#ffffff').pack(anchor='w')

        # Create canvas for chart
        chart_canvas = tk.Canvas(chart_container, bg='#0f172a', height=250, 
                                 highlightthickness=0)
        chart_canvas.pack(fill='x', padx=25, pady=(10, 25))

        # Generate sample data points based on transactions
        data_points = self.generate_chart_data()

        if len(data_points) > 1:
            # Draw chart
            self.draw_line_chart(chart_canvas, data_points)
        else:
            tk.Label(chart_canvas, text="Add transactions to see portfolio trends",
                     font=('Segoe UI', 12), bg='#0f172a', fg='#64748b').place(relx=0.5, rely=0.5, anchor='center')

    def generate_chart_data(self):
        """Generate chart data from transactions"""
        current_total = self.calculate_totals()['real_total']

        # Create 30 data points
        data_points = []

        if not self.data['transactions']:
            # If no transactions, show flat line
            for i in range(30):
                data_points.append(current_total)
            return data_points

        # Sort transactions by date
        sorted_trans = sorted(self.data['transactions'], 
                              key=lambda x: x.get('timestamp', ''), reverse=True)

        # Calculate running balance backwards
        balance = current_total
        date_balances = {datetime.now().date(): balance}

        for trans in sorted_trans[:60]: # Last 60 transactions
            balance -= trans['amount']
            try:
                trans_date = datetime.fromisoformat(trans['timestamp']).date()
                date_balances[trans_date] = balance
            except:
                pass

        # Fill 30 days
        for i in range(29, -1, -1):
            date = (datetime.now() - timedelta(days=i)).date()
            if date in date_balances:
                data_points.append(date_balances[date])
            else:
                data_points.append(data_points[-1] if data_points else current_total)

        return data_points

    def draw_line_chart(self, canvas, data_points):
        """Draw line chart on canvas"""
        canvas.update()
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width <= 1 or height <= 1:
            width = 1000
            height = 250

        padding = 50
        chart_width = width - 2 * padding
        chart_height = height - 2 * padding

        # Find min/max for scaling
        min_val = min(data_points)
        max_val = max(data_points)
        value_range = max_val - min_val if max_val != min_val else 1

        # Draw grid lines
        for i in range(5):
            y = padding + (chart_height * i / 4)
            canvas.create_line(padding, y, width - padding, y,
                                fill='#1e293b', width=1)
            value = max_val - (value_range * i / 4)
            canvas.create_text(padding - 10, y, text=f"{value/1000:.0f}K",
                                fill='#64748b', anchor='e', font=('Segoe UI', 9))

        # Draw line
        points = []
        for i, value in enumerate(data_points):
            x = padding + (chart_width * i / (len(data_points) - 1))
            y = padding + chart_height - ((value - min_val) / value_range * chart_height)
            points.extend([x, y])

        if len(points) >= 4:
            # Draw gradient fill
            fill_points = points + [width - padding, height - padding, padding, height - padding]
            canvas.create_polygon(fill_points, fill='#3b82f6', stipple='gray50', 
                                  outline='')

            # Draw line
            canvas.create_line(points, fill='#60a5fa', width=3, smooth=True)

            # Draw points
            for i in range(0, len(points), 2):
                canvas.create_oval(points[i]-4, points[i+1]-4,
                                   points[i]+4, points[i+1]+4,
                                   fill='#3b82f6', outline='#60a5fa', width=2)

        # X-axis labels
        for i in [0, len(data_points)//2, len(data_points)-1]:
            x = padding + (chart_width * i / (len(data_points) - 1))
            days_ago = len(data_points) - 1 - i
            date = (datetime.now() - timedelta(days=days_ago)).strftime('%m/%d')
            canvas.create_text(x, height - padding + 20, text=date,
                                fill='#64748b', font=('Segoe UI', 9))

    def create_modern_category(self, category, accounts, totals):
        """Create modern category section"""
        section = tk.Frame(self.home_content, bg='#1e293b', relief='flat')
        section.pack(fill='x', padx=20, pady=10)

        # Header
        header = tk.Frame(section, bg='#334155')
        header.pack(fill='x')

        icon = {'Cash & Bank': '🏦', 'Crypto & Investments': '₿', 'Upcoming': '📅'}.get(category, '💼')
        tk.Label(header, text=f"{icon} {category}", font=('Segoe UI', 14, 'bold'),
                 bg='#334155', fg='#ffffff').pack(side='left', padx=25, pady=15)

        # Accounts
        for account, balance in accounts.items():
            acc_frame = tk.Frame(section, bg='#1e293b')
            acc_frame.pack(fill='x', padx=25, pady=8)

            # Account name
            tk.Label(acc_frame, text=account, font=('Segoe UI', 11),
                     bg='#1e293b', fg='#e2e8f0', anchor='w').pack(side='left', fill='x', expand=True)

            # Balance
            if account == 'Crypto $':
                balance_text = f"$ {balance:,.2f}"
                lkr_value = balance * self.usd_to_lkr
                tk.Label(acc_frame, text=f"(≈ {lkr_value:,.2f} LKR)", font=('Segoe UI', 9),
                         bg='#1e293b', fg='#94a3b8').pack(side='right', padx=10)
                tk.Label(acc_frame, text=balance_text, font=('Segoe UI', 11, 'bold'),
                         bg='#1e293b', fg='#10b981').pack(side='right')
            else:
                tk.Label(acc_frame, text=f"{balance:,.2f} LKR", font=('Segoe UI', 11, 'bold'),
                         bg='#1e293b', fg='#10b981').pack(side='right', padx=10)

            # Edit button
            edit_btn = tk.Button(acc_frame, text="✏️", font=('Segoe UI', 10),
                                  bg='#3b82f6', fg='white', relief='flat',
                                  cursor='hand2', padx=10, pady=4,
                                  command=lambda c=category, a=account: self.edit_balance(c, a))
            edit_btn.pack(side='right', padx=5)

        # Add account button
        add_frame = tk.Frame(section, bg='#1e293b')
        add_frame.pack(fill='x', padx=25, pady=15)

        add_btn = tk.Button(add_frame, text="+ Add Account", font=('Segoe UI', 10),
                            bg='#475569', fg='white', relief='flat',
                            cursor='hand2', padx=15, pady=8,
                            command=lambda c=category: self.add_account(c))
        add_btn.pack(side='left')

        # Category total
        total_value = {'Cash & Bank': totals['cash_bank'], 
                       'Crypto & Investments': totals['crypto'],
                       'Upcoming': totals['upcoming']}.get(category, 0)

        total_frame = tk.Frame(section, bg='#0f172a')
        total_frame.pack(fill='x', padx=25, pady=15)

        tk.Label(total_frame, text=f"TOTAL {category.upper()}", font=('Segoe UI', 11, 'bold'),
                 bg='#0f172a', fg='#94a3b8').pack(side='left')
        tk.Label(total_frame, text=f"{total_value:,.2f} LKR", font=('Segoe UI', 14, 'bold'),
                 bg='#0f172a', fg='#10b981').pack(side='right')

    def calculate_totals(self):
        """Calculate all totals"""
        cash_bank = sum(self.data['categories']['Cash & Bank'].values())

        crypto_lkr = sum(v for k, v in self.data['categories']['Crypto & Investments'].items() 
                         if k != 'Crypto $')
        crypto_usd = self.data['categories']['Crypto & Investments'].get('Crypto $', 0)
        crypto_usd_lkr = crypto_usd * self.usd_to_lkr
        crypto_total = crypto_lkr + crypto_usd_lkr

        upcoming = sum(self.data['categories']['Upcoming'].values())

        real_total = cash_bank + crypto_total
        total = real_total + upcoming

        return {
            'cash_bank': cash_bank,
            'crypto': crypto_total,
            'upcoming': upcoming,
            'real_total': real_total,
            'total': total
        }

    def build_rule_tab(self):
        """Build the 25/15/50/10 Rule tab"""
        # Create main container with scrollbar
        main_container = tk.Frame(self.rule_frame, bg='#0f172a')
        main_container.pack(fill='both', expand=True)

        # Canvas and scrollbar
        self.rule_canvas = tk.Canvas(main_container, bg='#0f172a', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=self.rule_canvas.yview)

        self.rule_content = tk.Frame(self.rule_canvas, bg='#0f172a')

        # Configure scrolling
        self.rule_content.bind("<Configure>", lambda e: self.rule_canvas.configure(scrollregion=self.rule_canvas.bbox("all")))

        canvas_frame = self.rule_canvas.create_window((0, 0), window=self.rule_content, anchor="nw")

        def configure_canvas(event):
            self.rule_canvas.itemconfig(canvas_frame, width=event.width)

        self.rule_canvas.bind('<Configure>', configure_canvas)
        self.rule_canvas.configure(yscrollcommand=scrollbar.set)

        # --- MOUSE WHEEL SCROLLING (FIXED) ---
        # Bind the canvas AND the inner frame
        self._bind_mousewheel(self.rule_canvas, self.rule_canvas)
        self._bind_mousewheel(self.rule_content, self.rule_canvas) # <-- This was missing
        # --- END OF FIX ---

        self.rule_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # --- THIS IS THE UPDATED METHOD ---
    def refresh_rule_tab(self):
        """Refresh the rule tab with calculations"""
        for widget in self.rule_content.winfo_children():
            widget.destroy()

        # Get rule percentages
        rules = self.data.get('rule_percentages', {
            'growth': 25,
            'stability': 15,
            'essentials': 50,
            'rewards': 10
        })

        # Header
        header = tk.Frame(self.rule_content, bg='#1e293b', height=100)
        header.pack(fill='x', padx=20, pady=(20, 10))

        header_inner = tk.Frame(header, bg='#1e293b')
        header_inner.pack(fill='both', expand=True, padx=30, pady=20)

        tk.Label(header_inner, text="✅ Financial Allocation Rule", font=('Segoe UI', 28, 'bold'),
                 bg='#1e293b', fg='#ffffff').pack(anchor='w')

        rule_text = f"{rules['growth']}/{rules['stability']}/{rules['essentials']}/{rules['rewards']} Rule"
        tk.Label(header_inner, text=rule_text, font=('Segoe UI', 14),
                 bg='#1e293b', fg='#94a3b8').pack(anchor='w', pady=(5, 0))

        tk.Label(header_inner, text="Divide your wealth strategically for long-term growth", 
                 font=('Segoe UI', 11),
                 bg='#1e293b', fg='#64748b').pack(anchor='w', pady=(2, 0))

        # Calculate totals
        totals = self.calculate_totals()
        real_total = totals['real_total']

        # Overview Card
        overview = tk.Frame(self.rule_content, bg='#1e293b', relief='flat')
        overview.pack(fill='x', padx=20, pady=10)

        tk.Label(overview, text="📊 Your Financial Overview", font=('Segoe UI', 16, 'bold'),
                 bg='#1e293b', fg='#ffffff').pack(anchor='w', padx=30, pady=(20, 15))

        overview_inner = tk.Frame(overview, bg='#0f172a')
        overview_inner.pack(fill='x', padx=30, pady=(0, 20))

        tk.Label(overview_inner, text="Real Total (Cash + Investments):", font=('Segoe UI', 12),
                 bg='#0f172a', fg='#94a3b8').pack(side='left', padx=10, pady=15)
        tk.Label(overview_inner, text=f"LKR {real_total:,.2f}", font=('Segoe UI', 18, 'bold'),
                 bg='#0f172a', fg='#10b981').pack(side='left', padx=10)

        # --- UPDATED CALCULATION LOGIC ---

        # 1. Growth Calculation (as before)
        growth_target = real_total * (rules['growth'] / 100)
        growth_current = totals['crypto']
        growth_diff = growth_current - growth_target
        growth_percent_current = (growth_current / real_total * 100) if real_total > 0 else 0

        # 2. Non-Growth Calculations (Stability, Essentials, Rewards)
        
        # Get the total percentage for non-growth rules
        non_growth_rule_total = rules['stability'] + rules['essentials'] + rules['rewards']
        total_cash = totals['cash_bank']
        
        # Avoid division by zero if all non-growth rules are 0%
        if non_growth_rule_total == 0:
            stability_current = 0
            essentials_current = 0
            rewards_current = 0
        else:
            # Pro-rate the current cash balance across the 3 categories
            stability_current = total_cash * (rules['stability'] / non_growth_rule_total)
            essentials_current = total_cash * (rules['essentials'] / non_growth_rule_total)
            rewards_current = total_cash * (rules['rewards'] / non_growth_rule_total)

        # Calculate targets, diffs, and percentages for the 3 categories
        stability_target = real_total * (rules['stability'] / 100)
        stability_diff = stability_current - stability_target
        stability_percent_current = (stability_current / real_total * 100) if real_total > 0 else 0

        essentials_target = real_total * (rules['essentials'] / 100)
        essentials_diff = essentials_current - essentials_target
        essentials_percent_current = (essentials_current / real_total * 100) if real_total > 0 else 0

        rewards_target = real_total * (rules['rewards'] / 100)
        rewards_diff = rewards_current - rewards_target
        rewards_percent_current = (rewards_current / real_total * 100) if real_total > 0 else 0

        # --- END OF UPDATED LOGIC ---

        # Growth Section
        self.create_rule_card(
            "🚀 Growth",
            rules['growth'],
            growth_target,
            growth_current,
            growth_diff,
            growth_percent_current,
            '#10b981',
            "Money that makes you more money (Investments already allocated)"
        )

        # Stability Section
        self.create_rule_card(
            "🛡️ Stability",
            rules['stability'],
            stability_target,
            stability_current,      # <-- Updated
            stability_diff,         # <-- Updated
            stability_percent_current, # <-- Updated
            '#3b82f6',
            "Emergency fund - Keep accessible for safety"
        )

        # Essentials Section
        self.create_rule_card(
            "🏠 Essentials",
            rules['essentials'],
            essentials_target,
            essentials_current,     # <-- Updated
            essentials_diff,        # <-- Updated
            essentials_percent_current, # <-- Updated
            '#8b5cf6',
            "Necessary living costs (rent, food, utilities, transport)"
        )

        # Rewards Section
        self.create_rule_card(
            "🎉 Rewards",
            rules['rewards'],
            rewards_target,
            rewards_current,        # <-- Updated
            rewards_diff,           # <-- Updated
            rewards_percent_current, # <-- Updated
            '#f59e0b',
            "Enjoy life guilt-free (hobbies, travel, social)"
        )

        # Info Section
        info = tk.Frame(self.rule_content, bg='#1e293b', relief='flat')
        info.pack(fill='x', padx=20, pady=10)

        tk.Label(info, text="💡 How This Works", font=('Segoe UI', 16, 'bold'),
                 bg='#1e293b', fg='#ffffff').pack(anchor='w', padx=30, pady=(20, 15))

        info_text = """
• Growth: Your "Crypto & Investments" already count toward this goal
• Stability, Essentials, Rewards: Your "Cash & Bank" total is
  conceptually divided among these three categories.
The system calculates targets based on your Real Total and shows
how your current assets align with those targets.
        """

        tk.Label(info, text=info_text.strip(), font=('Segoe UI', 11),
                 bg='#1e293b', fg='#94a3b8', justify='left').pack(anchor='w', padx=30, pady=(0, 20))
    # --- END OF UPDATED METHOD ---

    def create_rule_card(self, title, percent, target, current, diff, current_percent, color, description):
        """Create a rule allocation card"""
        card = tk.Frame(self.rule_content, bg='#1e293b', relief='flat')
        card.pack(fill='x', padx=20, pady=10)

        # Header
        header = tk.Frame(card, bg=color)
        header.pack(fill='x')

        header_left = tk.Frame(header, bg=color)
        header_left.pack(side='left', fill='x', expand=True, padx=25, pady=15)

        tk.Label(header_left, text=title, font=('Segoe UI', 16, 'bold'),
                 bg=color, fg='#ffffff').pack(anchor='w')
        tk.Label(header_left, text=description, font=('Segoe UI', 10),
                 bg=color, fg='#ffffff').pack(anchor='w', pady=(3, 0))

        tk.Label(header, text=f"{percent}%", font=('Segoe UI', 32, 'bold'),
                 bg=color, fg='#ffffff').pack(side='right', padx=30)

        # Content
        content = tk.Frame(card, bg='#1e293b')
        content.pack(fill='x', padx=25, pady=20)

        # Target row
        target_row = tk.Frame(content, bg='#1e293b')
        target_row.pack(fill='x', pady=5)

        tk.Label(target_row, text="🎯 Target Amount:", font=('Segoe UI', 11, 'bold'),
                 bg='#1e293b', fg='#e2e8f0').pack(side='left')
        tk.Label(target_row, text=f"LKR {target:,.2f}", font=('Segoe UI', 11, 'bold'),
                 bg='#1e293b', fg='#10b981').pack(side='right')

        # Current row
        current_row = tk.Frame(content, bg='#1e293b')
        current_row.pack(fill='x', pady=5)

        tk.Label(current_row, text="💰 Current Amount:", font=('Segoe UI', 11),
                 bg='#1e293b', fg='#94a3b8').pack(side='left')
        tk.Label(current_row, text=f"LKR {current:,.2f} ({current_percent:.1f}%)", 
                 font=('Segoe UI', 11),
                 bg='#1e293b', fg='#94a3b8').pack(side='right')

        # Difference row
        diff_row = tk.Frame(content, bg='#1e293b')
        diff_row.pack(fill='x', pady=5)

        if diff >= 0:
            status_text = "✅ Exceeded by:"
            status_color = '#10b981'
        else:
            status_text = "⚠️ Need more:"
            status_color = '#f59e0b'

        tk.Label(diff_row, text=status_text, font=('Segoe UI', 11),
                 bg='#1e293b', fg='#94a3b8').pack(side='left')
        tk.Label(diff_row, text=f"LKR {abs(diff):,.2f}", font=('Segoe UI', 11, 'bold'),
                 bg='#1e293b', fg=status_color).pack(side='right')

        # Progress bar
        progress_frame = tk.Frame(content, bg='#0f172a', height=30)
        progress_frame.pack(fill='x', pady=(10, 5))

        progress_percent = min((current / target * 100) if target > 0 else 0, 100)

        # Use a fixed width for the canvas to ensure bar size is consistent
        bar_width_total = 600
        canvas = tk.Canvas(progress_frame, bg='#0f172a', height=20, width=bar_width_total, highlightthickness=0)
        # Center the canvas
        canvas.pack(pady=5) 

        canvas.create_rectangle(0, 0, bar_width_total, 20, fill='#334155', outline='')

        if progress_percent > 0:
            bar_width = bar_width_total * (progress_percent / 100)
            canvas.create_rectangle(0, 0, bar_width, 20, fill=color, outline='')

        canvas.create_text(bar_width_total/2, 10, text=f"{progress_percent:.1f}% Complete",
                            fill='#ffffff', font=('Segoe UI', 9, 'bold'))

    def edit_balance(self, category, account):
        """Edit account balance"""
        current = self.data['categories'][category][account]
        new_value = simpledialog.askfloat("Edit Balance", 
                                          f"Enter new balance for {account}:",
                                          initialvalue=current)
        if new_value is not None:
            self.data['categories'][category][account] = new_value
            self.save_data()
            self.refresh_home()
            self.refresh_rule_tab()

    def add_account(self, category):
        """Add new account"""
        name = simpledialog.askstring("Add Account", 
                                      f"Enter account name for {category}:")
        if name and name.strip():
            self.data['categories'][category][name.strip()] = 0.00
            self.save_data()
            self.refresh_home()
            self.refresh_rule_tab()

    def build_tracker_tab(self):
        """Build transaction tracker"""
        # Header
        header = tk.Frame(self.tracker_frame, bg='#1e293b', height=80)
        header.pack(fill='x', padx=20, pady=20)

        header_inner = tk.Frame(header, bg='#1e293b')
        header_inner.pack(fill='both', expand=True, padx=30, pady=20)

        tk.Label(header_inner, text="💰 Transaction History", font=('Segoe UI', 24, 'bold'),
                 bg='#1e293b', fg='#ffffff').pack(side='left')

        tk.Button(header_inner, text="+ Add Transaction", font=('Segoe UI', 11, 'bold'),
                   bg='#10b981', fg='white', relief='flat', cursor='hand2',
                   padx=25, pady=12, command=self.add_transaction).pack(side='right')

        # Transaction list
        list_frame = tk.Frame(self.tracker_frame, bg='#1e293b')
        list_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')

        columns = ('Date', 'Account', 'Description', 'Category', 'Amount')
        self.transaction_tree = ttk.Treeview(list_frame, columns=columns, 
                                             show='headings', yscrollcommand=scrollbar.set)

        self.transaction_tree.heading('Date', text='DATE')
        self.transaction_tree.heading('Account', text='ACCOUNT')
        self.transaction_tree.heading('Description', text='DESCRIPTION')
        self.transaction_tree.heading('Category', text='RULE CATEGORY')
        self.transaction_tree.heading('Amount', text='AMOUNT')

        self.transaction_tree.column('Date', width=150)
        self.transaction_tree.column('Account', width=180)
        self.transaction_tree.column('Description', width=280)
        self.transaction_tree.column('Category', width=150)
        self.transaction_tree.column('Amount', width=150)

        scrollbar.config(command=self.transaction_tree.yview)
        self.transaction_tree.pack(fill='both', expand=True)

        # Right-click menu for deleting transactions - NEW
        context_menu = tk.Menu(self.tracker_frame, tearoff=0, bg='#1e293b', fg='#ffffff')
        context_menu.add_command(label="🗑️ Delete Transaction", command=self.delete_transaction)

        def show_context_menu(event):
            try:
                item = self.transaction_tree.identify_row(event.y)
                if item:
                    self.transaction_tree.selection_set(item)
                    context_menu.post(event.x_root, event.y_root)
            except:
                pass

        self.transaction_tree.bind("<Button-3>", show_context_menu)

        style = ttk.Style()
        style.configure("Treeview", 
                        background='#1e293b',
                        foreground='#e2e8f0',
                        fieldbackground='#1e293b',
                        font=('Segoe UI', 10),
                        rowheight=35)
        style.configure("Treeview.Heading", 
                        background='#334155',
                        foreground='#ffffff',
                        font=('Segoe UI', 11, 'bold'))
        style.map('Treeview', background=[('selected', '#3b82f6')])

        self.refresh_tracker()

    def refresh_tracker(self):
        """Refresh transaction list"""
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)

        for trans in reversed(self.data['transactions']):
            amount = trans['amount']
            amount_str = f"+{amount:,.2f} LKR" if amount >= 0 else f"{amount:,.2f} LKR"
            tag = 'income' if amount >= 0 else 'expense'

            rule_cat = trans.get('rule_category', '-')

            self.transaction_tree.insert('', 'end', 
                                         values=(trans['date'], trans['account'], 
                                                 trans['description'], rule_cat, amount_str),
                                         tags=(tag,))

        self.transaction_tree.tag_configure('income', foreground='#10b981')
        self.transaction_tree.tag_configure('expense', foreground='#ef4444')

    def delete_transaction(self):
        """Delete selected transaction - NEW"""
        selected = self.transaction_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a transaction to delete!")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?"):
            item = selected[0]
            values = self.transaction_tree.item(item)['values']
            
            # Find and remove the transaction
            for i, trans in enumerate(self.data['transactions']):
                if (trans['date'] == values[0] and 
                    trans['account'] == values[1] and 
                    trans['description'] == values[2]):
                    
                    # Reverse the transaction amount from account
                    for category, accounts in self.data['categories'].items():
                        if trans['account'] in accounts:
                            self.data['categories'][category][trans['account']] -= trans['amount']
                            break
                    
                    # Remove transaction
                    self.data['transactions'].pop(i)
                    self.save_data()
                    self.refresh_home()
                    self.refresh_tracker()
                    self.refresh_rule_tab()
                    messagebox.showinfo("Success", "Transaction deleted successfully!")
                    break

    def add_transaction(self):
        """Add transaction dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Transaction")
        dialog.geometry("550x550")
        dialog.configure(bg='#1e293b')
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Add New Transaction", font=('Segoe UI', 18, 'bold'),
                 bg='#1e293b', fg='#ffffff').pack(pady=20)

        form = tk.Frame(dialog, bg='#1e293b')
        form.pack(fill='both', expand=True, padx=40)

        # Date
        tk.Label(form, text="Date", font=('Segoe UI', 11, 'bold'),
                 bg='#1e293b', fg='#e2e8f0').grid(row=0, column=0, sticky='w', pady=10)
        date_entry = tk.Entry(form, font=('Segoe UI', 11), width=35, bg='#0f172a', 
                              fg='#e2e8f0', insertbackground='white')
        date_entry.insert(0, datetime.now().strftime('%B %d, %Y'))
        date_entry.grid(row=0, column=1, pady=10)

        # Account
        tk.Label(form, text="Account", font=('Segoe UI', 11, 'bold'),
                 bg='#1e293b', fg='#e2e8f0').grid(row=1, column=0, sticky='w', pady=10)

        all_accounts = []
        for category, accounts in self.data['categories'].items():
            for account in accounts.keys():
                all_accounts.append(f"{account} ({category})")

        account_var = tk.StringVar()
        account_combo = ttk.Combobox(form, textvariable=account_var, 
                                     values=all_accounts, font=('Segoe UI', 11), 
                                     state='readonly', width=33)
        if all_accounts:
            account_combo.current(0)
        account_combo.grid(row=1, column=1, pady=10)

        # Description
        tk.Label(form, text="Description", font=('Segoe UI', 11, 'bold'),
                 bg='#1e293b', fg='#e2e8f0').grid(row=2, column=0, sticky='w', pady=10)
        desc_entry = tk.Entry(form, font=('Segoe UI', 11), width=35, bg='#0f172a',
                              fg='#e2e8f0', insertbackground='white')
        desc_entry.grid(row=2, column=1, pady=10)

        # Type
        tk.Label(form, text="Type", font=('Segoe UI', 11, 'bold'),
                 bg='#1e293b', fg='#e2e8f0').grid(row=3, column=0, sticky='w', pady=10)
        type_var = tk.StringVar(value="expense")

        type_frame = tk.Frame(form, bg='#1e293b')
        type_frame.grid(row=3, column=1, sticky='w', pady=10)

        tk.Radiobutton(type_frame, text="💸 Expense", variable=type_var, value="expense",
                        font=('Segoe UI', 11), bg='#1e293b', fg='#e2e8f0',
                        selectcolor='#0f172a').pack(side='left', padx=15)
        tk.Radiobutton(type_frame, text="💰 Income", variable=type_var, value="income",
                        font=('Segoe UI', 11), bg='#1e293b', fg='#e2e8f0',
                        selectcolor='#0f172a').pack(side='left', padx=15)

        # Rule Category
        tk.Label(form, text="Rule Category", font=('Segoe UI', 11, 'bold'),
                 bg='#1e293b', fg='#e2e8f0').grid(row=4, column=0, sticky='w', pady=10)

        rule_var = tk.StringVar(value="-")
        rule_categories = ["-", "Growth", "Stability", "Essentials", "Rewards"]

        rule_combo = ttk.Combobox(form, textvariable=rule_var, 
                                  values=rule_categories, font=('Segoe UI', 11), 
                                  state='readonly', width=33)
        rule_combo.current(0)
        rule_combo.grid(row=4, column=1, pady=10)

        # Amount
        tk.Label(form, text="Amount", font=('Segoe UI', 11, 'bold'),
                 bg='#1e293b', fg='#e2e8f0').grid(row=5, column=0, sticky='w', pady=10)
        amount_entry = tk.Entry(form, font=('Segoe UI', 11), width=35, bg='#0f172a',
                                fg='#e2e8f0', insertbackground='white')
        amount_entry.grid(row=5, column=1, pady=10)

        def save_transaction():
            try:
                date = date_entry.get().strip()
                account_full = account_var.get()
                account = account_full.split(' (')[0] if account_full else ""
                description = desc_entry.get().strip()
                amount = float(amount_entry.get())
                rule_category = rule_var.get()

                if not account or not description:
                    messagebox.showwarning("Warning", "Please fill all fields!")
                    return

                if type_var.get() == "expense":
                    amount = -abs(amount)
                else:
                    amount = abs(amount)

                category = None
                for cat, accounts in self.data['categories'].items():
                    if account in accounts:
                        category = cat
                        break

                if category:
                    self.data['categories'][category][account] += amount
                    self.data['transactions'].append({
                        'date': date,
                        'account': account,
                        'description': description,
                        'amount': amount,
                        'rule_category': rule_category,
                        'timestamp': datetime.now().isoformat()
                    })

                    self.save_data()
                    self.refresh_home()
                    self.refresh_tracker()
                    self.refresh_rule_tab()

                    messagebox.showinfo("Success", "Transaction added successfully!")
                    dialog.destroy()

            except ValueError:
                messagebox.showerror("Error", "Invalid amount!")

        btn_frame = tk.Frame(dialog, bg='#1e293b')
        btn_frame.pack(pady=30)

        tk.Button(btn_frame, text="💾 Save Transaction", font=('Segoe UI', 11, 'bold'),
                   bg='#10b981', fg='white', relief='flat', cursor='hand2',
                   padx=30, pady=12, command=save_transaction).pack(side='left', padx=10)

        tk.Button(btn_frame, text="✖ Cancel", font=('Segoe UI', 11, 'bold'),
                   bg='#64748b', fg='white', relief='flat', cursor='hand2',
                   padx=30, pady=12, command=dialog.destroy).pack(side='left', padx=10)

    # --- ENTIRE SETTINGS TAB REBUILT FOR SCROLLING ---
    def build_settings_tab(self):
        """Build settings tab"""
        # Create main container with scrollbar
        main_container = tk.Frame(self.settings_frame, bg='#0f172a')
        main_container.pack(fill='both', expand=True)

        # Canvas and scrollbar
        self.settings_canvas = tk.Canvas(main_container, bg='#0f172a', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=self.settings_canvas.yview)

        # This frame will hold all the content
        self.settings_content = tk.Frame(self.settings_canvas, bg='#0f172a')

        # Configure scrolling
        self.settings_content.bind("<Configure>", lambda e: self.settings_canvas.configure(scrollregion=self.settings_canvas.bbox("all")))
        
        canvas_frame = self.settings_canvas.create_window((0, 0), window=self.settings_content, anchor="nw")

        def configure_canvas(event):
            self.settings_canvas.itemconfig(canvas_frame, width=event.width)

        self.settings_canvas.bind('<Configure>', configure_canvas)
        self.settings_canvas.configure(yscrollcommand=scrollbar.set)

        # Bind mouse wheel
        self._bind_mousewheel(self.settings_canvas, self.settings_canvas)
        self._bind_mousewheel(self.settings_content, self.settings_canvas)
        
        self.settings_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- All content now goes into self.settings_content ---

        # Header (parent changed to self.settings_content)
        header = tk.Frame(self.settings_content, bg='#1e293b', height=80)
        header.pack(fill='x', padx=20, pady=20)

        header_inner = tk.Frame(header, bg='#1e293b')
        header_inner.pack(fill='both', expand=True, padx=30, pady=20)

        tk.Label(header_inner, text="⚙️ Settings", font=('Segoe UI', 24, 'bold'),
                 bg='#1e293b', fg='#ffffff').pack(side='left')

        # Content (parent changed to self.settings_content)
        content = tk.Frame(self.settings_content, bg='#0f172a')
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Rule Percentages section (parent is 'content', which is correct)
        rule_section = tk.Frame(content, bg='#1e293b')
        rule_section.pack(fill='x', padx=0, pady=10)

        tk.Label(rule_section, text="✅ Rule Percentages", font=('Segoe UI', 16, 'bold'),
                 bg='#1e293b', fg='#ffffff').pack(anchor='w', padx=30, pady=(20, 15))

        tk.Label(rule_section, text="Customize your financial allocation percentages (must total 100%)", 
                 font=('Segoe UI', 10),
                 bg='#1e293b', fg='#94a3b8').pack(anchor='w', padx=30, pady=(0, 15))

        rules = self.data.get('rule_percentages', {
            'growth': 25,
            'stability': 15,
            'essentials': 50,
            'rewards': 10
        })

        rule_frame = tk.Frame(rule_section, bg='#1e293b')
        rule_frame.pack(fill='x', padx=30, pady=(0, 20))

        # Growth
        growth_frame = tk.Frame(rule_frame, bg='#1e293b')
        growth_frame.pack(fill='x', pady=5)
        tk.Label(growth_frame, text="🚀 Growth:", font=('Segoe UI', 11),
                 bg='#1e293b', fg='#e2e8f0', width=15, anchor='w').pack(side='left', padx=10)
        growth_entry = tk.Entry(growth_frame, font=('Segoe UI', 11), width=10,
                                bg='#0f172a', fg='#e2e8f0', insertbackground='white')
        growth_entry.insert(0, str(rules['growth']))
        growth_entry.pack(side='left', padx=10)
        tk.Label(growth_frame, text="%", font=('Segoe UI', 11),
                 bg='#1e293b', fg='#94a3b8').pack(side='left')

        # Stability
        stability_frame = tk.Frame(rule_frame, bg='#1e293b')
        stability_frame.pack(fill='x', pady=5)
        tk.Label(stability_frame, text="🛡️ Stability:", font=('Segoe UI', 11),
                 bg='#1e293b', fg='#e2e8f0', width=15, anchor='w').pack(side='left', padx=10)
        stability_entry = tk.Entry(stability_frame, font=('Segoe UI', 11), width=10,
                                   bg='#0f172a', fg='#e2e8f0', insertbackground='white')
        stability_entry.insert(0, str(rules['stability']))
        stability_entry.pack(side='left', padx=10)
        tk.Label(stability_frame, text="%", font=('Segoe UI', 11),
                 bg='#1e293b', fg='#94a3b8').pack(side='left')

        # Essentials
        essentials_frame = tk.Frame(rule_frame, bg='#1e293b')
        essentials_frame.pack(fill='x', pady=5)
        tk.Label(essentials_frame, text="🏠 Essentials:", font=('Segoe UI', 11),
                 bg='#1e293b', fg='#e2e8f0', width=15, anchor='w').pack(side='left', padx=10)
        essentials_entry = tk.Entry(essentials_frame, font=('Segoe UI', 11), width=10,
                                    bg='#0f172a', fg='#e2e8f0', insertbackground='white')
        essentials_entry.insert(0, str(rules['essentials']))
        essentials_entry.pack(side='left', padx=10)
        tk.Label(essentials_frame, text="%", font=('Segoe UI', 11),
                 bg='#1e293b', fg='#94a3b8').pack(side='left')

        # Rewards
        rewards_frame = tk.Frame(rule_frame, bg='#1e293b')
        rewards_frame.pack(fill='x', pady=5)
        tk.Label(rewards_frame, text="🎉 Rewards:", font=('Segoe UI', 11),
                 bg='#1e293b', fg='#e2e8f0', width=15, anchor='w').pack(side='left', padx=10)
        rewards_entry = tk.Entry(rewards_frame, font=('Segoe UI', 11), width=10,
                                 bg='#0f172a', fg='#e2e8f0', insertbackground='white')
        rewards_entry.insert(0, str(rules['rewards']))
        rewards_entry.pack(side='left', padx=10)
        tk.Label(rewards_frame, text="%", font=('Segoe UI', 11),
                 bg='#1e293b', fg='#94a3b8').pack(side='left')

        def update_rule_percentages():
            try:
                growth = float(growth_entry.get())
                stability = float(stability_entry.get())
                essentials = float(essentials_entry.get())
                rewards = float(rewards_entry.get())

                total = growth + stability + essentials + rewards

                if abs(total - 100) > 0.01:
                    messagebox.showerror("Error", f"Percentages must total 100%! Current total: {total}%")
                    return

                self.data['rule_percentages'] = {
                    'growth': growth,
                    'stability': stability,
                    'essentials': essentials,
                    'rewards': rewards
                }

                self.save_data()
                self.refresh_rule_tab()
                messagebox.showinfo("Success", "Rule percentages updated successfully!")

            except ValueError:
                messagebox.showerror("Error", "Invalid percentage values!")

        btn_frame = tk.Frame(rule_frame, bg='#1e293b')
        btn_frame.pack(fill='x', pady=15)

        tk.Button(btn_frame, text="✓ Update Percentages", font=('Segoe UI', 11, 'bold'),
                   bg='#3b82f6', fg='white', relief='flat', cursor='hand2',
                   padx=20, pady=10, command=update_rule_percentages).pack(side='left', padx=10)

        # Exchange rate section
        rate_section = tk.Frame(content, bg='#1e293b')
        rate_section.pack(fill='x', padx=0, pady=10)

        tk.Label(rate_section, text="💱 Exchange Rate", font=('Segoe UI', 16, 'bold'),
                 bg='#1e293b', fg='#ffffff').pack(anchor='w', padx=30, pady=(20, 15))

        rate_frame = tk.Frame(rate_section, bg='#1e293b')
        rate_frame.pack(fill='x', padx=30, pady=(0, 20))

        tk.Label(rate_frame, text="USD to LKR Rate:", font=('Segoe UI', 12),
                 bg='#1e293b', fg='#e2e8f0').pack(side='left', padx=10)

        rate_entry = tk.Entry(rate_frame, font=('Segoe UI', 12), width=15,
                              bg='#0f172a', fg='#e2e8f0', insertbackground='white')
        rate_entry.insert(0, str(self.usd_to_lkr))
        rate_entry.pack(side='left', padx=10)

        def update_rate():
            try:
                new_rate = float(rate_entry.get())
                self.usd_to_lkr = new_rate
                self.save_data()
                self.refresh_home()
                self.refresh_rule_tab()
                messagebox.showinfo("Success", f"Exchange rate updated to {new_rate} LKR")
            except ValueError:
                messagebox.showerror("Error", "Invalid rate!")

        tk.Button(rate_frame, text="✓ Update", font=('Segoe UI', 11, 'bold'),
                   bg='#3b82f6', fg='white', relief='flat', cursor='hand2',
                   padx=20, pady=10, command=update_rate).pack(side='left', padx=10)

        # Account management section
        acc_section = tk.Frame(content, bg='#1e293b')
        acc_section.pack(fill='x', padx=0, pady=10)

        tk.Label(acc_section, text="🔧 Account Management", font=('Segoe UI', 16, 'bold'),
                 bg='#1e293b', fg='#ffffff').pack(anchor='w', padx=30, pady=(20, 15))

        btn_container = tk.Frame(acc_section, bg='#1e293b')
        btn_container.pack(anchor='w', padx=30, pady=(0, 20))

        tk.Button(btn_container, text="🗑️ Delete Account", font=('Segoe UI', 11, 'bold'),
                   bg='#ef4444', fg='white', relief='flat', cursor='hand2',
                   padx=25, pady=12, command=self.delete_account).pack(anchor='w', pady=8)

        tk.Button(btn_container, text="✏️ Rename Account", font=('Segoe UI', 11, 'bold'),
                   bg='#f59e0b', fg='white', relief='flat', cursor='hand2',
                   padx=25, pady=12, command=self.rename_account).pack(anchor='w', pady=8)

        # App info section
        info_section = tk.Frame(content, bg='#1e293b')
        info_section.pack(fill='x', padx=0, pady=10)

        tk.Label(info_section, text="ℹ️ Application Info", font=('Segoe UI', 16, 'bold'),
                 bg='#1e293b', fg='#ffffff').pack(anchor='w', padx=30, pady=(20, 15))

        info_text = tk.Label(info_section, 
                             text="Finance Tracker Pro v3.0 with 25/15/50/10 Rule\nModern financial management application\n© 2024 All Rights Reserved",
                             font=('Segoe UI', 10), bg='#1e293b', fg='#94a3b8', justify='left')
        info_text.pack(anchor='w', padx=30, pady=(0, 20))
    # --- END OF SETTINGS TAB FIX ---

    def delete_account(self):
        """Delete an account"""
        all_accounts = []
        for category, accounts in self.data['categories'].items():
            for account in accounts.keys():
                all_accounts.append((account, category))

        if not all_accounts:
            messagebox.showinfo("Info", "No accounts to delete!")
            return

        account_names = [f"{acc} ({cat})" for acc, cat in all_accounts]

        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Account")
        dialog.geometry("500x250")
        dialog.configure(bg='#1e293b')
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="🗑️ Delete Account", font=('Segoe UI', 18, 'bold'),
                 bg='#1e293b', fg='#ffffff').pack(pady=20)

        tk.Label(dialog, text="Select account to delete:", font=('Segoe UI', 11),
                 bg='#1e293b', fg='#e2e8f0').pack(pady=10)

        account_var = tk.StringVar()
        combo = ttk.Combobox(dialog, textvariable=account_var, values=account_names,
                             font=('Segoe UI', 11), state='readonly', width=35)
        combo.pack(pady=10)
        if account_names:
            combo.current(0)

        def confirm_delete():
            selected = account_var.get()
            if selected:
                account = selected.split(' (')[0]
                category = selected.split('(')[1].rstrip(')')

                if messagebox.askyesno("Confirm", f"Are you sure you want to delete {account}?"):
                    del self.data['categories'][category][account]
                    self.save_data()
                    self.refresh_home()
                    self.refresh_rule_tab()
                    messagebox.showinfo("Success", "Account deleted successfully!")
                    dialog.destroy()

        btn_frame = tk.Frame(dialog, bg='#1e293b')
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="🗑️ Delete", font=('Segoe UI', 11, 'bold'),
                   bg='#ef4444', fg='white', relief='flat', cursor='hand2',
                   padx=30, pady=12, command=confirm_delete).pack(side='left', padx=10)

        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 11, 'bold'),
                   bg='#64748b', fg='white', relief='flat', cursor='hand2',
                   padx=30, pady=12, command=dialog.destroy).pack(side='left', padx=10)

    def rename_account(self):
        """Rename an account"""
        all_accounts = []
        for category, accounts in self.data['categories'].items():
            for account in accounts.keys():
                all_accounts.append((account, category))

        if not all_accounts:
            messagebox.showinfo("Info", "No accounts to rename!")
            return

        account_names = [f"{acc} ({cat})" for acc, cat in all_accounts]

        dialog = tk.Toplevel(self.root)
        dialog.title("Rename Account")
        dialog.geometry("500x300")
        dialog.configure(bg='#1e293b')
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="✏️ Rename Account", font=('Segoe UI', 18, 'bold'),
                 bg='#1e293b', fg='#ffffff').pack(pady=20)

        tk.Label(dialog, text="Select account:", font=('Segoe UI', 11, 'bold'),
                 bg='#1e293b', fg='#e2e8f0').pack(pady=5)

        account_var = tk.StringVar()
        combo = ttk.Combobox(dialog, textvariable=account_var, values=account_names,
                             font=('Segoe UI', 11), state='readonly', width=35)
        combo.pack(pady=5)
        if account_names:
            combo.current(0)

        tk.Label(dialog, text="New name:", font=('Segoe UI', 11, 'bold'),
                 bg='#1e293b', fg='#e2e8f0').pack(pady=10)

        new_name_entry = tk.Entry(dialog, font=('Segoe UI', 11), width=35,
                                  bg='#0f172a', fg='#e2e8f0', insertbackground='white')
        new_name_entry.pack(pady=5)

        def confirm_rename():
            selected = account_var.get()
            new_name = new_name_entry.get().strip()

            if selected and new_name:
                old_name = selected.split(' (')[0]
                category = selected.split('(')[1].rstrip(')')

                if new_name in self.data['categories'][category]:
                    messagebox.showerror("Error", "Account name already exists!")
                    return

                balance = self.data['categories'][category][old_name]
                del self.data['categories'][category][old_name]
                self.data['categories'][category][new_name] = balance

                for trans in self.data['transactions']:
                    if trans['account'] == old_name:
                        trans['account'] = new_name

                self.save_data()
                self.refresh_home()
                self.refresh_tracker()
                self.refresh_rule_tab()
                messagebox.showinfo("Success", "Account renamed successfully!")
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Please enter a new name!")

        btn_frame = tk.Frame(dialog, bg='#1e293b')
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="✓ Rename", font=('Segoe UI', 11, 'bold'),
                   bg='#f59e0b', fg='white', relief='flat', cursor='hand2',
                   padx=30, pady=12, command=confirm_rename).pack(side='left', padx=10)

        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 11, 'bold'),
                   bg='#64748b', fg='white', relief='flat', cursor='hand2',
                   padx=30, pady=12, command=dialog.destroy).pack(side='left', padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    root.mainloop()