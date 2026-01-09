import pandas as pd
from transformers import pipeline

# --- Robust Financial Chatbot Implementation ---
class RobustFinancialChatbot:
    def __init__(self, holdings_path, trades_path):
        print("System: Loading Data...")
        self.holdings = pd.read_csv(holdings_path)
        self.trades = pd.read_csv(trades_path)

        # Intent Labels
        self.intents = [
            "count the number of trades or holdings",
            "check the profit and loss performance",
            "greeting",
            "ask about manager, ceo, sector, or unknown details"
        ]

        print("System: Loading AI Model...")
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def ask(self, user_question):
        # 1. Classify Intent
        result = self.classifier(user_question, self.intents)
        top_intent = result['labels'][0]
        confidence = result['scores'][0]

        # 2. Safety Overrides
        q_lower = user_question.lower()

        # Performance Logic
        if "best" in q_lower or "better" in q_lower or "worst" in q_lower or "profit" in q_lower or "p&l" in q_lower:
            return self._handle_performance()

        # Count Logic
        if top_intent == "count the number of trades or holdings" or "how many" in q_lower or "count" in q_lower or "number of" in q_lower:
            return self._handle_counts(user_question)

        # Greeting
        if top_intent == "greeting" and confidence > 0.8:
            return "Hello! I can answer questions about fund holdings and trades."

        # Default Fallback
        return "Sorry can not find the answer"

    def _handle_counts(self, question):
        q_lower = question.lower()

        # 1. Keyword Guardrail
        valid_count_keywords = ['count', 'number', 'how many', 'total', 'quantity', 'amount']
        if not any(k in q_lower for k in valid_count_keywords):
            return "Sorry can not find the answer"

        # 2. Get all funds
        all_funds = list(set(self.holdings['PortfolioName'].unique()) | set(self.trades['PortfolioName'].unique()))
        all_funds.sort(key=len, reverse=True)

        found_fund = None
        for fund in all_funds:
            if fund.lower() in q_lower:
                found_fund = fund
                break

        if found_fund:
            h_count = self.holdings[self.holdings['PortfolioName'] == found_fund].shape[0]
            t_count = self.trades[self.trades['PortfolioName'] == found_fund].shape[0]
            return f"Fund '{found_fund}' has {h_count} holdings and {t_count} trades."
        else:
            return "Sorry can not find the answer"

    def _handle_performance(self):
        if 'PL_YTD' not in self.holdings.columns:
            return "Sorry can not find the answer"

        perf = self.holdings.groupby('PortfolioName')['PL_YTD'].sum().sort_values(ascending=False)
        top_fund = perf.index[0]
        top_val = perf.iloc[0]
        return f"The best performing fund is '{top_fund}' with a Yearly P&L of ${top_val:,.2f}."

# --- Test Run ---
if __name__ == "__main__":
    bot = RobustFinancialChatbot('data/holdings.csv', 'data/trades.csv')

    print("\n--- TEST 1:")
    q1 = "What is the total Yearly P&L for all funds combined?"
    print(f"Q: {q1}")
    print(f"A: {bot.ask(q1)}")

    print("\n--- TEST 2: ")
    q2 = "What is the total number of trades for Northpoint 401K?"
    print(f"Q: {q2}")
    print(f"A: {bot.ask(q2)}")

    print("\n--- TEST 3: ")
    q3 = "Who is the manager of the Garfield fund?"
    print(f"Q: {q3}")
    print(f"A: {bot.ask(q3)}")

