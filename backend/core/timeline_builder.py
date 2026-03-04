def build_timeline(events):
    """
    Build a chronological timeline from extracted events.
    """

    timeline = []

    for event in events:

        date = event["date"]

        if date is None:
            continue

        # convert date to integer year
        try:
            year = int(date)
        except:
            continue

        timeline.append((year, event["event_type"], event))

    # sort by year
    timeline.sort(key=lambda x: x[0])

    return timeline

if __name__ == "__main__":

    events = [
        {'event_type': 'Birth', 'date': '1937'},
        {'event_type': 'Marriage', 'date': '1960'},
        {'event_type': 'Death', 'date': '2015'}
    ]

    timeline = build_timeline(events)

    for year, event_type, event in timeline:
        print(year, "→", event_type)