def format_time(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60

    if minutes == 0:
        return f"{seconds} secs"
    elif remaining_seconds == 0:
        return f"{minutes} mins"
    else:
        return f"{minutes} mins {remaining_seconds} secs"

if __name__ == "__main__":
    input_seconds = int(input("Enter the number of seconds: "))
    while input_seconds > 0:
        print(format_time(input_seconds))
        input_seconds = int(input("Enter the number of seconds: "))
    print("Goodbye!")