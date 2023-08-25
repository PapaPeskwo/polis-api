import requests

def get_events():
    url = 'https://polisen.se/api/events'
    response = requests.get(url)
    response.raise_for_status()
    events = response.json()

    # Sort by ID in ascending order
    sorted_events = sorted(events, key=lambda x: x['id'], reverse=True)
    
    return sorted_events


def filter_events(events, topic):
    if topic in ["all", ""]:
        return events
    return [event for event in events if event['type'] == topic]

def read_topics_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def display_topics_based_on_input(user_input, topics):
    if user_input == "show":
        for topic in topics:
            print(topic)
    elif "search" in user_input:
        keyword = user_input.split("search")[1].strip().lower()
        for topic in topics:
            if keyword in topic.lower():
                print(topic)

def main():
    events = get_events()
    topics = read_topics_from_file('topics.txt')

    print("Type 'show' to display all topics or 'search <keyword>' to find a topic. Type 'all' or leave blank to show all events:")
    choice = input("Enter your choice: ").strip()

    display_topics_based_on_input(choice, topics)

    if choice not in ["show", ""] and not choice.startswith("search"):
        if choice not in topics:
            print("Invalid choice. Showing all events.")
            choice = 'all'

    filtered_events = filter_events(events, choice)

    num_events = input(f"How many events do you want to see (max {len(filtered_events)})? ")
    try:
        num_events = int(num_events)
        if num_events < 0 or num_events > len(filtered_events):
            print(f"Invalid number. Showing all {len(filtered_events)} events.")
            num_events = len(filtered_events)
    except ValueError:
        print(f"Invalid input. Showing all {len(filtered_events)} events.")
        num_events = len(filtered_events)

    # Get the latest `num_events` and reverse them for display
    subset_events = filtered_events[:num_events][::-1]

    for event in subset_events:
        print(f"\nID: {event['id']}")
        print(f"Date/Time: {event['datetime']}")
        print(f"Name: {event['name']}")
        print(f"Summary: {event['summary']}")
        print(f"URL: {event['url']}")
        print(f"Type: {event['type']}")
        print(f"Location: {event['location']['name']}")
        print(f"GPS: {event['location']['gps']}")

if __name__ == "__main__":
    main()