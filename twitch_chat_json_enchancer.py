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
            "data": "iVBORw0KGgoAAAANSUhEUgAAAEoAAABACAYAAAC9S+EXAAAMb0lEQVR42uVcCVBVRxb9rO67KKLiBiZuuIDKKKEAF7DQiIgbIFYENSbRCCgaBgjIqnGJAgoquyjuG4qWCyiCKO4xbjHglpqZykxNTTmmQs3U3Ln3Tf8/77/f7/FBlo++qlN8+ve77/bp27dv3+73VaqmvYwQfRDeiChEJuIi4hHiL4g3iN8Z3rCyR6xOJrvHm8kwUr1nlyliMiIV8QIBDYQXTOZk9owWe1kyC/ilAcmRwy/sWZYtiaC+iB2I35qAICl+Y8/ua8gEtUPEI97q27B2rVvDMGtrcB8zBvxdXGCZhwcscXcXQJ+pjL6jOlS3DoSRDnFMJ4O5jJmDfaWkPHpeGGxlBSumT4fckBC4u20bvM7KgleZmfAiIwOe79kD1RJQGX1Hdagu3ZMbHCzIIFlGtRP2iulm3NwkdUEUKCnbqW1b+Byt41J8vNDg6t27oeodQTJIFskk2fSMWggrYLo2yzURUS2nXPcOHSBy/nx4vHOnYBlVDUAQDySbnkHP6obPVCCrmuncpENtEaKGp1Brc3P4ytMTHu3YIQyfxiJIx8rwWfRMejbpIENWDdO90YcixSvRcr02YcgQuJyY2KgWpI+FkQ6ki4J1RTdm7GWOSJezohhf32YliEcY6aRgXWmsTQ1OUj7vgb27dYPCyEiDIklM1inUjXSUISu/IckiQft5D3KwsYFbW7caHEFSkI6kqwxZ+xuCLBrHGbwHuNnZwWN0noZOkhqkqyvqLENWxrv4LJoZYniCKVp+tmtXiyFJjWfp6YLuMmTF1Hc29JMj6ecWSJIapLsCWb51Jcme5YR0hltLJklMlht/GP7O2q7X1YYly7SEjLW1hScYAbd0ktSgtjhgmzhkPWIc1JqBTOaFAC1hdqvPbCgTOmyvLYNqL73J3NQUjoWHv3ckqUFtozZyyBqjNMuVaKVGjIxgtZcXPM/IeG+JoraFYhuprRKiiuVmQXcpq0P69n1vCZKC2sqxKneeNV0SVzI1MYH80NAPhihqK7VZQtQlqVWNkLI5EVffLzMzPxiiqK0TPv6YZ1UjxERpzXQmxsaw9wOyJjWozdR2CVHJ4pDgV/GXA3v2FFKtHxpR1OYB2HYJUb+qQ4VRUnP7xsen1tw2Jf1vbtkCmwMDIXjmTCGzGDFvHhxau1azOdDcDVdvTNCw0icNRG2mtnOGH3GkChUXmqFDOxcToyjwfnIyzJ4wgTelCujZuTPE+/s3CznUQQ9SUmC9nx94OjjAyP79hRTLvE8+ge+XLIGnaWmKRkBtN9N16sSRaqe4sEObNkJPyAkiKxrUq5de+2suI0YIpDalBaV98YXirgxtQGxavFjW4kkGcSC5jzhSnRcXjhwwQNY/UWrFedgwMDc3h3Xr1sHLly/hyZMnsHLlSlnFJo0cKfRiU1jSri+/FFK/gwcPhuDgYPClVLDMxulnkyfL+iniQFKfOFI9Fhd+On4816LIXPNCQoQ6y5cvB/FVU1MDs2bN4m984vBMWrSo0X0WrdusunYFDw8PePPmjUa3yspK6NixI1e3SPSpPIsiDiR1iSPVX8WFQVOnchtFqQlv9EtUZyeuvKVXbGysrFXZoZ+oLYa5mpQEqcuWQTRaAYE+U5k+sRzpG4s+kZ5VUlKio5sP30FDm1atoBJdiVQWccCZ+bTzTiE4g8mlJWytrIQ6c+bM0VLk7du34ObmJkuURadOcCUxkUv+90FBcssHzTKK6ijlwYjMiWx76uTJkzpETZo0SVY+b4YnDjh5KtW/xIVh3t5cZWhzUb0Ta4KzQkBAgNB7RUVFMG3aNEWn3qldOzgbHa0lr3LzZnAaOlTvgxdUl+6R852DLC2FeiNwAnn9+rWGpDT0j60VDnhMHztWpxOIA0k94kj1b32Iom1rawuLeh3HscRwoXzDBo2sG9jggaxhdQHdc4NDFunWXxQotsFZy8nJCQboOmUd0OQkzf+v1vW3AlFaW+NUSa7XPJH9+hA1HIfFM+ZrfkpPF+Kb+p6BontJhtYQzs4G24ED6yXPB/3uzxIftdTdnbcVr/qnuJCO1MgFZAfDwuqsiImpKXwWEwePsrIEGRS5c9ZT+svDe0mGdKPTe2FAveQloguplsha4OwsrUccCQdKNYWBU6YohvtR8+fXSRGHT70g+UoZ3rtLkEsRMpUbY4Otra1h+PDhMHr0aLC3t4exaLFqTMCepuFDoM/jxo2Dfv36CfeSDLGO1Wjt2Xv3Q5feveukG6WBf0xN1QkPOLs0xJHqJ3EhLU2UIvMqVDAsNh7ad+2mqISpeStwC1oKsRU34XDhGaExFKUPZ42lRmfjkMnNzYWcnBwu6Hs16P8YXF60wimdZEgj/pv5+yA4vwA6W+q3ajBBOXvDw3VGDwWcdMKPc2RIVSouHI9RrVLscjs3D2Jv3IaY0nKYsXot9Br80f+DS7QS+n/S0s8h7NQZSKi8Axuu3YDbeXnCveUbN0J3FvwRURnYIVIylMiKxpmTiCIZJEsr/iGrOn8JIi6UwEh3D8FiZScXG1v4Ci3wzPGT3FCjve4S5i4RlSMu7IxTuVKK5QgSEHf9FsQzJN26B9FIGhETU3pN+D8eiaTvqF7BmXNCI+jeUgwg1eswipa9cYadh9Hx7NmzwcvLC2bMmAFTMdijuIf+enp6wnT0mVQ+E2MbR0dHgQCSQbKkut1F69xQfgMSb96FkMPHwMlvIfQcZANtMY6jDnTy84egtN2QiB1I+mVcKNZy5IQynJ3NdDcbKH+uitDKHmClMklvaWY+HHYpl69qSKoNW5G4h5lZmvvvbd+uMWuawinmsbOz0xs2NjYCUUNRBsnSidCxQ4qOHtc8PwE7LOn2fdhw5wfhbwLrQDU2X60Q2iSWkYIrAmPdrAidTVBNka7NtgQG8oNOtLQ4PUlKQN9Utr9AZ3lAaQzKXS3DIPXruXNhJUb5oQsWQBguWwhrcLIIw/+/8fODCJyRIhn+SH8XLoQ1aIUkQ2ntmHX+ol56xiKeiPwxTRABrq684bpCvTP8H/EXM2UWxhXoMGMlvSKH4ycKNUNObn2mhKp3WEQ/yMqG78qu16rjemzL/ewcra2rHjhMOUQNUKeCtfbz2qHDfMg50nPx0BG9eir90mWdsd+kyTvsoEJ01PoQpZ5oCDmrVvFivGfiXeNV0uFHgZhUgTPHTtRKVNK1Sqjcm9/856EyMmFTLVZFo+NW3l7NbEe5M441rRfvwvSQDr/+PXro+IGTJ04pEkXf5Z67oDjkmtKqDp4uUtSXiLrJiCqMipLbWreWHs7YJ65Anj/O31+LrKOnTiv2UGJFJVTs22cwuyrlOJnQpKJEFA29l+ibZE4RH+Ud1hjDe1dFHCocwQhbiahtV8oN62gPEvBd+XVFH/UAg1raSZJZfzrIHfnROdQ6DiN1dZh/7FSh4rA7ePqsQQw7zSyGuuwoLlXU+VxCArTFyUvmxLDs0R8L6SKZHDulRsk8C48rO/OSg4cMyqKo02hlIKdz1NnzYM3PixEH3Ws7TDaTl9qgRHwJRr1xCrPdndw8g9v9PS3TueFnLwhrPpn14Ax9TwOn8cjynTcfEnAdxSNqU1kFPDXAQ/nFBw9rrxjQL329/xB06WUlR1JyXU4HmyEqdITgMBzq4gpRxbrrvWRcAz6XZB4NAaUHDkA8m/losewd+S2Y8n2Sev/OrK4ng7sh7vEEdrSwAP9NWyCRMgWMqN0XSwTnaXBEFRwQsgWhR0+CreMfhM6WIekyovW7vLh4jSsYHzjQ3gGWZ+YKhGVeKDaoGU+ItnECOpWcAo7ePmBiZqaUyDvcEK95kIDdsq/AImH9Ro2C0PAIqMKh19znPdWv3NK6zX30aN4pOjFoNRLWkK+kUTzhg/izUnqVDjfMdXISzgA8TE3936uxjezgSf6rrCzheXtWrAA/Fxfo0r69PungHxGOjfkOcYp0L1But4Ry2xSDUeRLG6B0WEPrhWv20vVzhXTLc85L2LQhcCIiQjjTsMjNDYb06VOXnZ2/I0Ia41093mXDfgKkpi67HvRWOfU2nUWglfosR0fwdXaGAGwsnS4JmjJFIFYAfqayha6uMGfiRKE+EdK+bq/1i/E3xLeIzs3xAnZPxDcsZwMGiiuIQEQrQ/ntA3v2AxE/NDMxNSweWm3ov6ihYuukuYiNbAfjH41IzGvEEbZJ4tpUvqexLiOWHHRGLGa+YgeLX4jI24in7Jcv/sR+lKaKzUy0QihC5CE2I9Yg5rADqE32kyL/Bdh75VgXPwo1AAAAAElFTkSuQmCC",
            "name": "BibleThump",
            "width": 37,
            "height": 32,
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
    
    processed_data = add_biblethump_object(remove_brackets_as_smiles(add_info_messages(data, args.interval)))
    
    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)
    
    print(f"Processing complete. Output saved to {args.output_file}")

if __name__ == "__main__":
    main()
