class CommandHandler:
    """
    Handles terminal commands and their output.
    """
    def __init__(self):
        self.commands = {}
        self.register('help', self.cmd_help)
        self.register('access', self.cmd_access)
        self.register('exit', self.cmd_exit)

    def register(self, name, func):
        self.commands[name] = func

    def handle(self, line):
        parts = line.strip().split()
        if not parts:
            return ''
        cmd = parts[0].lower()
        args = parts[1:]
        if cmd in self.commands:
            return self.commands[cmd](args)
        else:
            return f"Unknown command: {cmd}. Type 'help' for a list of commands."

    def cmd_help(self, args):
        return [
            "Available commands:",
            "  help   - Show this help message",
            "  access - Simulate system access",
            "  exit   - Exit the terminal"
        ]

    def cmd_access(self, args):
        return [
            "ACCESS GRANTED.",
            "Welcome, Operator. System ready for input."
        ]

    def cmd_exit(self, args):
        return ["Exiting terminal..."] 