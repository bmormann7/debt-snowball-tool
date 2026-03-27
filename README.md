# Debt Snowball Simulator (Python)

A modular, extensible Python project that simulates debt payoff using the **Debt Snowball** method.  
Built with clean architecture, testable components, and both CLI and UI layers.

This project was created to:
- Build a real, production‑style Python codebase  
- Practice modular design and separation of concerns  
- Create a personal finance tool that produces accurate amortization schedules  
- Demonstrate engineering skills for a professional portfolio  

---

## Features

### ✔ Fully Functional Core Engine
- Calculates monthly interest  
- Applies minimum payments  
- Applies snowball payments  
- Supports optional extra payments  
- Generates a complete amortization schedule  
- Determines payoff order and timeline  

### ✔ Clean, Modular Architecture

```text
engine/         # Core payoff logic  
models/         # Debt model  
storage/        # File I/O for saving/loading debts  
cli/            # Command-line interface  
streamlit_app/  # UI prototype (optional)  
tests/          # Unit tests for engine logic  
```

### Installation

Clone the repository:

```bash
git clone https://github.com/bmormann7/debt-snowball-tool.git
cd debt-snowball-tool

pip install -r requirements.txt
```

## Running the CLI

To run the command‑line interface:

```bash
python cli/main.py
```

## Running the Streamlit App (Optional)

To launch the Streamlit prototype UI:

```bash
streamlit run streamlit_app/app.py
```

## Project Structure

The project is organized into modular components to keep the logic clean, testable, and easy to extend.

```text
engine/         # Core payoff logic  
models/         # Debt model definitions  
storage/        # Saving/loading debt profiles  
cli/            # Command-line interface  
streamlit_app/  # Streamlit UI prototype  
utils/          # Helper functions  
data/           # Example datasets  
charts/         # Generated charts and figures  
```

## How the Debt Snowball Works

The Debt Snowball method focuses on paying off debts from smallest balance to largest balance.  
As each debt is paid off, its payment amount “snowballs” into the next debt, accelerating payoff speed.

This project automates the entire process by:
- Calculating monthly interest  
- Applying minimum payments  
- Rolling over freed payments to the next debt  
- Generating a full amortization schedule  
- Predicting payoff dates and total interest paid  

## Example Output

Here is an example of what the CLI produces when running a simulation:

```text
Month 1  |  Debt: Credit Card A  |  Payment: $200.00  |  Interest: $12.50  |  Remaining: $1,812.50
Month 2  |  Debt: Credit Card A  |  Payment: $200.00  |  Interest: $11.33  |  Remaining: $1,623.83
...
Debt Paid Off: Credit Card A in 11 months
Snowball added to next debt: +$200.00
```

## Saving and Loading Debt Profiles

You can save your debt configurations to a JSON file and load them later for quick simulations.

```bash
python cli/main.py --save debts.json
python cli/main.py --load debts.json
```

## Exporting and Visualizing Results

The project can generate charts, tables, and amortization exports to help visualize your payoff progress.

Common outputs include:
- Monthly balance charts  
- Interest‑vs‑principal breakdowns  
- Full amortization tables  
- Snowball progression timelines  

Exports are saved automatically inside the `charts/` or `data/` directories depending on the output type.

## Roadmap

Planned enhancements for future versions:

- Add Avalanche payoff mode  
- Add hybrid Snowball/Avalanche strategy  
- Add interactive debt entry wizard  
- Add CSV and Excel export options  
- Add richer Streamlit dashboards  
- Add payoff date forecasting  
- Add interest‑savings comparison charts  
- Add pretty terminal tables for CLI output  
- Add full test coverage for engine and models  

## License

This project is open‑source and available under the MIT License.  
You are free to use, modify, and distribute it as long as the original license is included.

## Acknowledgments

This project was inspired by the Debt Snowball method popularized by personal finance educators.  
Special thanks to the open‑source community for tools, libraries, and patterns that helped shape this project’s architecture.


### Updates

Intelligent File Selection & Last‑Used Memory
The CLI now includes a smart file‑loading system that makes it easy to switch between multiple debt profiles:

Automatically scans the data/ directory for all .json debt files

Displays them in a numbered, alphabetical menu

Remembers the last used file and sets it as the default

Allows the user to press Enter to quickly reload the default file

Stores the default in data/.last_used_file for seamless future sessions

This upgrade improves usability for both personal and public use cases — for example, keeping a private debts_personal.json locally while maintaining a public debts_example.json in the repository.