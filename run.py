from memory.store import load_state, save_state

def main():
    state = load_state()
    print("Loaded state:", state)
    save_state(state)
    print("State saved")

if __name__ == "__main__":
    main()