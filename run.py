from src.__main__ import Main

if __name__ == "__main__":
    try:
        main = Main()
        main.main()
    except Exception as e:
        print(f'Special error: {e}')