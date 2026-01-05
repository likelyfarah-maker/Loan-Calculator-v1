import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pandas as pd

# Set appearance mode and color theme
ctk.set_appearance_mode("light")  # Default to light mode
ctk.set_default_color_theme("blue")  # Can be "blue", "green", "dark-blue"

class LoanCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("💰 Loan Repayment Calculator")
        self.geometry("1000x800")
        self.minsize(900, 700)
        
        # Create main container with scrollbar
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar for scrollable content
        self.canvas = tk.Canvas(self.main_frame, highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self.main_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, corner_radius=10)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.scrollbar.pack(side="right", fill="y", padx=(5, 0))
        
        # Bind mouse wheel to canvas
        self.canvas.bind("<Enter>", self._bind_to_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_from_mousewheel)
        
        # Initialize variables
        self.loan_amount = ctk.DoubleVar(value=5000.0)
        self.repayment_months = ctk.IntVar(value=6)
        
        # Create UI elements
        self.create_widgets()
        
    def _bind_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def create_widgets(self):
        # Title Section
        title_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        title_frame.pack(fill="x", padx=20, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="💰 Loan Repayment Calculator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(15, 5))
        
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Money Lending Services",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Separator
        separator1 = ctk.CTkFrame(title_frame, height=2, fg_color="gray")
        separator1.pack(fill="x", padx=10, pady=5)
        
        # Main Content Frame
        content_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create two columns
        left_column = ctk.CTkFrame(content_frame, corner_radius=10)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_column = ctk.CTkFrame(content_frame, corner_radius=10)
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Left Column - Input Section
        self.create_input_section(left_column)
        
        # Right Column - How it Works
        self.create_info_section(right_column)
        
        # Results Section
        self.create_results_section()
        
        # Disclaimer
        self.create_disclaimer()
    
    def create_input_section(self, parent):
        input_frame = ctk.CTkFrame(parent, corner_radius=10)
        input_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        input_title = ctk.CTkLabel(
            input_frame,
            text="Loan Details",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        input_title.pack(pady=(10, 15))
        
        # Loan Amount Input
        loan_label = ctk.CTkLabel(
            input_frame,
            text="Loan Amount (RM):",
            font=ctk.CTkFont(size=14)
        )
        loan_label.pack(anchor="w", padx=20, pady=(5, 0))
        
        loan_entry = ctk.CTkEntry(
            input_frame,
            textvariable=self.loan_amount,
            width=200,
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        loan_entry.pack(pady=(5, 15), padx=20)
        
        # Repayment Period Input
        period_label = ctk.CTkLabel(
            input_frame,
            text="Repayment Period (Months):",
            font=ctk.CTkFont(size=14)
        )
        period_label.pack(anchor="w", padx=20, pady=(5, 0))
        
        period_optionmenu = ctk.CTkOptionMenu(
            input_frame,
            variable=self.repayment_months,
            values=[str(i) for i in range(1, 13)],
            width=200,
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        period_optionmenu.pack(pady=(5, 20), padx=20)
        
        # Calculate Button
        calculate_btn = ctk.CTkButton(
            input_frame,
            text="Calculate Repayment",
            command=self.calculate,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8,
            height=40
        )
        calculate_btn.pack(pady=20, padx=20)
    
    def create_info_section(self, parent):
        info_frame = ctk.CTkFrame(parent, corner_radius=10)
        info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        info_title = ctk.CTkLabel(
            info_frame,
            text="How it Works",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        info_title.pack(pady=(10, 15))
        
        # Info Text
        info_text = """
Cost Structure:
• Management Fee: RM15 per month
• Stamp Duty: 0.5% of loan amount
• Repayment: Salary deduction

Interest Calculation:
1. Repayment Period Interest Rate = (Total Management Cost / Loan Amount) × 100%
2. Monthly Interest Rate = Repayment Period Interest Rate ÷ Number of Months

Example (RM5,000 for 6 months):
• Management: 6 × RM15 = RM90
• Repayment Period Interest Rate = (90 / 5000) × 100% = 1.8%
• Monthly Interest Rate = 1.8% ÷ 6 = 0.3%
        """
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=13),
            justify="left"
        )
        info_label.pack(pady=10, padx=20, anchor="w")
    
    def create_results_section(self):
        # Results Frame
        self.results_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        self.results_frame.pack(fill="x", padx=20, pady=10)
        
        # Results will be populated when calculate is called
        
    def create_disclaimer(self):
        disclaimer_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        disclaimer_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        disclaimer_text = (
            "⚠️ Disclaimer: This loan repayment calculator is for informational purposes only. "
            "It does not provide financial advice, offer loans, or represent a licensed money lending service."
        )
        
        disclaimer_label = ctk.CTkLabel(
            disclaimer_frame,
            text=disclaimer_text,
            font=ctk.CTkFont(size=11),
            wraplength=900,
            justify="center"
        )
        disclaimer_label.pack(pady=15, padx=20)
    
    def calculate_loan_repayment(self, loan_amount, num_months):
        """
        Core function to calculate loan repayment details
        """
        if loan_amount <= 0:
            raise ValueError("Loan amount must be positive")
        
        if num_months < 1 or num_months > 12:
            raise ValueError("Repayment period must be between 1 and 12 months")
        
        # Calculate costs
        management_cost = 15 * num_months
        stamp_duty = loan_amount * 0.005  # 0.5% stamp duty
        
        # Calculate repayment details
        total_repayment = loan_amount + management_cost + stamp_duty
        monthly_installment = total_repayment / num_months
        
        # Calculate interest rates according to the instructions
        # 1. Interest rate for the repayment period (in percentage)
        repayment_period_interest_rate = (management_cost / loan_amount) * 100
        
        # 2. Monthly interest rate (in percentage)
        monthly_interest_rate_percent = repayment_period_interest_rate / num_months
        
        # 3. Monthly interest rate as decimal (optional)
        monthly_interest_rate_decimal = management_cost / (loan_amount * num_months)
        
        return {
            'loan_amount': loan_amount,
            'repayment_months': num_months,
            'management_cost': management_cost,
            'stamp_duty': stamp_duty,
            'total_repayment': total_repayment,
            'monthly_installment': monthly_installment,
            'repayment_period_interest_rate': repayment_period_interest_rate,
            'monthly_interest_rate_percent': monthly_interest_rate_percent,
            'monthly_interest_rate_decimal': monthly_interest_rate_decimal,
            'total_fees': management_cost + stamp_duty
        }
    
    def format_interest_rate(self, rate):
        """
        Format interest rate to 3 decimal places if there are non-zero digits after 2 decimal places
        """
        if round(rate, 2) != rate:
            return f"{rate:.3f}%"
        else:
            return f"{rate:.2f}%"
    
    def clear_results(self):
        """Clear previous results"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
    
    def calculate(self):
        try:
            self.clear_results()
            
            loan_amount = self.loan_amount.get()
            num_months = self.repayment_months.get()
            
            # Calculate loan details
            result = self.calculate_loan_repayment(loan_amount, num_months)
            
            # Format interest rates
            period_interest_formatted = self.format_interest_rate(result['repayment_period_interest_rate'])
            monthly_interest_formatted = self.format_interest_rate(result['monthly_interest_rate_percent'])
            
            # Results Title
            results_title = ctk.CTkLabel(
                self.results_frame,
                text="Calculation Results",
                font=ctk.CTkFont(size=20, weight="bold")
            )
            results_title.pack(pady=(15, 20))
            
            # Main Results Grid
            results_grid = ctk.CTkFrame(self.results_frame, corner_radius=10)
            results_grid.pack(fill="x", padx=20, pady=10)
            
            # Create 4 columns for results
            for i in range(4):
                results_grid.columnconfigure(i, weight=1)
            
            # Monthly Installment
            monthly_frame = ctk.CTkFrame(results_grid, corner_radius=8)
            monthly_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(monthly_frame, text="Monthly Installment", 
                        font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
            ctk.CTkLabel(monthly_frame, text=f"RM {result['monthly_installment']:,.2f}", 
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(0, 10))
            
            # Total Repayment
            total_frame = ctk.CTkFrame(results_grid, corner_radius=8)
            total_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(total_frame, text="Total Repayment", 
                        font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
            ctk.CTkLabel(total_frame, text=f"RM {result['total_repayment']:,.2f}", 
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(0, 10))
            
            # Repayment Period Interest Rate
            period_interest_frame = ctk.CTkFrame(results_grid, corner_radius=8)
            period_interest_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(period_interest_frame, text="Repayment Period Interest Rate", 
                        font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
            ctk.CTkLabel(period_interest_frame, text=period_interest_formatted, 
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(0, 10))
            
            # Monthly Interest Rate
            monthly_interest_frame = ctk.CTkFrame(results_grid, corner_radius=8)
            monthly_interest_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(monthly_interest_frame, text="Monthly Interest Rate", 
                        font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
            ctk.CTkLabel(monthly_interest_frame, text=monthly_interest_formatted, 
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(0, 10))
            
            # Detailed Breakdown Section
            self.create_detailed_breakdown(result)
            
            # Repayment Schedule
            self.create_repayment_schedule(result)
            
            # Additional Info
            additional_frame = ctk.CTkFrame(self.results_frame, corner_radius=10)
            additional_frame.pack(fill="x", padx=20, pady=10)
            
            additional_label = ctk.CTkLabel(
                additional_frame,
                text=f"Additional Information: Monthly interest rate as decimal: {result['monthly_interest_rate_decimal']:.4f}",
                font=ctk.CTkFont(size=12)
            )
            additional_label.pack(pady=10)
            
        except ValueError as e:
            tk.messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    
    def create_detailed_breakdown(self, result):
        # Detailed Breakdown Container
        breakdown_container = ctk.CTkFrame(self.results_frame, corner_radius=10)
        breakdown_container.pack(fill="x", padx=20, pady=10)
        
        breakdown_title = ctk.CTkLabel(
            breakdown_container,
            text="Detailed Cost Breakdown",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        breakdown_title.pack(pady=(10, 15))
        
        # Two columns for breakdown
        breakdown_columns = ctk.CTkFrame(breakdown_container)
        breakdown_columns.pack(fill="x", padx=10, pady=10)
        breakdown_columns.columnconfigure(0, weight=1)
        breakdown_columns.columnconfigure(1, weight=1)
        
        # Cost Components
        cost_frame = ctk.CTkFrame(breakdown_columns, corner_radius=8)
        cost_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        ctk.CTkLabel(cost_frame, text="Cost Components", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 10))
        
        # Cost components data
        cost_data = [
            ("Loan Amount", f"RM {result['loan_amount']:,.2f}"),
            (f"Management Cost ({result['repayment_months']} months × RM15)", f"RM {result['management_cost']:,.2f}"),
            ("Stamp Duty (0.5%)", f"RM {result['stamp_duty']:,.2f}"),
            ("Total Repayment", f"RM {result['total_repayment']:,.2f}")
        ]
        
        for component, amount in cost_data:
            row_frame = ctk.CTkFrame(cost_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(row_frame, text=component, 
                        font=ctk.CTkFont(size=12), anchor="w").pack(side="left")
            ctk.CTkLabel(row_frame, text=amount, 
                        font=ctk.CTkFont(size=12, weight="bold"), anchor="e").pack(side="right")
        
        # Interest Calculation
        interest_frame = ctk.CTkFrame(breakdown_columns, corner_radius=8)
        interest_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        
        ctk.CTkLabel(interest_frame, text="Interest Calculation", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 10))
        
        # Interest calculation data
        interest_data = [
            ("Total Management Cost", f"{result['repayment_months']} × RM15 = RM {result['management_cost']:,.2f}"),
            ("Loan Amount", f"RM {result['loan_amount']:,.2f}"),
            ("Repayment Period Interest Rate", 
             f"(RM {result['management_cost']:,.2f} ÷ RM {result['loan_amount']:,.2f}) × 100 = {result['repayment_period_interest_rate']:.3f}%"),
            ("Monthly Interest Rate", 
             f"{result['repayment_period_interest_rate']:.3f}% ÷ {result['repayment_months']} = {result['monthly_interest_rate_percent']:.3f}%")
        ]
        
        for description, calculation in interest_data:
            row_frame = ctk.CTkFrame(interest_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(row_frame, text=description, 
                        font=ctk.CTkFont(size=12), anchor="w").pack(side="left")
            calc_label = ctk.CTkLabel(row_frame, text=calculation, 
                                    font=ctk.CTkFont(size=11), anchor="e", wraplength=300)
            calc_label.pack(side="right")
    
    def create_repayment_schedule(self, result):
        schedule_frame = ctk.CTkFrame(self.results_frame, corner_radius=10)
        schedule_frame.pack(fill="x", padx=20, pady=10)
        
        schedule_title = ctk.CTkLabel(
            schedule_frame,
            text="Repayment Schedule",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        schedule_title.pack(pady=(10, 15))
        
        # Create a frame for the table
        table_frame = ctk.CTkFrame(schedule_frame, corner_radius=8)
        table_frame.pack(fill="x", padx=10, pady=10)
        
        # Create table headers
        headers = ["Month", "Payment (RM)", "Remaining Balance (RM)"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                table_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                height=30
            )
            header_label.grid(row=0, column=i, padx=1, pady=1, sticky="nsew")
            table_frame.columnconfigure(i, weight=1)
        
        # Generate schedule data
        remaining_balance = result['total_repayment']
        schedule_data = []
        
        for month in range(1, result['repayment_months'] + 1):
            if month == result['repayment_months']:
                monthly_payment = remaining_balance
            else:
                monthly_payment = result['monthly_installment']
            
            remaining_balance -= monthly_payment
            schedule_data.append({
                "month": month,
                "payment": monthly_payment,
                "remaining": max(0, round(remaining_balance, 2))
            })
        
        # Populate table with data
        for row, data in enumerate(schedule_data, 1):
            month_label = ctk.CTkLabel(
                table_frame,
                text=str(data["month"]),
                font=ctk.CTkFont(size=11),
                height=25
            )
            month_label.grid(row=row, column=0, padx=1, pady=1, sticky="nsew")
            
            payment_label = ctk.CTkLabel(
                table_frame,
                text=f"{data['payment']:,.2f}",
                font=ctk.CTkFont(size=11),
                height=25
            )
            payment_label.grid(row=row, column=1, padx=1, pady=1, sticky="nsew")
            
            remaining_label = ctk.CTkLabel(
                table_frame,
                text=f"{data['remaining']:,.2f}",
                font=ctk.CTkFont(size=11),
                height=25
            )
            remaining_label.grid(row=row, column=2, padx=1, pady=1, sticky="nsew")

def main():
    app = LoanCalculator()
    app.mainloop()

if __name__ == "__main__":
    main()