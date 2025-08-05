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

def remove_brackets_as_smiles(data):
    data['embeddedData']['thirdParty'] = [obj for obj in data['embeddedData']['thirdParty'] if not (isinstance(obj, dict) and obj.get('name') == ')))')]
    data['embeddedData']['thirdParty'] = [obj for obj in data['embeddedData']['thirdParty'] if not (isinstance(obj, dict) and obj.get('name') == '))')]
    return data

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
    
    processed_data = remove_brackets_as_smiles(add_info_messages(data, args.interval))
    
    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)
    
    print(f"Processing complete. Output saved to {args.output_file}")

if __name__ == "__main__":
    main()
