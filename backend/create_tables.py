"""
Database Tables Creation Script
Creates all database tables for Smart Food Tracker
"""
import sys
import os

# Add project path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.database import Base, engine
from app.models import visual_portion, meal_record, daily_goal  # noqa: F401


class Colors:
    """Terminal colors"""
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def print_header(title: str):
    """Print header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{title}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}\n")


def print_success(text: str):
    print(f"{Colors.GREEN}✓{Colors.RESET} {text}")


def print_error(text: str):
    print(f"{Colors.RED}✗{Colors.RESET} {text}")


def print_info(text: str):
    print(f"{Colors.CYAN}○{Colors.RESET} {text}")


def main():
    """Main function"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════════════╗")
    print("║   Smart Food Tracker - Database Tables        ║")
    print("║                    Creation Script             ║")
    print("╚════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

    print_header("Step 1: Importing Models")
    print_info("Importing all database models...")

    # Models are imported at the top, they are registered to Base.metadata
    print_success("Models imported successfully")

    # List all tables that will be created
    print_header("Step 2: Tables to Create")
    tables_to_create = list(Base.metadata.tables.keys())
    for table in tables_to_create:
        print_info(f"  - {table}")

    print_header("Step 3: Creating Tables")
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print_success("All database tables created successfully")
    except Exception as e:
        print_error(f"Failed to create database tables: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    # Verification
    print_header("Step 4: Verification")
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        print_success(f"Verified {len(existing_tables)} tables in database:")
        for table in existing_tables:
            print_info(f"  - {table}")

        if set(existing_tables) >= set(tables_to_create):
            print_success("\n✓ All required tables exist")
        else:
            missing = set(tables_to_create) - set(existing_tables)
            print_error(f"\n✗ Missing tables: {missing}")
            return 1

    except Exception as e:
        print_error(f"Verification failed: {str(e)}")
        return 1

    # Summary
    print_header("Summary")
    print(f"{Colors.GREEN}{Colors.BOLD}✓ Database tables creation completed!{Colors.RESET}")
    print(f"\n{Colors.BOLD}Database location:{Colors.RESET}")
    print(f"  {os.path.abspath('smart_food.db')}")
    print(f"\n{Colors.BOLD}Next steps:{Colors.RESET}")
    print(f"  1. Import food data: python init_extended_database.py")
    print(f"  2. Configure .env file with GLM_API_KEY")
    print(f"  3. Start backend service: uvicorn app.main:app --reload")

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
