from orchestrator import InterviewOrchestrator


def main():
    print("\n AI Mock Interview Coach\n")

    role = input("Enter target role: ")
    focus = input("Enter focus area (technical/behavioral/mixed): ")
    background = input("Enter background (optional): ")

    orchestrator = InterviewOrchestrator()
    orchestrator.run(role, focus, background)


if __name__ == "__main__":
    main()