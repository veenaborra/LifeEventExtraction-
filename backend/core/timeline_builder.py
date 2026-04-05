def build_timeline(events):

    merged = {}

    for e in events:

        year = e.get("year")
        span = e.get("span")

        # skip invalid events
        if not year or not span:
            continue

        key = (year, span)

        #  create new entry if not exists
        if key not in merged:
            merged[key] = {
                "year": year,
                "span": span,
                "event_types": set(),
                "event": e
            }

        # 🔥 merge event types
        merged[key]["event_types"].add(e["event_type"])

    
    #  BUILD FINAL TIMELINE
   
    timeline = []

    for (year, span), data in merged.items():

        #  combine event types
        event_types = "+".join(sorted(data["event_types"]))

        timeline.append((year, event_types, data["event"]))

    #  sort by year
    timeline.sort(key=lambda x: x[0])

    return timeline