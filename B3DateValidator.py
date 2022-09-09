import pandas_market_calendars as mcal
import pandas as pd


class B3DateValidator:
    def __init__(self, date):
        self.bmf = mcal.get_calendar('BMF')
        self.valid_date = self._validate_date(date)

    def _validate_date(self, date):
        date_index = self.bmf.valid_days(start_date=date, end_date=date)

        if date_index.size == 0:
            return pd.to_datetime(date) + pd.offsets.BusinessDay(-1)
        else:
            return pd.to_datetime(date)
