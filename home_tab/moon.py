from .api_call import make_api_call
import datetime

def get_moon_phase() -> dict:
    today = datetime.datetime.now().date()
    jd = int(today.strftime("%j"))  # Julian day of year
    url = f"https://www.icalendar37.net/lunar/api/?lang=en&month={today.month}&year={today.year}&size=100"

    data = make_api_call(url)
    
    moon_data = data['phase'][str(today.day)]
    
    return {
            "phase": moon_data['phaseName'],
            "icon": moon_data['svg']
        }

if __name__ == "__main__":
    moon_phase = get_moon_phase()
    print(f"Moon Phase: {moon_phase['phase']}")
    print(f"Icon URL: {moon_phase['icon']}")