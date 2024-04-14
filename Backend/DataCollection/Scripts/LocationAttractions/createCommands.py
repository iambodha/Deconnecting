import os

def generate_commands(queries_folder, base_command):
    files = [f for f in os.listdir(queries_folder) if f.startswith("example-queries") and f.endswith(".txt")]
    files.sort()
    commands = []
    for file in files:
        input_file = file
        output_file = f"result_{os.path.splitext(file)[0]}.csv"
        command = base_command.format(input_file=input_file, output_file=output_file)
        commands.append(command + "\n")
    with open("allCommands.txt", "w") as f:
        f.writelines(commands)
    return commands

def main():
    base_command = "./google-maps-scraper -input ../Queries/{input_file} -results ../Results/{output_file} -exit-on-inactivity 3m"
    queries_folder = "Queries"
    generate_commands(queries_folder, base_command)
    print("\033[92mCommands generated successfully.\033[0m")

if __name__ == "__main__":
    main()