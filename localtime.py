import datetime as dt
import zoneinfo

class Localtime:
    """set local time zone and return local time, example location Asia/Colombo"""
    def __init__ (self,location :str):
        self.location=location

    def get_local_time(self):
        try:
            time_zone = zoneinfo.ZoneInfo(self.location)
            current_time = dt.datetime.now(time_zone)
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            return formatted_time
        except zoneinfo.ZoneInfoNotFoundError:
            return "Timezone 'Asia/Colombo' not found. Ensure the tzdata package is installed."
        except Exception as e:
            return f"An error occurred: {e}"