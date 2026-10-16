if __name__ == "__main__":
    try:
        from src.__main__ import Main
        import sys

        Main.main()
    except Exception as e:
        print(f'Special error: {e}', file=sys.stderr)
    except KeyboardInterrupt:
        print("\nCommand error: pacman has been interrupted", file=sys.stderr)
