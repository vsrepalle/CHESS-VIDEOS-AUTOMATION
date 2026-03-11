def build_json(parsed):

    json_data = {
        "channel": "ChessArena",
        "topic_id": "Elite_Rapid_Open_2026",
        "headline": parsed.get("headline"),
        "day": "Sunday",
        "date": parsed.get("date"),
        "location": parsed.get("location"),
        "news_type": "Chess Tournament Announcement",

        "hook_text": "A major rapid chess tournament is coming to Hyderabad with a large prize pool.",

        "details": f"The Elite Rapid Open Chess Championship will take place at {parsed.get('location')}. "
                   f"The tournament offers a prize pool of {parsed.get('total_prize_pool_rupees')} rupees "
                   f"with an entry fee of {parsed.get('entry_fee_rupees')} rupees.",

        "subscribe_hook": "Register now and compete in this exciting rapid chess event.",

        "metadata": {
            "organiser": parsed.get("organiser"),
            "contact_number": parsed.get("contact_number"),
            "total_prize_pool_rupees": parsed.get("total_prize_pool_rupees"),
            "entry_fee_rupees": parsed.get("entry_fee_rupees")
        }
    }

    return json_data