from automating import Driver

def main() -> None:
    """Main entry point."""
    driver = Driver()
    driver.login()
    total = driver.analyze_pages(pages_quantity=12)
    print(f"All: {total}")

    user_input = input("Quit? ")
    if user_input.lower() == 'y':
        driver.quit()


if __name__ == "__main__":
    main()