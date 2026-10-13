
import os
from pathlib import Path

import pandas as pd


class EmployeeDataAnalysis:
    """Analyze employee data using Pandas and CSV files."""

    def __init__(self, input_file: str) -> None:
        self.input_file: Path = Path(input_file)
        self.output_dir: Path = Path("output")
        self.data: pd.DataFrame | None = None

        # Create output folder automatically
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_data(self) -> bool:
        """Load and validate employee data from CSV."""

        try:
            if not self.input_file.is_file():
                print(f"Error: CSV file not found: {self.input_file}")
                return False

            data: pd.DataFrame = pd.read_csv(
                self.input_file,
                encoding="utf-8"
            )

            required_columns = {
                "employee_id",
                "name",
                "department",
                "salary",
                "experience",
            }

            missing_columns = required_columns.difference(data.columns)

            if missing_columns:
                print(
                    "Error: Missing columns:",
                    ", ".join(sorted(missing_columns))
                )
                return False

            if data.empty:
                print("Error: Employee CSV file is empty.")
                return False

            # Validate numeric columns
            data["salary"] = pd.to_numeric(
                data["salary"], errors="coerce"
            )
            data["experience"] = pd.to_numeric(
                data["experience"], errors="coerce"
            )

            if data["salary"].isna().any():
                print("Error: Salary column contains invalid values.")
                return False

            if (data["salary"] < 0).any():
                print("Error: Salary cannot be negative.")
                return False

            self.data = data

            print("\nEmployee data loaded successfully!")
            print("\nEmployee Records:")
            print(self.data.to_string(index=False))

            return True

        except (OSError, UnicodeError, pd.errors.ParserError) as error:
            print(f"Error while reading CSV: {error}")
            return False

    def calculate_average_salary(self) -> float:
        """Calculate average salary."""

        assert self.data is not None

        average_salary = float(self.data["salary"].mean())

        print(f"\nAverage Salary: Rs. {average_salary:,.2f}")

        return average_salary

    def count_departments(self) -> None:
        """Count employees in each department and export results."""

        assert self.data is not None

        department_count = self.data["department"].value_counts()

        print("\nEmployees by Department:")
        print(department_count.to_string())

        output_file = self.output_dir / "department_count.csv"

        department_count.to_csv(
            output_file,
            header=["employee_count"],
            index_label="department",
        )

        print(f"\nDepartment report saved: {output_file}")

    def filter_high_salary(self, threshold: float) -> None:
        """Find employees earning above the given salary."""

        assert self.data is not None

        filtered_data = self.data[
            self.data["salary"] > threshold
        ]

        print(f"\nEmployees earning above Rs. {threshold:,.2f}:")

        if filtered_data.empty:
            print("No employees found above this threshold.")
        else:
            print(filtered_data.to_string(index=False))

        output_file = self.output_dir / "high_salary_employees.csv"

        filtered_data.to_csv(output_file, index=False)

        print(f"\nFiltered report saved: {output_file}")
        print(f"Employees matching the filter: {len(filtered_data)}")

    def export_full_data(self) -> None:
        """Export the complete employee dataset."""

        assert self.data is not None

        output_file = self.output_dir / "employee_analysis.csv"

        self.data.to_csv(output_file, index=False)

        print(f"\nComplete employee data saved: {output_file}")

    def run(self) -> None:
        """Run the complete employee analysis project."""

        print("=" * 50)
        print("       EMPLOYEE DATA ANALYSIS SYSTEM")
        print("=" * 50)

        if not self.load_data():
            return

        self.calculate_average_salary()
        self.count_departments()

        try:
            user_input = input(
                "\nEnter salary threshold (Rs.): "
            ).strip()

            threshold = float(user_input)

            if not pd.notna(threshold) or threshold < 0:
                print("Error: Enter a valid non-negative salary.")
                return

        except ValueError:
            print("Error: Please enter a numeric salary.")
            return

        self.filter_high_salary(threshold)
        self.export_full_data()

        print("\n" + "=" * 50)
        print("Analysis completed successfully!")
        print(f"Check the '{self.output_dir}' folder for reports.")
        print("=" * 50)


if __name__ == "__main__":
    project = EmployeeDataAnalysis("employees.csv")
    project.run()
