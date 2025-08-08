import json
import argparse
from datetime import datetime, timedelta, timezone

UTC = timezone.utc

def create_info_message(comment, timestamp):
    moscow = timestamp + timedelta(hours=3)
    return {
        "_id": f"info-{comment['_id']}",
        "created_at": timestamp.isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
        "channel_id": comment["channel_id"],
        "content_type": "video",
        "content_id": comment["content_id"],
        "content_offset_seconds": comment["content_offset_seconds"],
        "commenter": {
            "display_name": "Time",
            "_id": "0",
            "name": "Time",
            "bio": "",
            "created_at": "2013-03-29T22:06:42.877141Z",
            "updated_at": datetime.now(UTC).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            "logo": "https://static-cdn.jtvnw.net/jtv_user_pictures/dbbd7c25-a736-41d3-85e6-b57bd188bbe2-profile_image-300x300.png"
        },
        "message": {
            "body": f"{moscow.strftime('%d-%m-%Y %H:%M:%S')}",
            "bits_spent": 0,
            "fragments": [{
                "text": f"{moscow.strftime('%d-%m-%Y %H:%M:%S')}",
                "emoticon": None
            }],
            "user_badges": [],
            "user_color": "#1E90FF",
            "emoticons": []
        }
    }

def parse_iso_datetime(dt_str):
    if dt_str.endswith('Z'):
        dt_str = dt_str[:-1] + '+00:00'
    return datetime.fromisoformat(dt_str)

import json

def remove_some_smiles(data):
    data['embeddedData']['thirdParty'] = [obj for obj in data['embeddedData']['thirdParty'] if not (isinstance(obj, dict) and obj.get('name') == ')))')]
    data['embeddedData']['thirdParty'] = [obj for obj in data['embeddedData']['thirdParty'] if not (isinstance(obj, dict) and obj.get('name') == '))')]
    data['embeddedData']['thirdParty'] = [obj for obj in data['embeddedData']['thirdParty'] if not (isinstance(obj, dict) and obj.get('name') == 'gg')]
    data['embeddedData']['thirdParty'] = [obj for obj in data['embeddedData']['thirdParty'] if not (isinstance(obj, dict) and obj.get('name') == 'гг')]
    data['embeddedData']['thirdParty'] = [obj for obj in data['embeddedData']['thirdParty'] if not (isinstance(obj, dict) and obj.get('name') == ':3')]
    return data

def add_biblethump_object(data):
    if 'embeddedData' not in data:
        data['embeddedData'] = {}
    if 'firstParty' not in data['embeddedData']:
        data['embeddedData']['firstParty'] = []

    biblethump_exists = any(
        isinstance(obj, dict) and obj.get('name') == 'BibleThump'
        for obj in data['embeddedData']['firstParty']
    )

    if not biblethump_exists:
        data['embeddedData']['firstParty'].append({
            "id": "86",
            "imageScale": 2,
            "data": "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",
            "name": "BibleThump",
            "width": 37,
            "height": 32,
            "isZeroWidth": False
        })

    return data;

def add_pogchamp_object(data):
    if 'embeddedData' not in data:
        data['embeddedData'] = {}
    if 'firstParty' not in data['embeddedData']:
        data['embeddedData']['firstParty'] = []

    pogchamp_exists = any(
        isinstance(obj, dict) and obj.get('name') == 'PogChamp'
        for obj in data['embeddedData']['firstParty']
    )

    if not pogchamp_exists:
        data['embeddedData']['firstParty'].append({
            "id": "88",
            "imageScale": 2,
            "data": "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",
            "name": "PogChamp",
            "width": 32,
            "height": 32,
            "isZeroWidth": False
        })

    return data;

def add_comfort_object(data):
    if 'embeddedData' not in data:
        data['embeddedData'] = {}
    if 'firstParty' not in data['embeddedData']:
        data['embeddedData']['firstParty'] = []

    comfort_exists = any(
        isinstance(obj, dict) and obj.get('name') == 'guitComfort'
        for obj in data['embeddedData']['firstParty']
    )

    if not comfort_exists:
        data['embeddedData']['firstParty'].append({
            "id": "37241",
            "imageScale": 2,
            "data": "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",
            "name": "guitComfort",
            "width": 28,
            "height": 28,
            "isZeroWidth": False
        })

    return data;

def add_info_messages(data, max_interval_minutes=10):
    if not data.get("comments"):
        return data

    comments = data["comments"]
    new_comments = []

    if comments:
        first_comment = comments[0]
        first_time = parse_iso_datetime(first_comment["created_at"])
        new_comments.append(create_info_message(first_comment, first_time))
        new_comments.append(first_comment)

        for i in range(1, len(comments)):
            prev_comment = comments[i-1]
            current_comment = comments[i]
            
            prev_time = parse_iso_datetime(prev_comment["created_at"])
            current_time = parse_iso_datetime(current_comment["created_at"])
            time_diff = current_time - prev_time
            
            if time_diff > timedelta(minutes=max_interval_minutes):
                new_comments.append(create_info_message(current_comment, current_time))
            
            new_comments.append(current_comment)

        last_comment = comments[-1]
        last_time = parse_iso_datetime(last_comment["created_at"])
        new_comments.append(create_info_message(last_comment, last_time))

    data["comments"] = new_comments
    return data

def main():
    parser = argparse.ArgumentParser(description='Add info messages between comments with large time gaps.')
    parser.add_argument('input_file', help='Input JSON file')
    parser.add_argument('output_file', help='Output JSON file')
    parser.add_argument('--interval', type=int, default=10, 
                       help='Maximum interval between comments in minutes (default: 10)')
    
    args = parser.parse_args()
    
    with open(args.input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    processed_data = add_pogchamp_object(add_comfort_object(add_biblethump_object(remove_some_smiles(add_info_messages(data, args.interval)))))
    
    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)
    
    print(f"Processing complete. Output saved to {args.output_file}")

if __name__ == "__main__":
    main()
