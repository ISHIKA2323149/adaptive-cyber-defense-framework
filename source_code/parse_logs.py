with open('cowrie.log', 'r') as f:
    for line in f:
        if 'login attempt' in line:
            print(line.strip())
